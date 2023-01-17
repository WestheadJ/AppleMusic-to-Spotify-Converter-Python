import requests
from colours import color,colorMessage
from bs4 import BeautifulSoup

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

class AppleMusicInterface:
    playlistTrackTitles = []
    playlistTrackArtists = []

    def GetPlaylist(self,URL):
        # Splits the inputted url into parts:
        # if entered correctly e.g. https://music.apple.com or http://music.apple.com
        # parts = ["https", "", "music.apple.com"] or ["http", "", "music.apple.com"]
        parts = URL.split("/")

        validDomains = ["music.apple.com"]

        # // not included in allowed protocols due to them being validated in parts which splits on /
        allowedProtocols = ["https:", "http:"]

        protocolsOk = parts[0] in allowedProtocols

        if not protocolsOk and parts[0] in validDomains:
            URL = f"https://{URL}"

        parts =URL.split("/")
        protocolsOk = parts[0] in allowedProtocols
        domainOk = parts[2] in validDomains and "playlist" in parts

        if protocolsOk and domainOk:
            # Making a GET request
            request = requests.get(URL)
        else:
            raise InvalidURLException

        # If page not found
        if (request.status_code == 404):
            print("STATUS BAD")
            raise InvalidURLException
        else:
            print(colorMessage(color.SUCCESS, "Playlist found!"))
            return request

    def GetSongs(self,request):
        # Parsing the HTML
        soup = BeautifulSoup(request.content, 'html.parser')

        # List Comprehension: Same as using:
        # for item in someList:
        #   otherList.append(item.something)

        trackTitleHTML = soup.findAll('div', class_='songs-list-row__song-name')
        self.playlistTrackTitles = [item.string for item in trackTitleHTML]

        trackArtistsHTML = soup.findAll('div', class_="songs-list-row__by-line svelte-1yo4jst")
        self.playlistTrackArtists = [item.find_all('a') for item in trackArtistsHTML]

        songsToAdd = []
        count = 0
        for item in self.playlistTrackArtists:
            songsToAdd.append([item[0].string, self.playlistTrackTitles[count]])
            count += 1

        return songsToAdd