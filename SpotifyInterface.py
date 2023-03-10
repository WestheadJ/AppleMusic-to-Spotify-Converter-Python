import spotipy
from spotipy.oauth2 import SpotifyOAuth
from colours import color,colorMessage
import datetime
import glob
import os
import re

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1/'

# Created a custom exception for Privacy input
class PrivacyException(Exception):
    "Raised when the Playlist privacy input is incorrectly entered"
    def __init__(self):
        message = f"You need to have entered public or private as your playlists type\nYou Entered: {self.playlist_privacy}"
        print(colorMessage(color.ERROR, message))

class PlaylistNotGiven(Exception):
    """Raised when there is no ID to be found"""
    def __init__(self):
        message = f"No ID has been set or the createdPlaylist isn't a boolean value, either set the ID by the most recently created playlist or through a current playlist ID"
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
        """Used to create a playlist for the user"""
        if (playlist_privacy.lower() == "public"):
            self.playlistPublicy = True
        elif (playlist_privacy.lower() == "private"):
            pass
        elif (playlist_privacy.lower() == ""):
            pass
        else:
            raise PrivacyException
        
        self.playlist = self.sp.user_playlist_create(user=self.USERNAME, name=playlist_name, public=playlist_privacy, description=playlist_description)

    def clean_string(self, input_string):
        # Remove parentheses and their contents
        output_string = re.sub(r'\([^)]*\)', '', input_string)
        # Remove spaces before and after remaining text
        output_string = output_string.strip()
        return output_string

    def AddToPlaylist(self,tracks,createdPlaylist=True,playlist_id=""):
        """Used to add songs to the set playlist. Takes tracks and createdPlaylist (is it a new playlist) as parameters default is True, if it's to a pre-existing playlist then needs to be set to False"""

        tracksQuery = []
        notFound = []
        found = []

        if createdPlaylist == True:
            playlistID = self.playlist['id']
        elif createdPlaylist == False:
            playlistID = playlist_id
        else:
            raise PlaylistNotGiven     
        
        for track in tracks:
            result = self.sp.search(q="artist:" + track[0] + " track:" + track[1], type="track")
            if (len(result['tracks']['items']) != 0):
                tracksQuery.append(result['tracks']['items'][0]['uri'])
                print(colorMessage(color.SUCCESS, "Found the song: "),colorMessage(color.KEY,f"{track[1]} by {track[0]}"))
                found.append(f"Found song {track[1]} by {track[0]}")
            else:
                print(colorMessage(color.ERROR, "Could not find song"),
                      colorMessage(color.KEY, f"{track[1]} by {track[0]}"))
                result_alt = self.sp.search(q="artist:" + track[0] + " track:" + self.clean_string(track[1]), type="track")
                if (len(result_alt['tracks']['items']) != 0):
                    decision = input('Possible Result: ' +
                                    result_alt['tracks']['items'][0]['name'] +
                                    ' by ' + result_alt['tracks']['items'][0]['artists'][0]['name'] +
                                    '\nType y to confirm\n')

                    if decision == 'y':
                         tracksQuery.append(result_alt['tracks']['items'][0]['uri'])
                    else:
                         notFound.append("Could not find song " + track[1] + " by " + track[0])

        if playlistID == "":
            raise PlaylistNotGiven
        else:
            self.sp.playlist_add_items(playlist_id=playlistID, items=tracksQuery)
            self.LogTracks(notFound,found)

    def LogTracks(self,unfoundTracks,foundTracks):
        """Used to log tracks that it can't find on spotify"""
        out_file = open(
            str(self.logsDirectory + "/" + datetime.datetime.now().strftime("%a-%d-%b-%Y_%H-%M-%S-%f")) + ".txt", "w")
        out_file.writelines("***** Songs not found *****\n")
        for missedTrack in unfoundTracks:
            out_file.writelines(missedTrack + "\n")
        out_file.writelines("***** ___END___ *****\n")
        out_file.writelines("***** Songs found *****\n")
        for trackFound in foundTracks:
            out_file.writelines(trackFound+"\n")
        out_file.writelines("***** ___END___ *****\n")
        out_file.close()

        list_of_files = glob.glob(self.logsDirectory)
        latest_file = max(list_of_files, key=os.path.getctime)

        if (len(unfoundTracks) == 0):
            print(colorMessage(color.SUCCESS, f"All songs added onto your new spotify playlist {self.playlist_name}"))
        else:
            print(colorMessage(color.ERROR, f"All songs that can't be found have been added to {latest_file} in /logs"))

    def GetUserPlaylist(self):
        """Used to get the users playlists"""

        playlists = []
        usersPlaylists = self.sp.user_playlists(self.username)

        count = 0
        for item in usersPlaylists['items']:
            count += 1
            playlists.append([item['name'],item['id']])

        # The request query returns a dictionary with the key 'next' and the value gives back the offset and the limit
        # needed to get the rest of the playlists

        while (usersPlaylists['next'] != None):
            parameters = usersPlaylists['next'].split('?')[1]
            splitParameters = parameters.split('&')
            offset = splitParameters[0].split("=")[1]
            limit = splitParameters[1].split('=')[1]
            usersPlaylists = self.sp.user_playlists(self.username,limit,offset)
            for item in usersPlaylists['items']:
                count += 1
                playlists.append([item['name'],item['id']])

        return playlists
