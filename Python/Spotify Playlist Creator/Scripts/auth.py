# 1 Libraries

import spotipy
from spotipy.oauth2 import SpotifyOAuth


# 2 Setting up the Auth Flow

class SpotifyAuthClient:

    def __init__(self):
        with open('Creds/Client_id.txt', 'r') as cid:
            self.client_id = cid.read()

        with open('Creds/Client_Secret.txt', 'r') as cid_secret:
            self.client_secret = cid_secret.read()

        self.redirect_uri = 'https://www.google.com/'

        self.scope = 'user-read-private playlist-modify-public playlist-modify-private playlist-read-private'

        self.token = SpotifyOAuth(client_id=self.client_id,
                                  client_secret=self.client_secret,
                                  redirect_uri=self.redirect_uri,
                                  scope=self.scope)

    def auth_obj(self):
        sp = spotipy.Spotify(auth_manager=self.token)
        return sp
