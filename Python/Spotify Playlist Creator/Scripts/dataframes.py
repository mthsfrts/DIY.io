# Libraries

import pandas as pd
import numpy as np
from auth import SpotifyAuthClient

# Instances
spotify = SpotifyAuthClient()
sp = spotify.auth_obj()


class SpotifyDataFrame:

    # Setting up Class Variables

    def __init__(self):

        self.artist = []
        self.artist_id = []
        self.artist_genres = []

        self.track = []
        self.track_id = []

        self.recommendation_track = []
        self.recommendation_id = []
        self.recommendation_album = []
        self.recommendation_artist = []
        self.recommendation_popularity = []

    # Setting up Methods

    def artist_data(self, artist_search):
        
        for i, j in enumerate(artist_search['artists']['items']):
            self.artist.append(j['name'])
            self.artist_id.append(j['id'])
            self.artist_genres.append(j['genres'][0])

        artist_df = pd.DataFrame(
            {'name': self.artist,
             'Genre': self.artist_genres,
             'ID': self.artist_id
             })

        pd.set_option('display.max_columns', 20)

        return {'artist_df': artist_df,
                'name': self.artist,
                'id': self.artist_id,
                'genres': self.artist_genres}

    def track_data(self, track_search):

        for i, j in enumerate(track_search['tracks']['items']):
            self.track.append(j['name'])
            self.track_id.append(j['id'])

        track_df = pd.DataFrame(
            {'Name': self.track,
             })

        pd.set_option('display.max_columns', 20)

        return {'track_df': track_df, 'id': self.track_id, 'name': self.track,
                }

    def recommendation_data(self, recommendations_search):

        for i, j in enumerate(recommendations_search['tracks']):
            self.recommendation_artist.append(j['artists'][0]['name'])
            self.recommendation_track.append(j['name'])
            self.recommendation_id.append(j['id'])
            self.recommendation_album.append(j['album']['name'])
            self.recommendation_popularity.append(j['popularity'])

        recommendations_df = pd.DataFrame(
            {'Track Name': self.recommendation_track,
             'Album Name': self.recommendation_album,
             'Artist Name': self.recommendation_artist,
             'Track Popularity': self.recommendation_popularity,
             'ID': self.recommendation_id,
             })

        # --- Creating the Analysis DataFrame --- #

        audio_df = pd.DataFrame()

        for id_ in recommendations_df['ID'].iteritems():
            self.recommendation_id = id_[1]

            audio_load_data = sp.audio_features(self.recommendation_id)

            audio_set_df = pd.DataFrame(audio_load_data, index=[0])

            audio_df = pd.concat([audio_df, audio_set_df])

        merge_df = recommendations_df.merge(audio_df, left_on='ID', right_on='id')

        # --- Load new values into merged DataFrame --- #

        # New Key and Mode Values #
        key_conditions = [
            (merge_df['key'] == 0),
            (merge_df['key'] == 1),
            (merge_df['key'] == 2),
            (merge_df['key'] == 3),
            (merge_df['key'] == 4),
            (merge_df['key'] == 5),
            (merge_df['key'] == 6),
            (merge_df['key'] == 7),
            (merge_df['key'] == 8),
            (merge_df['key'] == 9),
            (merge_df['key'] == 10),
            (merge_df['key'] == 11),
        ]

        key_values = ['C', 'D-flat', 'D',
                      'E-flat', 'E', 'F',
                      'F-sharp', 'G', 'A-Flat',
                      'A', 'B-flat', 'B']

        merge_df['key.'] = np.select(key_conditions, key_values, default=None)

        merge_df['mode.'] = np.where(merge_df['mode'] == 1, 'major', 'minor')

        # Camelot Values #

        camelot_conditions = [
            (merge_df['key.'] == 'C') & (merge_df['mode'] == 1),
            (merge_df['key.'] == 'C') & (merge_df['mode'] == 0),
            (merge_df['key.'] == 'D-flat') & (merge_df['mode'] == 1),
            (merge_df['key.'] == 'D-flat') & (merge_df['mode'] == 0),
            (merge_df['key.'] == 'D') & (merge_df['mode'] == 1),
            (merge_df['key.'] == 'D') & (merge_df['mode'] == 0),
            (merge_df['key.'] == 'E-flat') & (merge_df['mode'] == 1),
            (merge_df['key.'] == 'E-flat') & (merge_df['mode'] == 0),
            (merge_df['key.'] == 'E') & (merge_df['mode'] == 1),
            (merge_df['key.'] == 'E') & (merge_df['mode'] == 0),
            (merge_df['key.'] == 'F') & (merge_df['mode'] == 1),
            (merge_df['key.'] == 'F') & (merge_df['mode'] == 0),
            (merge_df['key.'] == 'F-sharp') & (merge_df['mode'] == 1),
            (merge_df['key.'] == 'F-sharp') & (merge_df['mode'] == 0),
            (merge_df['key.'] == 'G') & (merge_df['mode'] == 1),
            (merge_df['key.'] == 'G') & (merge_df['mode'] == 0),
            (merge_df['key.'] == 'A-Flat') & (merge_df['mode'] == 1),
            (merge_df['key.'] == 'A-Flat') & (merge_df['mode'] == 0),
            (merge_df['key.'] == 'A') & (merge_df['mode'] == 1),
            (merge_df['key.'] == 'A') & (merge_df['mode'] == 0),
            (merge_df['key.'] == 'B-flat') & (merge_df['mode'] == 1),
            (merge_df['key.'] == 'B-flat') & (merge_df['mode'] == 0),
            (merge_df['key.'] == 'B') & (merge_df['mode'] == 1),
            (merge_df['key.'] == 'B') & (merge_df['mode'] == 0)
        ]
        camelot_values = ['8B', '5A',
                          '3B', '12A',
                          '10B', '7A',
                          '5B', '2A',
                          '12B', '9A',
                          '7B', '4A',
                          '2B', '11A',
                          '9B', '6A',
                          '4B', '1A',
                          '11B', '8A',
                          '6B', '3A',
                          '1B', '10A'
                          ]

        merge_df['Camelot'] = np.select(camelot_conditions, camelot_values, default=None)

        # New Bpm Values #

        bpm_conditions = [(merge_df['tempo'] <= 79),
                          (merge_df['tempo'] <= 129),
                          (merge_df['tempo'] >= 130)
                          ]

        bpm_values = ('Slow', 'Medium', 'Fast')

        merge_df['BPM'] = np.select(bpm_conditions, bpm_values, default=None)

        # New Valence Values #

        valence_conditions = [(merge_df['valence'] <= 0.2),
                              (merge_df['valence'] <= 0.4),
                              (merge_df['valence'] <= 0.6),
                              (merge_df['valence'] <= 0.8),
                              (merge_df['valence'] > 0.8)]

        valence_values = ('Melancholic', 'Sad', 'Optimistic', 'Happy', 'Ecstatic')

        merge_df['Mood'] = np.select(valence_conditions, valence_values, default=None)

        # New Energy Values #

        energy_conditions = [(merge_df['energy'] <= 0.2),
                             (merge_df['energy'] <= 0.4),
                             (merge_df['energy'] <= 0.6),
                             (merge_df['energy'] <= 0.8),
                             (merge_df['energy'] > 0.8)]

        energy_values = ('Dull', 'Detached', 'Calm', 'Emphatic', 'Excited')

        merge_df['Feel'] = np.select(energy_conditions, energy_values, default=None)

        # New Bpm Values #

        pop_conditions = [(merge_df['Track Popularity'] <= 35),
                          (merge_df['Track Popularity'] <= 70),
                          (merge_df['Track Popularity'] > 70)
                          ]

        pop_values = ('Low', 'Good', 'High')

        merge_df['Streams'] = np.select(pop_conditions, pop_values, default=None)

        # Final DataFrame #

        final_df = merge_df[['Track Name', 'Album Name',
                             'Artist Name', 'Streams',
                             'Feel', 'Mood',
                             'BPM', 'Camelot']]

        pd.set_option('display.max_columns', 20)

        return {'recommendations': final_df,
                'merge': merge_df,
                'id': merge_df['ID']}
