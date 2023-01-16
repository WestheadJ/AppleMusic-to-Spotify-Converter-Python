import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Created a custom exception for Privacy input
class PrivacyException(Exception):
    "Raised when the Playlist privacy input is incorrectly entered"
    def __init__(self):
        message = f"You need to have entered public or private as your playlists type\nYou Entered: {playlist_privacy}"
        print(colorMessage(color.ERROR, message))

class SpotifyInterface:

    def __init__(self,clientID,clientSecret,scope,username,redirectURI):
        self.username = username
        self.CLIENT_ID = clientID
        self.CLIENT_SECRET = clientSecret
        self.CLIENT_SCOPE = scope
        self.USERNAME = username
        self.REDIRECT_URI = redirectURI

    playlist_name = ""
    playlist_description = ""
    playlist_privacy = ""
    playlist_publicy = False

    def CreatePlaylist(self,playlist_name,playlist_description,playlist_privacy):
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.CLIENT_ID,client_secret=self.CLIENT_SECRET,redirect_uri=self.REDIRECT_URI,scope=self.CLIENT_SCOPE))
        if (playlist_privacy.lower() == "public"):
            playlistPublicy = True
        elif (playlist_privacy.lower() == "private"):
            pass
        elif (playlist_privacy.lower() == ""):
            pass
        else:
            raise PrivacyException
        
        sp.user_playlist_create(user=self.USERNAME, name=playlist_name, public=playlist_privacy,description=playlist_description)
