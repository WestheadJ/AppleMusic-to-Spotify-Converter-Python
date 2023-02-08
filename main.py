from configs import CLIENT_ID,CLIENT_SECRET,REDIRECT_URI,SCOPE,USERNAME
import time
from SpotifyInterface import SpotifyInterface
from AppleMusicInterface import AppleMusicInterface
import os

# Instantiate the interface objects
spotifyInterface = SpotifyInterface(CLIENT_ID, CLIENT_SECRET, SCOPE, USERNAME, REDIRECT_URI)
appleInterface = AppleMusicInterface()

# Set the logs directory
logsDirectory = os.getcwd()+"/logs"

if not os.path.exists(logsDirectory):
    os.makedirs(logsDirectory)

# Get the URL for the Apple Music Playlist
url = input("Enter Apple Music playlist URL: ")

# Get the playlist - needs to check if the playlist exists
request = appleInterface.GetPlaylist(url)

# If the playlist exists, get all the songs from the playlist
# songsToAdd = appleInterface.GetSongs(request)
#
# choice = input("""Enter the option you want:
# - (1) Create a new playlist and add all songs to it
# - (2) Add songs to an existing playlist:
# - (0) Exit program
# Enter: """)
# submenuCreateOrAdd = True
# while submenuCreateOrAdd:
#     if(int(choice) == 1):
#         print("Creating New Playlist")
#         submenuCreateOrAdd = False
#     elif(int(choice) == 2):
#         print("Adding to a new Playlist")
#         playlists = spotifyInterface.GetUserPlaylist()
#         print("Your Playlists:")
#         time.sleep(0.5)
#         count = 0
#         for item in playlists:
#             count += 1
#             print(str(count) + "-", item[0])
#         choice = input("Enter the number of the playlist you want to add: ")
#         if (choice.isalnum):
#             choice = int(choice) - 1
#         if (choice > len(playlists)):
#             print("Not one of your playlists")
#         if (choice == 0):
#             exit()
#         if (choice < -1):
#             print("Not one of your playlists")
#         else:
#             print("Enter the number of the playlist you want to add!")
#         submenuCreateOrAdd = False
#     elif(int(choice) == 0):
#         exit(0)
#     else:
#         print("Enter an option from the list")
#
#
#
#
# playlist_name = input("Enter a playlist name: ")
# playlist_description = input("Enter a playlist description: ")
# playlist_privacy = input("Playlist Privacy Public/Private (default is private just leave empty):")
#
#
# spotifyInterface.CreatePlaylist(playlist_name,playlist_description,playlist_privacy)
# spotifyInterface.AddToPlaylist(songsToAdd)