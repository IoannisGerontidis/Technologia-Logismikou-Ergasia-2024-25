import csv
import time
import textwrap

def generate_list_games(filename):

    main_list = []

    file_in = open(filename, encoding='UTF-8', errors='replace')

    file_in.readline()
    file_in = csv.reader(file_in)

    for line in file_in:
        if ";" in line[3]:
            line[3] = line[3].split(";")
        else:
            line[3] = [line[3]]      
        if ";" in line[5]:
            line[5] = line[5].split(";")
        else:
            line[5] = [line[5]]
        if ";" in line[6]:
            line[6] = line[6].split(";")
        else:
            line[6] = [line[6]]
        if ";" in line[7]:
            line[7] = line[7].split(";")
        else:
            line[7] = [line[7]]
        if ";" in line[8]:
            line[8] = line[8].split(";")
        else:
            line[8] = [line[8]]
        if ";" in line[10]:
            line[10] = line[10].replace(";",",")
        
        
        
        main_list.append(line)

    return main_list


def print_menu(menu_list):

    print("\n"*5)
    for i in range(0, len(menu_list)):
        print(f'{i+1}. {menu_list[i]}')


def get_menu_selection(menu_list):

    possible_choice_values = []
    for i in range(0, len(menu_list)):
        possible_choice_values.append(str(i+1))

    choice = input("Type number to choose ... ")

    while choice not in possible_choice_values:
        print("Incorrect selection")
        print("\n"*30)
        
        print_menu(menu_list)
        choice = input("Type number to choose ...")

    return int(choice)


def get_all_possible_genres(list_of_games):

    genres = []
    
    for game in list_of_games:
        for genre in game[6]:
            if genre not in genres:
                genres.append(genre)

    genres.sort()
    return genres


def print_genres(list_genres):

    print("\n\nAll genres available are:")
    print("-"*20)

    for item in list_genres:
        print(f'{item:<30}')
    
    print("\n") 


def get_valid_genre(list_genres):

    genre = input("What genre would you like to filter for?")
    while genre not in list_genres:
        genre = input("Sorry that genre name is not valid. Please try again")
    
    return genre


def filter_all_listings_genre(list_of_games, genre):

    sub_list = []

    for item in list_of_games:
        if genre in item[6]:
            sub_list.append(item)

    return sub_list



def get_valid_listing(list_games):

    possible_choice_values = []
    for i in range(0, len(list_games)):
        possible_choice_values.append(str(i+1))
    
    choice = input("Which listing would you like to choose?")

    while choice not in (possible_choice_values):
        choice = input("Invalid choice. Try another number")

    choice = int(choice) - 1

    return list_games[choice]


def print_listings_table(list_games):

    for i in range(0, len(list_games)):
        game = list_games[i]
        s = f"{i+1:<3} {game[0]:<30}"
        print(s)


def print_game_details(some_game):
    s = "\n"
    s += some_game[0]  + "\n" + "-"*40

    k = some_game[10]

    t = f'Released on: {some_game[1]}\n\n'
    t += f'Metacritic score: {some_game[2]}\n\n'
    t += f'ESRB rating: {some_game[3]}\n\n'
    t += f'Average Playtime: {some_game[4]} hours\n\n'

 # check if the game has any developers
    if len(some_game[8])>=1:    
        d = f'Developed by: '
        for dev in some_game[8]:
            d += dev + ", "
            
        ##Removes last comma and space for formating
        d = d[:-2]
        ##Edits d before adding it to t
        t += d
        t += '\n\n'

# check if the game is playable on any platform      
    if len(some_game[5])>=1:
        p = 'Playable on: '
        for platform in some_game[5]:
            p += platform+ ", "
        
        p = p[:-2]
        t += p 
        t += '\n\n'

# check if the game has any genres
    if len(some_game[6]) >= 1:
        g = 'Genres: '
        for genre in some_game[6]:
            g += genre + ", "

        g = g[:-2]
        t += g
        t += '\n'

# print the game title and a line of dashes
    print(s)
    print("")
# print the game's description
    print(textwrap.fill(k, width = 90))
    print("")
# print the game's release date, metacritic score, ESRB rating, playtime, developers, platforms, and genres
    print(t)
    
##Adds All ESRB Ratings in a List 
def get_all_possible_ESRB_ratings(list_of_games):

    ESRB_Ratings = []
    
    for game in list_of_games:
        for ESRB_Rating in game[3]:
            if ESRB_Rating not in ESRB_Ratings:
                ESRB_Ratings.append(ESRB_Rating)

    ESRB_Ratings.sort()
    return ESRB_Ratings

##Formatted And Made it So the User Can see ESRB_Rating and the Age range 
def print_ESRB_Ratings(list_ESRB_Ratings):

    print("\n\nAll ratings available are:")
    print("-"*35)

    print("Everyone                      6+")
    print("Everyone 10+                  10+")
    print("Teen                          13+")
    print("Mature                        17+")
    print("Adults Only                   18+")
    print("Rating Pending                N/A")
    print("Press Enter for Games with rating pending")
            
    print("\n")

##Gets valid Rating From User 
def get_valid_rating(list_ratings):

    rating = input("What ESRB Rating would you like to filter for?")
    while rating not in list_ratings:
        rating = input("Sorry that age rating is not valid. Please try again")
    
    return rating

##Using User Input, Sublist Filters all games in that rating 
def filter_all_listings_rating(list_of_games, rating):

    sub_list = []

    for item in list_of_games:
        if rating in item[3]:
            sub_list.append(item)

    return sub_list

def user_metacrtic_range(continue_1):
    continue_1 = "no"
       #While Loop if User Enters no for continue it restarts while loop 
    while continue_1 == "no" or continue_1 == "NO" or continue_1 == "No":
        print("Please Enter a Low and High Value between 0 and 100 to filter a Metacrtic Score")
        LowEnd = int(input("\nPlease Input a Low Number for Your Range"))
        #If out of range 
        if LowEnd > 100 or LowEnd < 0:
            LowEnd = int(input("\nThat Low End Number is not within the range"))
            
        HighEnd = int(input("\nPlease Input a High Number for Your Range"))
        while HighEnd > 100 or HighEnd < 0 or HighEnd <= LowEnd:
            if HighEnd > 100:
                HighEnd = int(input("\nThat High End Number is not within the range, Try Again "))
            elif HighEnd < 0:
                HighEnd = int(input("\nThat High End Number is not within the range, Try Again "))
                #If HighEnd Lower or Equal to LowEnd
            else:
                HighEnd = int(input("\nHighEnd Cant Be Lower Than or Equal To LowEnd, Try Again "))
            
        continue_1 = input(f'\nThe Range you would Like to Filter for are games between {LowEnd} and {HighEnd}\nWould You Like To Continue?')

    return [LowEnd, HighEnd]
    

def get_all_possible_platforms(list_of_games):

    platforms = []

    for game in list_of_games:
        for platform in game[5]:
            if platform not in platforms:
                platforms.append(platform)

    platforms.sort()

    return platforms

def print_platforms(list_platforms):
    print("\n")
    print("Choose Desired Platform to Filter For:")
    print("-"*20)
    
    for i in range(0, len(list_platforms)):
        print(f'{i+1:>2}. {list_platforms[i]}')
        time.sleep(0.02)

    print("\n")

##Gets valid Platform From User 
def get_valid_platform(list_platform):

    platform = input("What platform would you like to filter for?")
    while platform not in list_platform:
        platform = input("Sorry that platform is not valid. Please try again")
    
    return platform


def filter_all_listings_score_platform(list_of_games, game_platform, Low, High):

    sub_list = []

    for item in list_of_games:
        if game_platform in item[5]:#Checks If game is In Given Platform
            if item[2]: #Checks if Theres a Score in Metacritic Score
                if int(item[2]) >= Low and int(item[2]) <= High: #If Score Is WIthin Range
                    sub_list.append(item)


    return sub_list


def print_listing_Platfom_score(sub_list_platformscore, Low, High):

    if not sub_list_platformscore: #If Sublist Is Empty
        print("\n\n\n\nNo games within this range on chosen platform") 
    else:
        print("No.  Game Title                      Metacritic Score")
        print("-" * 55)


    for i in range(len(sub_list_platformscore)):
        game = sub_list_platformscore[i]
        s = f"{i+1:<3} {game[0]:<30} {game[2]:>3}" #For Every Game In List Prints Game and Metacritic Score 
        print(s)

        if i < len(sub_list_platformscore) - 1:
            print("-" * 55)

    print(f'\n\nThese are all the games on this platform between {Low} and {High}')


def filter_by_playtime(list_of_games, hours):

    playable_games = []

#If Amount of Hours is Equal to, or Less Than Amount User Has To Play Add Game to List
    for game in list_of_games:
        if int(game[4]) <= hours:
            playable_games.append(game)

    return playable_games


def get_user_playtime():
    print("\n"*3)
    playtime = int(input("How Many Hours are you willing to put on a game"))

    return playtime

def main():
    main_game_list = generate_list_games("video_game_data.csv")

    all_platforms = get_all_possible_platforms(main_game_list)
    
    all_genres = get_all_possible_genres(main_game_list)

    all_ESRB_Ratings = get_all_possible_ESRB_ratings(main_game_list)


    menu_items = ['See All Listings', 'Find game by genre', 'Find game by ESRB Rating', 'Find Listings in Range of Metacritic Score', 'Find Listing Based on User Play Time', 'Exit']
    
    print_menu(menu_items)
    choice = get_menu_selection(menu_items)
    
    while 0 < choice and choice < len(menu_items):

        ##See all listings
        if choice == 1:
            print_listings_table(main_game_list)

        #Find listing by Genre
        elif choice == 2:
            print_genres(all_genres)

            genre = get_valid_genre(all_genres)

            sub_list_genres = filter_all_listings_genre(main_game_list, genre)

            print_listings_table(sub_list_genres)

            current_game = get_valid_listing(sub_list_genres)
            
            print_game_details(current_game)

        #Find listing by Rating
        elif choice == 3:
            print_ESRB_Ratings(all_ESRB_Ratings)

            ESRB_Rating = get_valid_rating(all_ESRB_Ratings)

            sub_list_ratings = filter_all_listings_rating(main_game_list, ESRB_Rating)
            print_listings_table(sub_list_ratings)

            current_game = get_valid_listing(sub_list_ratings)
            print_game_details(current_game)
        
        #Filter Listing by Platform and Metacritic Score   
        elif choice == 4:
            continue_1 = input("Press Enter To Start")

            Range = user_metacrtic_range(continue_1)
            #Range is a list so uses Index to get Value for LowEnd and HighEnd
            LowEnd = Range[0]
            HighEnd = Range[1]
            
            print_platforms(all_platforms)

            platform = get_valid_platform(all_platforms)

            #Gets Sublist Using Platform Low End and High End 
            sub_list_platform_score = filter_all_listings_score_platform(main_game_list, platform, LowEnd, HighEnd)

            print_listing_Platfom_score(sub_list_platform_score, LowEnd, HighEnd)
            
        #Filter Based on Number of Hours User Has to Play
        elif choice == 5:

            #Gets Number Of Hours From User 
            number_of_hours = get_user_playtime()

            #Filters all games Equal or Below Playtime
            playtime_gamelist = filter_by_playtime(main_game_list, number_of_hours)
            
            print_listings_table(playtime_gamelist)
            print("\nHere are all the games you can play with the amount of hours chosen")
            
            current_game = get_valid_listing(playtime_gamelist)

            print_game_details(current_game)
            

        print_menu(menu_items)
        choice = get_menu_selection(menu_items)
        
        

    print("\n\nGood bye!")
    
    


if __name__ == "__main__":
    main()



