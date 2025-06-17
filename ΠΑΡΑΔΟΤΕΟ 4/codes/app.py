# Εισαγωγή απαραίτητων βιβλιοθηκών
from flask import Flask, render_template, request, redirect, session, url_for
import json
import os
from datetime import datetime

# Εισαγωγή βοηθητικών συναρτήσεων από το άλλο αρχείο (διαχείριση φίλτρων και δεδομένων)
from project import (
    generate_list_games, get_all_possible_genres, get_all_possible_ESRB_ratings,
    get_all_possible_platforms, filter_all_listings_genre,
    filter_all_listings_rating, filter_by_playtime,
    filter_all_listings_score_platform
)

# Δημιουργία Flask εφαρμογής
app = Flask(__name__)
app.secret_key = 'secretkey'  # Χρησιμοποιείται για την ασφάλεια των sessions

# Ονόματα αρχείων για χρήστες και δεδομένα παιχνιδιών
USERS_FILE = 'users.json'
CSV_FILE = 'video_game_data.csv'

# Συνάρτηση για μετατροπή string σε datetime αντικείμενο
def parse_date(d):
    try:
        return datetime.strptime(d, '%Y-%m-%d')
    except:
        return datetime.min  # Επιστρέφει την ελάχιστη ημερομηνία αν υπάρχει σφάλμα

# --------- Διαχείριση χρηστών (φόρτωση/αποθήκευση) ---------

# Φόρτωση χρηστών από αρχείο JSON
def load_users():
    try:
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
            # Εάν κάποιο χρήστης αποθηκεύτηκε ως string, τον μετατρέπουμε σε dict
            for k, v in users.items():
                if isinstance(v, str):
                    users[k] = {"password": v, "favorites": []}
            return users
    except:
        return {}  # Αν δεν υπάρχει το αρχείο ή είναι άδειο

# Αποθήκευση χρηστών στο αρχείο
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

# --------- ROUTES ---------

# Εγγραφή χρήστη
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        # Έλεγχος για κενά πεδία
        if not username or not password:
            return render_template('register.html', error="❌ Συμπληρώστε όλα τα πεδία.")

        # Έλεγχος αν ο χρήστης υπάρχει ήδη
        if username in users:
            return render_template('register.html', error="Ο χρήστης υπάρχει ήδη.")

        # Δημιουργία νέου χρήστη
        users[username] = {
            "password": password,
            "favorites": []
        }

        save_users(users)
        return redirect(url_for('login', success="1"))

    return render_template('register.html')

# Σύνδεση χρήστη
@app.route('/login', methods=['GET', 'POST'])
def login():
    success = request.args.get('success')
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']

        # Έλεγχος στοιχείων σύνδεσης
        if username in users:
            current = users[username]
            if isinstance(current, dict) and 'password' in current:
                if current['password'] == password:
                    session['user'] = username
                    return redirect(url_for('home'))

        return render_template('login.html', error="❌ Λάθος στοιχεία.", success=success)

    return render_template('login.html', success=success)

# Αποσύνδεση χρήστη
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Σελίδα λεπτομερειών για ένα συγκεκριμένο παιχνίδι
@app.route('/game/<int:index>')
def game_details(index):
    games = generate_list_games(CSV_FILE)
    try:
        game = games[index]
    except IndexError:
        return "Το παιχνίδι δεν βρέθηκε."

    # Έλεγχος αν είναι στα αγαπημένα
    is_favorite = False
    if 'user' in session:
        users = load_users()
        user_data = users.get(session['user'], {})
        is_favorite = index in user_data.get("favorites", [])

    return render_template("game_details.html", game=game, index=index, is_favorite=is_favorite)

# Αναζήτηση παιχνιδιού με βάση τον τίτλο
@app.route('/search')
def search_title():
    query = request.args.get('query', '').strip().lower()
    games = generate_list_games(CSV_FILE)

    if not query:
        return render_template("result.html", games=[], title="Δεν δόθηκε λέξη αναζήτησης")

    # Εύρεση παιχνιδιών που περιέχουν την αναζητούμενη λέξη στον τίτλο
    results = [(i, g) for i, g in enumerate(games) if query in g[0].lower()]
    return render_template("result.html", games=results, title=f"Αποτελέσματα αναζήτησης για: '{query}'")

# Φιλτράρισμα με συνδυασμό κριτηρίων
@app.route('/filter/combined', methods=['POST'])
def filter_combined():
    genre = request.form.get("genre")
    platform = request.form.get("platform")
    rating = request.form.get("rating")
    low = request.form.get("score_low")
    high = request.form.get("score_high")
    playtime = request.form.get("playtime")

    all_games = generate_list_games(CSV_FILE)
    filtered = []

    # Εφαρμογή όλων των φίλτρων
    for i, g in enumerate(all_games):
        match = True
        if genre and genre not in g[6]:
            match = False
        if platform and platform not in g[5]:
            match = False
        if rating and rating not in g[3]:
            match = False
        if low and high:
            try:
                score = int(g[2]) if g[2].isdigit() else -1
                if not (int(low) <= score <= int(high)):
                    match = False
            except:
                match = False
        if playtime:
            try:
                pt = int(g[4]) if g[4].isdigit() else 9999
                if pt > int(playtime):
                    match = False
            except:
                match = False

        if match:
            filtered.append((i, g))

    return render_template("result.html", games=filtered, title="Αποτελέσματα φίλτρου")

# Αρχική σελίδα
@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))

    page = int(request.args.get('page', 1))
    per_page = 100

    all_games = generate_list_games(CSV_FILE)
    total_pages = (len(all_games) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    games = all_games[start:end]

    # Δημιουργία κατηγοριών HOT / BEST / NEW
    users = load_users()
    favorite_counts = {}
    for user in users.values():
        for i in user.get("favorites", []):
            favorite_counts[i] = favorite_counts.get(i, 0) + 1

    top_favorites = sorted(favorite_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    hot_indices = set(i for i, _ in top_favorites)

    best_games = [(i, g) for i, g in enumerate(all_games) if g[2].isdigit()]
    best_games_sorted = sorted(best_games, key=lambda x: int(x[1][2]), reverse=True)[:5]
    best_indices = set(i for i, _ in best_games_sorted)

    new_games = sorted([(i, g) for i, g in enumerate(all_games)], key=lambda x: parse_date(x[1]), reverse=True)[:5]
    new_indices = set(i for i, _ in new_games)

    # Προετοιμασία για σύγκριση
    compare_list = session.get("compare_list", [])
    compare_titles = []
    for idx in compare_list:
        try:
            idx_int = int(idx)
            if 0 <= idx_int < len(all_games):
                compare_titles.append(all_games[idx_int][0])
            else:
                compare_titles.append(f"Παιχνίδι #{idx}")
        except:
            compare_titles.append(f"Παιχνίδι #{idx}")

    # Φόρτωση διαθέσιμων φίλτρων
    genres = get_all_possible_genres(all_games)
    ratings = get_all_possible_ESRB_ratings(all_games)
    platforms = get_all_possible_platforms(all_games)

    return render_template(
        'index.html',
        games=games,
        genres=genres,
        ratings=ratings,
        platforms=platforms,
        page=page,
        total_pages=total_pages,
        hot_indices=hot_indices,
        best_indices=best_indices,
        new_indices=new_indices,
        compare_list=compare_list,
        compare_titles=compare_titles
    )

# Προσθήκη ή αφαίρεση αγαπημένου παιχνιδιού
@app.route('/favorite/<int:index>', methods=['POST'])
def toggle_favorite(index):
    if 'user' not in session:
        return redirect(url_for('login'))

    users = load_users()
    username = session['user']
    user_data = users.get(username)

    if user_data:
        favs = user_data.get("favorites", [])
        if index in favs:
            favs.remove(index)
        else:
            favs.append(index)
        user_data["favorites"] = favs
        users[username] = user_data
        save_users(users)

    return redirect(url_for('game_details', index=index))

# Προβολή αγαπημένων παιχνιδιών
@app.route('/favorites')
def show_favorites():
    if 'user' not in session:
        return redirect(url_for('login'))

    users = load_users()
    fav_indices = users.get(session['user'], {}).get("favorites", [])
    all_games = generate_list_games(CSV_FILE)

    fav_games = [(i, all_games[i]) for i in fav_indices if i < len(all_games)]

    return render_template("result.html", games=fav_games, title="Τα αγαπημένα μου παιχνίδια")

# Προβολή στατιστικών
@app.route('/stats')
def game_stats():
    if 'user' not in session:
        return redirect(url_for('login'))

    games = generate_list_games(CSV_FILE)
    users = load_users()

    favorite_counts = {}
    for user in users.values():
        for index in user.get("favorites", []):
            favorite_counts[index] = favorite_counts.get(index, 0) + 1

    hot_games = sorted(favorite_counts.items(), key=lambda x: x[1], reverse=True)
    hot_games_list = [games[i] for i, _ in hot_games[:5]]

    best_games = [g for g in games if g[2].isdigit()]
    best_games_sorted = sorted(best_games, key=lambda g: int(g[2]), reverse=True)[:5]

    new_games = sorted(games, key=lambda g: parse_date(g[1]), reverse=True)[:5]

    return render_template("stats.html", hot=hot_games_list, best=best_games_sorted, new=new_games)

# Σύγκριση δύο παιχνιδιών
@app.route('/compare')
def compare():
    if 'user' not in session:
        return redirect(url_for('login'))

    compare_list = session.get('compare_list', [])
    if len(compare_list) != 2:
        return "<h3>❌ Πρέπει να επιλέξεις 2 παιχνίδια για σύγκριση. <a href='/'>Πίσω</a></h3>"

    games = generate_list_games(CSV_FILE)

    try:
        g1 = games[int(compare_list[0])]
        g2 = games[int(compare_list[1])]
    except:
        return "<h3>⚠️ Σφάλμα στη σύγκριση.</h3>"

    session['compare_list'] = []  # Εκκαθάριση μετά τη σύγκριση

    return render_template("compare.html", g1=g1, g2=g2)

# Προσθήκη παιχνιδιού στη λίστα σύγκρισης
@app.route('/add_to_compare/<int:index>')
def add_to_compare(index):
    compare_list = session.get("compare_list", [])
    index_str = str(index)

    if index_str in compare_list:
        return redirect(url_for('home'))

    if len(compare_list) >= 2:
        return "<h3>❌ Μπορείς να συγκρίνεις μόνο 2 παιχνίδια. <a href='/'>Πίσω</a></h3>"

    compare_list.append(index_str)
    session['compare_list'] = compare_list

    if len(compare_list) == 2:
        return redirect(url_for('compare'))

    return redirect(url_for('home'))

# Εκκίνηση εφαρμογής
if __name__ == '__main__':
    app.run(debug=True)
