import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from configs import CLIENT_ID,CLIENT_SECRET,REDIRECT_URI,SCOPE,username
import datetime
from colours import color
import glob
import os

logsDirectory = os.getcwd()+"/logs"

if not os.path.exists(logsDirectory):
    os.makedirs(logsDirectory)

# Making a GET request
try:
    url = input("Enter Apple Music playlist URL: ")
    r = requests.get(url)

except:
    raise Exception("Error URL is incorrect")

if(r.status_code == 404):
    raise Exception("URL is incorrect, please check if URL is correct")
else:
    print(color.SUCCESS+"Playlist found!    ")
    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')

    trackTitleHTML = soup.findAll('div', class_='songs-list-row__song-name')
    trackArtistsHTML = soup.findAll('div', class_="songs-list-row__by-line svelte-1yo4jst")
    trackArtistItems = []
    tracks = []
    songsToAdd = []

    # Spotify authentication
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI,scope=SCOPE))

    playlist_name = input("Enter a playlist name: ")
    playlist_description = input("Enter a playlist description: ")
    playlist_privacy = input("Playlist Privacy Public/Private (default is private just leave empty):")
    playlistPublicy = False
    if (playlist_privacy.lower() == "public"):
        playlistPublicy = True
    elif (playlist_privacy.lower() == "private"):
        pass
    elif (playlist_privacy.lower() == ""):
        pass
    else:
        raise Exception("Needs to be public or private you entered", playlist_privacy)

    sp.user_playlist_create(user=username, name=playlist_name, public=True, description=playlist_description)

    for item in trackArtistsHTML:
        trackArtistItems.append(item.find_all('a'))

    for i in trackTitleHTML:
        tracks.append(i.string)

    count = 1
    for item in trackArtistItems:
        songsToAdd.append([item[0].string, tracks[count - 1]])
        count += 1

    tracksQuery = []
    notFound = []
    for track in songsToAdd:
        result = sp.search(q="artist:" + track[0] + " track:" + track[1], type="track")
        if (len(result['tracks']['items']) != 0):
            tracksQuery.append(result['tracks']['items'][0]['uri'])
        else:
            print(color.ERROR +"Could not find song", color.KEY + track[1], "by", track[0])
            notFound.append("Could not find song " + track[1] + " by " + track[0])
    
    out_file = open(str(logsDirectory+"/"+datetime.datetime.now().strftime("%a-%d-%b-%Y_%H-%M-%S-%f"))+".txt", "w")
    for missedTrack in notFound:
        out_file.writelines(missedTrack+"\n")
    out_file.close()
    getRecentPlaylist = sp.user_playlists(username)
    playlistID = getRecentPlaylist['items'][0]['id']

    sp.user_playlist_add_tracks(user=username, playlist_id=playlistID, tracks=tracksQuery)
    
    list_of_files = glob.glob(logsDirectory)
    latest_file = max(list_of_files, key=os.path.getctime)

    if(len(notFound)==0):
        print(color.SUCCESS + "All songs added onto your new spotify playlist",playlist_name)
    else:
        print(color.ERROR +"All songs that can't be found have been added to {latest_file} in /logs")