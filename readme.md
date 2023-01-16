# Apple Music Playlist To Spotify Playlist Converter
This is a pyhton script that uses [Spotipy](https://spotipy.readthedocs.io/en/2.22.0/), 
[Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/), 
[requests](https://pypi.org/project/requests/) python libraries and the 
[SpotifyAPI](https://developer.spotify.com/documentation/web-api/) to get the songs from an
Apple Music playlist and add them to a Spotify playlist.

## How does it work?
As stated above it uses 3 main python libaries (```Spotipy```, ```Beautiful Soup``` and ```requests```)
and the [SpotifyAPI](https://developer.spotify.com/documentation/web-api/) to allow this to work.

First it gets a URL (needs to be an Apple Music Playlist to work) it uses the ```requests``` to
```GET``` the HTML contents of the page the URL leads to, in this case the playlist. This is 
because you have to pay for an Apple Music developers license so it lead me to use a 
webscraper which leads onto the next part.

The second step it uses ```Beautiful Soup``` to parse the HTML received by the ```GET``` 
request. I then, still using ```Beautiful Soup``` it finds the ```<div>``` with the song name 
and the artist.

```Spotipy``` then authenticates the user with the SpotifyAPI.Then the user is prompted with 
inputs, it asks for a playlist title, playlist description, and it's privacy. It then creates
the playlist on the users spotify account.

It then loops through ```<div>``` each to get the artist and song name and appends it to an array.
This array is then looped over and added to a new array e.g ```songsToAdd = []``` turns into
```songsToAdd = [["song1","artist1"],["song2","arist2"]]```.

This array is then looped over and each song is then searched using ```Spotipy``` with the song
name and artist the result of said query is then added to an array. However, some song titles aren't
the same on Spotify as they are on Apple Music, so to counter this I check if the result of the 
search is empty if it is, add it to a ```.txt``` file which uses a timestamp as the filename and
doesn't add it to the array, so it stops duplicates. The array is then used to send of ```POST```
request using ```Spotipy``` to add the songs to the playlists.

## How To Use Yourself
Fork/Clone the code or download it as a ```.zip```. In this directory open up a command prompt/terminal
make sure you have ```python 3.8+``` I am using ```python 3.9``` make sure ```pip``` is installed
create a virutal environment using ```venv``` e.g ```python3 -m venv [venv-directoy]``` activate the
environment by using:

#### Linux/Mac 
Activation: ```source [venv-directory]/bin/activate```

Deactivation: ```deactivate```

#### Windows
Activation: ```[my-venv-directory]\Scripts\activate.bat```

Deactivation: ```[my-venv-directory]\Scripts\deactivate.bat``` 

Whilst the environment is active use ```pip install -r requirments.txt``` this should set up the venv
exactly how I have it setup. 

Create a ```configs.py``` and add ```CLIENT_ID```, ```CLIENT_SECRET``` and ```REDIRECT_URI``` from
your [Spotify Developer](https://developer.spotify.com/dashboard/login) dashboard after creating an
app. Then add ```SCOPE = "playlist-modify-public,playlist-modify-private"``` if you want to add you own functionality then look at the (authorization scopes)[https://developer.spotify.com/documentation/general/guides/authorization/scopes/]  and go to your spotify
account to find your ```username``` and add that to ```configs.py```.

To find Apple Music playlist link go to an Apple Music playlist on your iPhone, go to the top right ```...
-> Share Playlist... -> copy``` and paste that to somewhere or in the prompt for the URL.

## Future Updates
- Add to an existing playlist
- Make sure over 100 songs can be added to a playlist (SpotifyAPI states it's not alloweds)
- A website version
- A C# version
