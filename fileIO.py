from alertUser import alertUser
import os
import copy

def writeRankingFile(songList, playlistId, currentSongIndex):

    print('creating ranking file...')

    sortedSongList = copy.deepcopy(songList)

    file = open('./ranking.txt', 'w', encoding = "utf-8")

    sortedSongList = calcAvgRankings(sortedSongList)

    sortedSongList.sort(key = lambda song: song['avgRating'], reverse = True)

    for i in range(0, len(sortedSongList)):
        file.write(str(i + 1) + '. ' + sortedSongList[i]['name'] + '\n\t\t')
        if (sortedSongList[i]['viewed'] == True):
            file.write(str(sortedSongList[i]['avgRating'])[0:4] + '\n')
        else:
            file.write('Unrated' + '\n')

    file.close()

    saveRankingProgress(songList, playlistId, currentSongIndex)

    alertUser('Ranking File Created Successfully!', 'A text file called "ranking.txt" has been created in the "saves" folder containing the ranked list of your songs.', 'info')

    print('successfully created ranking file...')

def calcAvgRankings(songList):

    for s in songList:
        s['avgRating'] = ( s['instRating'] + s['lyricsRating'] + s['feelRating']) / 3

    return songList

def saveRankingProgress(songList, playlistId, lastSongIndex):
    try:
        os.mkdir('./saves')
    except FileExistsError:
        pass
    file = open('./saves/' + playlistId + '_rs.txt', 'w', encoding = "utf-8")

    file.write(playlistId + '\n')
    for song in songList:
        file.write(song['link'][31:54] + ',' + str(song['instRating']) + ',' + str(song['lyricsRating']) + ',' + str(song['feelRating']) + '\n' )

    file.write(str(lastSongIndex))

    file.close()

    return

def readRankingsFile(songList, id):

    print('reading saved file...')

    newSongList = []
    songArrayFromFile = []

    # assemble array from file

    file = open('./saves/' + id + '_rs.txt', 'r')
    
    lines = file.readlines()

    for i in range(1, len(lines) - 1):

        ratingCounter = 0
        currentRating = ''
        currInstRating = 0
        currLyricsRating = 0
        currFeelRating = 0

        for c in lines[i][23:]:

            if c != ',' and c != '\n':
                currentRating += c
            else:

                if ratingCounter == 0:
                    currInstRating = int(currentRating)
                elif ratingCounter == 1:
                    currLyricsRating = int(currentRating)
                elif ratingCounter == 2:
                    currFeelRating = int(currentRating)
                ratingCounter += 1
                currentRating = ''

        songArrayFromFile.append({
            'id': lines[i][0:22],
            'instRating': currInstRating,
            'lyricsRating': currLyricsRating,
            'feelRating': currFeelRating
        })

    lastSongIndex = lines[len(lines) - 1][0:len(lines[len(lines) - 1])]

    file.close()

    # iterate through array and iterate through file array and merge

    for s in songList:

        hasBeenAdded = False

        for a in songArrayFromFile:
            if s['id'] == a['id']:
                newSongList.append({
                    'id': s['id'],
                    'name': s['name'],
                    'artist': s['artist'],
                    'link': s['link'],
                    'instRating': a['instRating'],
                    'lyricsRating': a['lyricsRating'],
                    'feelRating': a['feelRating'],
                    'viewed': s['viewed']
                })
                hasBeenAdded = True
                continue
        
        if hasBeenAdded == False:
            newSongList.append({
                'id': s['id'],
                'name': s['name'],
                'artist': s['artist'],
                'link': s['link'],
                'instRating': s['instRating'],
                'lyricsRating': s['lyricsRating'],
                'feelRating': s['feelRating'],
                'viewed': s['viewed']
            })

    print('successfully read saved file...')

    return {
        'songList': newSongList,
        'songIndex': lastSongIndex
    }