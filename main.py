from configs import CLIENT_ID,CLIENT_SECRET,REDIRECT_URI,SCOPE,USERNAME
import os
from SpotifyInterface import SpotifyInterface
from AppleMusicInterface import AppleMusicInterface

spotifyInterface = SpotifyInterface(CLIENT_ID, CLIENT_SECRET, SCOPE, USERNAME, REDIRECT_URI)
appleInterface = AppleMusicInterface()

logsDirectory = os.getcwd()+"/logs"

if not os.path.exists(logsDirectory):
    os.makedirs(logsDirectory)

url = input("Enter Apple Music playlist URL: ")

request = appleInterface.GetPlaylist(url)

songsToAdd = appleInterface.GetSongs(request)

playlist_name = input("Enter a playlist name: ")
playlist_description = input("Enter a playlist description: ")
playlist_privacy = input("Playlist Privacy Public/Private (default is private just leave empty):")

spotifyInterface.CreatePlaylist(playlist_name,playlist_description,playlist_privacy)

spotifyInterface.AddToPlaylist(songsToAdd)
