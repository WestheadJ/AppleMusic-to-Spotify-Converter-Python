import requests
from bs4 import BeautifulSoup
from configs import CLIENT_ID,CLIENT_SECRET,REDIRECT_URI,SCOPE,USERNAME
from Colours import color, colorMessage
import os
from SpotifyInterface import SpotifyInterface

# Created custom exception for URL
class InvalidURLException(Exception):
    "Raised when an invalid URL (non Apple Music link) is entered"
    def __init__(self):
        message = """
        Error URL is incorrect!!! This means that it may not contain,
            http://,
            https://,
            apple.music.com,
            /playlist

        OR the URL does not lead to a playlist.
        """
        print(colorMessage(color.ERROR, message))


interface = SpotifyInterface(CLIENT_ID, CLIENT_SECRET, SCOPE, USERNAME, REDIRECT_URI)

logsDirectory = os.getcwd()+"/logs"

if not os.path.exists(logsDirectory):
    os.makedirs(logsDirectory)

url = input("Enter Apple Music playlist URL: ")

# Splits the inputted url into parts: 
# if entered correctly e.g. https://music.apple.com or http://music.apple.com 
# parts = ["https", "", "music.apple.com"] or ["http", "", "music.apple.com"]
parts = url.split("/")

validDomains = ["music.apple.com"]

# // not included in allowed protocols due to them being validated in parts which splits on /
allowedProtocols = ["https:", "http:"]

protocolsOk = parts[0] in allowedProtocols

if not protocolsOk and parts[0] in validDomains:
    url = f"https://{url}"

parts = url.split("/")
protocolsOk = parts[0] in allowedProtocols
domainOk = parts[2] in validDomains and "playlist" in parts

if protocolsOk and domainOk:
    # Making a GET request
    r = requests.get(url)
else:
    raise InvalidURLException

# If page not found
if(r.status_code == 404):
    print("STATUS BAD")
    raise InvalidURLException

print(colorMessage(color.SUCCESS, "Playlist found!"))
# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')

trackTitleHTML = soup.findAll('div', class_='songs-list-row__song-name')
trackArtistsHTML = soup.findAll('div', class_="songs-list-row__by-line svelte-1yo4jst")
trackArtistItems = []
tracks = []
songsToAdd = []

playlist_name = input("Enter a playlist name: ")
playlist_description = input("Enter a playlist description: ")
playlist_privacy = input("Playlist Privacy Public/Private (default is private just leave empty):")

interface.CreatePlaylist(playlist_name,playlist_description,playlist_privacy)

for item in trackArtistsHTML:
    trackArtistItems.append(item.find_all('a'))

for i in trackTitleHTML:
    tracks.append(i.string)

count = 1
for item in trackArtistItems:
    songsToAdd.append([item[0].string, tracks[count - 1]])
    count += 1

interface.AddToPlaylist(songsToAdd)
