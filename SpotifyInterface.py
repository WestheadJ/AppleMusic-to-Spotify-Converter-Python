import spotipy
from spotipy.oauth2 import SpotifyOAuth
from colours import color,colorMessage
import datetime
import glob
import os

# Created a custom exception for Privacy input
class PrivacyException(Exception):
    "Raised when the Playlist privacy input is incorrectly entered"
    def __init__(self):
        message = f"You need to have entered public or private as your playlists type\nYou Entered: {self.playlist_privacy}"
        print(colorMessage(color.ERROR, message))

class SpotifyInterface:

    def __init__(self, clientID, clientSecret, scope, username, redirectURI):
        self.username = username
        self.CLIENT_ID = clientID
        self.CLIENT_SECRET = clientSecret
        self.CLIENT_SCOPE = scope
        self.USERNAME = username
        self.REDIRECT_URI = redirectURI
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.CLIENT_ID,client_secret=self.CLIENT_SECRET,redirect_uri=self.REDIRECT_URI,scope=self.CLIENT_SCOPE))
        

    playlist_name = ""
    playlist_description = ""
    playlist_privacy = ""
    playlist_publicy = False

    logsDirectory = os.getcwd() + "/logs"

    def CreatePlaylist(self, playlist_name, playlist_description, playlist_privacy):
        if (playlist_privacy.lower() == "public"):
            self.playlistPublicy = True
        elif (playlist_privacy.lower() == "private"):
            pass
        elif (playlist_privacy.lower() == ""):
            pass
        else:
            raise PrivacyException
        
        self.playlist = self.sp.user_playlist_create(user=self.USERNAME, name=playlist_name, public=playlist_privacy, description=playlist_description)


    def AddToPlaylist(self,tracks):
        tracksQuery = []
        notFound = []
        for track in tracks:
            result = self.sp.search(q="artist:" + track[0] + " track:" + track[1], type="track")
            if (len(result['tracks']['items']) != 0):
                tracksQuery.append(result['tracks']['items'][0]['uri'])
            else:
                print(track)
                print(result)
                print(colorMessage(color.ERROR, "Could not find song"),
                      colorMessage(color.KEY, f"{track[1]} by {track[0]}"))
                notFound.append("Could not find song " + track[1] + " by " + track[0])

        playlistID = self.playlist['id']
        self.sp.playlist_add_items(playlist_id=playlistID, items=tracksQuery, position=None)
        self.LogTracks(notFound)


    def LogTracks(self, tracks):
        out_file = open(
            str(self.logsDirectory + "/" + datetime.datetime.now().strftime("%a-%d-%b-%Y_%H-%M-%S-%f")) + ".txt", "w")
        for missedTrack in tracks:
            out_file.writelines(missedTrack + "\n")
        out_file.close()

        list_of_files = glob.glob(self.logsDirectory)
        latest_file = max(list_of_files, key=os.path.getctime)

        if (len(tracks) == 0):
            print(colorMessage(color.SUCCESS, f"All songs added onto your new spotify playlist {self.playlist_name}"))
        else:
            print(colorMessage(color.ERROR, f"All songs that can't be found have been added to {latest_file} in /logs"))
