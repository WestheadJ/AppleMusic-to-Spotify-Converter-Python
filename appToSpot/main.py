import requests
from bs4 import BeautifulSoup

# Making a GET request
r = requests.get('https://music.apple.com/gb/playlist/untitled-playlist/pl.u-9N9LX8yI1amWkjA')

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')

trackTitleHTML = soup.findAll('div', class_='songs-list-row__song-name')
trackArtistsHTML = soup.findAll('div', class_="songs-list-row__by-line svelte-1yo4jst")
trackArtistItems = []
tracks = []

for item in trackArtistsHTML:
    print(item.find_all('a'))
    for artists in item.find_all(('a')):
        print(artists)
    # trackArtistItems.append(item.find_all('a').text)

print(trackArtistItems)

# count = 0
# for i in trackTitleHTML:
#     tracks.append([i.text,0])
#
# count = 0
# for item in trackArtistsHTML:
#     trackArtistItems.append(item.find_all('a'))

