# Code Libraries
from searchs import SpotifyClient
from dataframes import SpotifyDataFrame

# Style Libraries

import time
from colorama import Fore

# Instances

sp = SpotifyClient()
df = SpotifyDataFrame()

# -------------------------------------------------------------------

# Load Users Data

user = sp.me()
username = user['username']
user_id = user['id']
user_ct = user['country']
user_followers = user['followers']

# Greeting the User

print('Hey ' + f'{Fore.LIGHTBLUE_EX + username}' + Fore.RESET + '!!')
print(Fore.RESET + 'Welcome to the ' + Fore.RED + 'BEST' + Fore.RESET + Fore.GREEN + ' Playlist Creator'
      + Fore.RESET + ' that you will find online!')
print('Here is some of your stats on Spotify:')
print('Here is your ID: ' + f'{Fore.LIGHTBLUE_EX}{user_id}')
print(Fore.RESET + 'Your number of followers: ' + f'{Fore.LIGHTBLUE_EX}{user_followers}')
print(Fore.RESET + 'Your country: ' + Fore.LIGHTBLUE_EX + user_ct)
time.sleep(1)
print()

print(Fore.RESET + 'For this to work I will need some inputs from you! \nI will need a Artist, a Track,'
                   ' an Energy and a Mood.')
print()
print('But no worries I will explain what everything means')
print()
time.sleep(1)
print(Fore.LIGHTBLUE_EX + 'Energy parameter: ' + Fore.RESET + 'Represents a perceptual measure of intensity and '
                                                              'activity.'
                                                              '\nTypically, energetic tracks feel fast, loud, '
                                                              'and noisy.')

print()
time.sleep(1)
print(Fore.LIGHTBLUE_EX + 'Mood parameter: ' + Fore.RESET + 'Represents the general feel of the song, a higher number '
                                                            'sound more positive (e.g. happy, '
                                                            '\ncheerful, euphoric), while tracks with a lower number sound more negative (e.g. sad, depressed, angry)')
print()
time.sleep(1)
print('Please read carefully the parameters descriptions above to get the best results.')
print('Now lets start!')
print()
time.sleep(1)


def creator():
    while True:

        # Inputs

        artist_input = input(Fore.LIGHTRED_EX + 'Enter the Artist Name: ')
        track_input = input(Fore.LIGHTRED_EX + 'Enter the Track Name: ')
        target_energy = input(Fore.LIGHTRED_EX + 'Enter the Target Energy: ')
        target_mood = input(Fore.LIGHTRED_EX + 'Enter the Target Mood: ')
        print()
        print(Fore.RESET + 'All right, just a minute and I will be back with the results')

        # Setting up base queries

        artist = sp.artist(artist_input)

        artist_id = ''.join(artist['id'])
        genres = ''.join(artist['genres'])

        track = sp.track(track_input)

        track_id = ''.join(track['id'])

        seed_artist = artist_id

        seed_track = track_id

        seed_genre = genres

        # Query
        recommendations = sp.recommendations(seed_artist,
                                             seed_track,
                                             seed_genre,
                                             target_energy,
                                             target_mood)
        print()
        print(Fore.LIGHTYELLOW_EX + f"{recommendations['recommendations'].to_string(index=False)}")
        print()
        print(Fore.RESET + 'Cool ' + f'{Fore.LIGHTBLUE_EX + username}' + Fore.RESET + '!!')
        print()
        time.sleep(1)
        print('Now I need just a couple more things to get your playlist ready!')
        print()
        time.sleep(1)
        pl_name = input(Fore.LIGHTRED_EX + 'Could you name your playlist? ')
        time.sleep(1)
        print()
        pl_disc = input(Fore.LIGHTRED_EX + 'Now, do you want to give some description? (optional) ')
        time.sleep(1)
        print()
        print(Fore.RESET + 'Cool, be right back')

        # Setting Up Play list

        playlist = sp.create_list(f'{user_id}', f'{pl_name}', f'{pl_disc}')

        playlist_id = playlist['id']
        playlist_url = playlist['url']

        # Adding Tracks

        recommendations_ids = recommendations['id']

        add_songs = sp.add_songs(playlist_id, recommendations_ids)

        print()
        print('Yo, just finished, here is your playlist info')
        print()
        print(Fore.RESET + 'Playlist Name: ' + Fore.LIGHTYELLOW_EX + f'{pl_name}',
              Fore.RESET + '\nID: ' + Fore.LIGHTYELLOW_EX + f'{playlist_id}',
              Fore.RESET + '\nURL: ' + Fore.LIGHTYELLOW_EX + f'{playlist_url}')
        print()
        time.sleep(1)
        print(Fore.RESET + 'Hope you enjoy your new playlist!!')
        print('Just one more thing, do you want do it again?')
        print()
        time.sleep(1)
        print(Fore.LIGHTBLUE_EX + '1' + Fore.RESET + '- Yes')
        print(Fore.LIGHTBLUE_EX + '2' + Fore.RESET + '- No')
        print()
        response = input(Fore.LIGHTRED_EX + 'Choose a number: ')
        if response == '1':
            print(Fore.RESET + 'Nice, let clear your last results')
            print()
            time.sleep(1)
            continue

        else:
            print('No worries, we do it another time!')
            break


if __name__ == '__main__':
    creator()
