from alertUser import alertUser

def extractSpotifyId(link):

    # index 34 to 56

    return link[34:56]

def isLinkValid(playlistLink):
    baseUrl = playlistLink[0:34]
    standardSpotifyBaseUrl = 'https://open.spotify.com/playlist/'
    
    if (baseUrl == standardSpotifyBaseUrl and len(playlistLink[34:56]) == 22):
        return True
    return False