from alertUser import alertUser
from tkinter import *
from tkinter import filedialog
from getSongList import getSongList
from linkHandling import extractSpotifyId, isLinkValid
from fileIO import writeRankingFile, readRankingsFile
import os

playlistUrl = ''
songTitleLabels = []
currentSongIndex = 0
currentScreen = 'home'
playlistId = ''

titleFont = ('Arial', 72)
subtitleFont = ('Arial', 18)
bodyFont = ('Arial', 9)


def keyPressed(e):

    if currentScreen == 'home' and e.keycode == 13:
        submitLink()
        return
    if currentScreen == 'preview' and e.keycode == 13:
        beginRanking()

    return

def submitLink():
    global currentScreen, playlistId

    playlistUrl = linkEntry.get()
    linkEntry.delete(0, len(linkEntry.get()))

    if (isLinkValid(playlistUrl)):
        
        title.grid_remove()
        subtitle.grid_remove()
        linkEntry.grid_remove()
        submitBtn.grid_remove()

        playlistId = extractSpotifyId(playlistUrl)

        previewPlaylist(playlistId)
        currentScreen = 'preview'

    else:
        alertUser('Invalid Link', 'The link you have entered is not a valid Spotify playlist link', 'error')

def previewPlaylist(playlistId):
    global currentScreen
    global songList
    songList = getSongList(playlistId)
    for song in songList:
        songTitleLabels.append(Label(text = '>   ' + song['name'], master = songTable, font = bodyFont))

    Label(text = 'Playlist Preview:', font = subtitleFont).grid(row = 0, column = 0, pady = 10, padx = 50)
    songTable.grid(row = 1, column = 0, ipadx = 50, padx = 10)

    for i in range(0, len(songTitleLabels)):
        if i > 4:
            break
        songTitleLabels[i].grid(column = 0, row = i, sticky = 'W')
    if len(songTitleLabels) > 5:
        Label(text = '...', master = songTable).grid(column = 0, row = 5, sticky = 'W')

    Button(text = 'Begin Ranking', command = beginRanking).grid(row = 2, column = 0, ipadx = 50, padx = 10, pady = 10)

def isDoneRanking():
    for s in songList:
        if s['viewed'] == False:
            return False

    return True

def beginRanking():
    global currentScreen, currentSongIndex, songList, playlistId, lyricsValue, feelValue

    currentScreen = 'ranking'

    def updateRatingLabels(v = 0):
        
        instScaleLabel['text'] = instScale.get()
        lyricsScaleLabel['text'] = lyricsScale.get()
        feelScaleLabel['text'] = feelScale.get()

    def writeRankings():
        global songList, playlistId, currentSongIndex

        songList[currentSongIndex]['instRating'] = instScale.get()
        songList[currentSongIndex]['lyricsRating'] = lyricsScale.get()
        songList[currentSongIndex]['feelRating'] = feelScale.get()

        writeRankingFile(songList, playlistId, currentSongIndex)

    def switchSong(dir):

        global currentSongIndex

        songList[currentSongIndex]['instRating'] = instScale.get()
        songList[currentSongIndex]['lyricsRating'] = lyricsScale.get()
        songList[currentSongIndex]['feelRating'] = feelScale.get()

        if dir == 'prev':
            currentSongIndex -= 1
        elif dir == 'next':
            currentSongIndex += 1
        else:
            print('invalid switchSong dir input')

        if (currentSongIndex >= len(songList)):
            currentSongIndex = 0
        elif (currentSongIndex < 0):
            currentSongIndex = len(songList) - 1

        currentSongTitle['text'] = songList[currentSongIndex]['name']
        songCounter['text'] = str(currentSongIndex + 1) + ' of ' + str(len(songList))
        currentArtist['text'] = songList[currentSongIndex]['artist']

        instScale.set(songList[currentSongIndex]['instRating'])
        lyricsScale.set(songList[currentSongIndex]['lyricsRating'])
        feelScale.set(songList[currentSongIndex]['feelRating'])
        songList[currentSongIndex]['viewed'] = True

        updateRatingLabels()



    try:
        os.mkdir('./saves')
    except FileExistsError:
        pass

    for filename in os.listdir('./saves'):
        f = open('./saves/' + filename, 'r')
        id = f.read(22)
        
        if id == playlistId:

            alertUser('Previous Ranking Found!', 'A previous saved ranking was found in your saved rankings. It will be loaded now.', 'info')



            fileInput = readRankingsFile(songList, id)
            songList = fileInput['songList']
            currentSongIndex = int(fileInput['songIndex'])

        f.close()

    for w in root.winfo_children():
        w.grid_remove()







    artistTitleFrame = Frame()
    scaleFrame = Frame()

    currentSongTitle = Label(text = songList[currentSongIndex]['name'], font = subtitleFont, master = artistTitleFrame)
    songList[currentSongIndex]['viewed'] = True

    currentArtist = Label(text = songList[currentSongIndex]['artist'], font = bodyFont, master = artistTitleFrame, fg = '#888888')


    instLabel = Label(text = 'Instrumentals / Beat', master = scaleFrame, relief = 'sunken')
    lyricsLabel = Label(text = 'Lyrics', master = scaleFrame, relief = 'sunken')
    feelLabel = Label(text = 'Feel', master = scaleFrame, relief = 'sunken')

    global instScale, lyricsScale, feelScale
    instScale = Scale(from_ = 100, to = 0, width = 25, sliderlength = 40, showvalue = 0, resolution = 1, length = 300, master = scaleFrame, command = updateRatingLabels, borderwidth = 2, relief = 'sunken')
    lyricsScale = Scale(from_ = 100, to = 0, width = 25, sliderlength = 40, showvalue = 0, resolution = 1, length = 300, master = scaleFrame, command = updateRatingLabels, borderwidth = 2, relief = 'sunken')
    feelScale = Scale(from_ = 100, to = 0, width = 25, sliderlength = 40, showvalue = 0, resolution = 1, length = 300, master = scaleFrame, command = updateRatingLabels, borderwidth = 2, relief = 'sunken')

    instScaleLabel = Label(text = songList[currentSongIndex]['instRating'], master = scaleFrame)
    lyricsScaleLabel = Label(text = songList[currentSongIndex]['lyricsRating'], master = scaleFrame)
    feelScaleLabel = Label(text = songList[currentSongIndex]['feelRating'], master = scaleFrame)

    instScale.set(songList[currentSongIndex]['instRating'])
    lyricsScale.set(songList[currentSongIndex]['lyricsRating'])
    feelScale.set(songList[currentSongIndex]['feelRating'])

    prevBtn = Button(text = '<<', command = lambda: switchSong('prev'))
    submitBtn = Button(text = 'Submit Playlist Ranking', command = writeRankings)
    nextBtn = Button(text = '>>', command = lambda: switchSong('next'))

    songCounter = Label(text = str(currentSongIndex + 1) + ' of ' + str(len(songList)), font = bodyFont)

    currentSongTitle.grid(row = 0, column = 0)
    currentArtist.grid(row = 1, column = 0)
    artistTitleFrame.grid(row = 0, column = 0, columnspan = 3, pady = 10)

    instLabel.grid(row = 0, column = 0, sticky = 'WE', padx = 20)
    lyricsLabel.grid(row = 0, column = 1, sticky = 'WE', padx = 20)
    feelLabel.grid(row = 0, column = 2, sticky = 'WE', padx = 20)

    instScale.grid(row = 1, column = 0, padx = 50, pady = 10)
    lyricsScale.grid(row = 1, column = 1, padx = 50, pady = 10)
    feelScale.grid(row = 1, column = 2, padx = 50, pady = 10)

    instScaleLabel.grid(row = 2, column = 0, padx = 20)
    lyricsScaleLabel.grid(row = 2, column = 1, padx = 20)
    feelScaleLabel.grid(row = 2, column = 2, padx = 20)

    scaleFrame.grid(row = 1, column = 0, columnspan = 3, pady = 10)

    prevBtn.grid(row = 4, column = 0, pady = 10, ipadx = 20)
    submitBtn.grid(row = 4, column = 1, pady = 10, ipadx = 50)
    nextBtn.grid(row = 4, column = 2, pady = 10, ipadx = 20)

    songCounter.grid(row = 5, column = 0, columnspan = 3, pady = 10)

root = Tk()
root.title('SongRank')
root.bind('<KeyPress>', keyPressed)
root.resizable(False, False)

title = Label(text = 'SongRank', font = ('Arial', 72), bd = 3)
title.grid(row = 0, column = 0, pady = 40)

subtitle = Label(text = 'Enter Playlist Link:', font = ('Arial', 18))
subtitle.grid(row = 1, column = 0, sticky = 'W', padx = 10, pady = 10)

linkEntry = Entry()
linkEntry.grid(row = 2, column = 0, ipadx = 200, padx = 10)

submitBtn = Button(text = 'Begin Ranking', command = submitLink, bd = 2)
submitBtn.grid(row = 3, column = 0, padx = 10, ipadx = 20, pady = 10, sticky = 'E')

songTable = Frame(borderwidth = 2, relief = 'sunken', padx = 5, pady = 5)



root.mainloop()