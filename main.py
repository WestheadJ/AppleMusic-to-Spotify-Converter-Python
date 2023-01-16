import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from configs import CLIENT_ID,CLIENT_SECRET,REDIRECT_URI,SCOPE,USERNAME
import datetime
from Colours import color, colorMessage
import glob
import os
from SpotifyInterface import SpotifyInterface

# Created custom exception for URL
# class InvalidURLException(Exception):
#     "Raised when an invalid URL (non apple music link) is entered"
#     def __init__(self):
#         message = """
#         Error URL is incorrect!!! This means that it may not contain,
#             http://,
#             https://,
#             apple.music.com,
#             /playlist

#         OR the URL does not lead to a playlist.
#         """
#         print(colorMessage(color.ERROR, message))


interface = SpotifyInterface(CLIENT_ID, CLIENT_SECRET, SCOPE, USERNAME, REDIRECT_URI)

# logsDirectory = os.getcwd()+"/logs"

# if not os.path.exists(logsDirectory):
#     os.makedirs(logsDirectory)

# url = input("Enter Apple Music playlist URL: ")

# # Splits the inputted url into parts: 
# # if entered correctly e.g. https://music.apple.com or http://music.apple.com 
# # parts = ["https", "", "music.apple.com"] or ["http", "", "music.apple.com"]
# parts = url.split("/")

# validDomains = ["music.apple.com"]

# # // not included in allowed protocols due to them being validated in parts which splits on /
# allowedProtocols = ["https:", "http:"]

# protocolsOk = parts[0] in allowedProtocols

# if not protocolsOk and parts[0] in validDomains:
#     url = f"https://{url}"

# parts = url.split("/")
# protocolsOk = parts[0] in allowedProtocols
# domainOk = parts[2] in validDomains and "playlist" in parts

# if protocolsOk and domainOk:
#     # Making a GET request
#     r = requests.get(url)
# else:
#     raise InvalidURLException

# # If page not found
# if(r.status_code == 404):
#     print("STATUS BAD")
#     raise InvalidURLException

# print(colorMessage(color.SUCCESS, "Playlist found!"))
# # Parsing the HTML
# soup = BeautifulSoup(r.content, 'html.parser')

# trackTitleHTML = soup.findAll('div', class_='songs-list-row__song-name')
# trackArtistsHTML = soup.findAll('div', class_="songs-list-row__by-line svelte-1yo4jst")
# trackArtistItems = []
# tracks = []
# songsToAdd = []

playlist_name = input("Enter a playlist name: ")
playlist_description = input("Enter a playlist description: ")
playlist_privacy = input("Playlist Privacy Public/Private (default is private just leave empty):")

interface.CreatePlaylist(playlist_name,playlist_description,playlist_privacy)

# interface.AddToPlaylist()

# for item in trackArtistsHTML:
#     trackArtistItems.append(item.find_all('a'))

# for i in trackTitleHTML:
#     tracks.append(i.string)

# count = 1
# for item in trackArtistItems:
#     songsToAdd.append([item[0].string, tracks[count - 1]])
#     count += 1

# tracksQuery = []
# notFound = []
# for track in songsToAdd:
#     result = sp.search(q="artist:" + track[0] + " track:" + track[1], type="track")
#     if (len(result['tracks']['items']) != 0):
#         tracksQuery.append(result['tracks']['items'][0]['uri'])
#     else:
#         print(colorMessage(color.ERROR, "Could not find song"), colorMessage(color.KEY, f"{track[1]} by {track[0]}"))
#         notFound.append("Could not find song " + track[1] + " by " + track[0])

# out_file = open(str(logsDirectory+"/"+datetime.datetime.now().strftime("%a-%d-%b-%Y_%H-%M-%S-%f"))+".txt", "w")
# for missedTrack in notFound:
#     out_file.writelines(missedTrack+"\n")
# out_file.close()
# getRecentPlaylist = sp.user_playlists(username)
# playlistID = getRecentPlaylist['items'][0]['id']

# sp.user_playlist_add_tracks(user=username, playlist_id=playlistID, tracks=tracksQuery)

# list_of_files = glob.glob(logsDirectory)
# latest_file = max(list_of_files, key=os.path.getctime)

# if(len(notFound)==0):
#     print(colorMessage(color.SUCCESS, f"All songs added onto your new spotify playlist {playlist_name}"))
# else:
#     print(colorMessage(color.ERROR, f"All songs that can't be found have been added to {latest_file} in /logs"))
