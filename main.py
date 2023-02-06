from configs import CLIENT_ID,CLIENT_SECRET,REDIRECT_URI,SCOPE,USERNAME
import time
from SpotifyInterface import SpotifyInterface
from AppleMusicInterface import AppleMusicInterface
import os

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
print(songsToAdd)

spotifyInterface.AddToPlaylist(songsToAdd)


playlists = spotifyInterface.GetUserPlaylist()
print("Your Playlists:")
time.sleep(0.5)
count = 0
for item in playlists:
    count += 1
    print(str(count)+"-", item[0])
choice = input("Enter the number of the playlist you want to add: ")
if(choice.isalnum):
    choice = int(choice) - 1
if(choice > len(playlists)):
    print("Not one of your playlists")
if(choice == 0):
    exit()
if(choice < -1):
    print("Not one of your playlists")
