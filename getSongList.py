import spotipy
from spotipy import SpotifyClientCredentials
from spotipy import client

SPOTIPY_CLIENT_ID = 'd2b141136bb14f7eb7cf893d54a460b7'
SPOTIPY_CLIENT_SECRET = '1e0845c19e584488bf6c571285e800fa'

def getSongList(playlistId):

    print('retrieving songs...')

    # need to retrieve the songs external link, the name, the artist, set all of the initial ratings to 0, set 'viewed' to false

    songs = []

    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id = SPOTIPY_CLIENT_ID, client_secret = SPOTIPY_CLIENT_SECRET))

    counter = 0
    while True:

        response = spotify.playlist_tracks(playlistId, offset = counter * 100)

        for track in response['items']:
            songs.append({
                'name': track['track']['name'],
                'artist': track['track']['artists'][0]['name'],
                'link': track['track']['external_urls']['spotify'],
                'id': track['track']['id'],
                'instRating': 0,
                'lyricsRating': 0,
                'feelRating': 0,
                'viewed': False
            })

        if(len(response['items']) < 100):
            break

        counter += 1

    print('successfully retrieved songs...')

    return songs