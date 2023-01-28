# Libraries
from auth import SpotifyAuthClient
from dataframes import SpotifyDataFrame

# Instances

spotify = SpotifyAuthClient()
sp = spotify.auth_obj()
df = SpotifyDataFrame()


# Setting up the main class
class SpotifyClient:

    # Creating Methods

    @staticmethod
    def me():
        user = sp.current_user()

        return {'username': user['display_name'],
                'id': user['id'],
                'followers': user['followers']['total'],
                'country': user['country']}

    @staticmethod
    def artist(artist_name):

        for a in range(0, 100, 10):
            artist_search = sp.search(q=f'artist:{artist_name}',
                                      type='artist',
                                      limit=1,
                                      offset=0)

            # Response

            if artist_search:
                artist_data = df.artist_data(artist_search)
                return artist_data

        else:
            raise Exception(f'I could not find {artist_name}, please check the spell!')

    @staticmethod
    def track(tracks_name):

        for a in range(0, 100, 10):
            track_search = sp.search(q=f'track:{tracks_name}',
                                     type='track',
                                     limit=1,
                                     offset=0)

            # Response

            if track_search:
                return df.track_data(track_search)

    @staticmethod
    def recommendations(seed_artist, seed_track, seed_genre, target_energy, target_valence):

        for a in range(0, 100, 10):
            recommendations_search = sp.recommendations(seed_artists=[f'{seed_artist}'],
                                                        seed_tracks=[f'{seed_track}'],
                                                        seed_genres=[f'{seed_genre}'],
                                                        target_energy=f'{target_energy}',
                                                        target_valence=f'{target_valence}',
                                                        min_popularity=0,
                                                        max_poularity=100,
                                                        limit=15)

            if recommendations_search:
                return df.recommendation_data(recommendations_search)

    @staticmethod
    def create_list(user_id, playlist_name, description):
        create = sp.user_playlist_create(user=f'{user_id}',
                                         name=f'{playlist_name}',
                                         public=False,
                                         collaborative=False,
                                         description=f'{description}')

        if create:
            return {'name': create['name'],
                    'id': create['id'],
                    'url': create['external_urls']['spotify']}

        else:
            raise Exception(f' I could not save your playlist, please revisit your input!')

    @staticmethod
    def add_songs(playlist_id, track_id):
        add = sp.playlist_add_items(playlist_id=playlist_id,
                                    items=track_id)

        return add
