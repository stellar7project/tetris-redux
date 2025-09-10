'''Version 2.4'''
import sys
from tetrisAssets import *

optionList = ('graphics', 'sound', 'controls', 'gameplay')

#v2.4 RESOLUTIONS
resolutions = pygame.display.list_modes(0, FULLSCREEN) #|HWSURFACE|DOUBLEBUF)
if resolutions != -1:
    resOpts = []
    i = 0
    while i < len(resolutions):
        if resolutions[i][0] > VideoInfo.current_w:
            resolutions.pop(i)
        else:
            resOpts.append(str(resolutions[i][0])+' x '+str(resolutions[i][1]))
            i += 1
    if (VideoInfo.current_w, VideoInfo.current_h) not in resolutions:
        resolutions.insert(0, (VideoInfo.current_w, VideoInfo.current_h))
        resOpts.insert(0, str(VideoInfo.current_w)+' x '+str(VideoInfo.current_h))
else:
    resOpts = [str(VideoInfo.current_w)+' x '+str(VideoInfo.current_h)]
    resolutions = [(VideoInfo.current_w, VideoInfo.current_h)]

#v2.4 Default to monitor's resolution
iRes = resolutions.index((VideoInfo.current_w, VideoInfo.current_h))

bWindowed = False
#bDropFX = True
colourScheme = 8                #v2.5 RANDOM SCHEME
backdropIndex = len(backdrops)  #v2.5 RANDOM BACKDROP
SCREENMODE = ('FULLSCREEN', 'WINDOWED')
TOGGLE = ('OFF', 'ON')
DROPMODE = ('INSTANT', 'HOLD KEY')
PLAYBACK = ('SHUFFLED', 'SINGLE', 'ORDERED')

playbackMode = 0
soundVolume = 100
musicVolume = 100
NEXT_TRACK = 26
bPlayMusic = False
bPanMusic = False
PAN_TRACK = 27
pygame.mixer.music.set_endevent(NEXT_TRACK)

leftKey = K_LEFT
rightKey = K_RIGHT
rotateKey = K_UP
dropKey = K_DOWN
bombKey = K_RSHIFT

startLevel = 0
numBombs = 0
dropMode = 0
endLevel = 35

mainMenu = []
optsMenu = []
bUpdateMenu = False

closeRect = None
#xColor = outlineColors[colorScheme]

#v2.4
cursorColor = WHITE
bFlashUp = False
FV = 0

L_Rect = {
    'render': None,
    'rect': None,
    'select': False
}
R_Rect = {
    'render': None,
    'rect': None,
    'select': False
}

def InitMain(centerX):
    offset = blockSize//12
    if offset < 2:
        offset += 1
    mainMenu.clear()
    restart = font.render('RESTART', True, WHITE)
    restartRect = restart.get_rect(center=(centerX, int(blockSize*2.0)+offset))
    options = font.render('OPTIONS', True, WHITE)
    optionsRect = options.get_rect(center=(centerX, int(blockSize*4.0)+offset))
    main = font.render('BACK TO TITLE', True, WHITE)
    mainRect = main.get_rect(center=(centerX, int(blockSize*6.0)+offset))
    exitGame = font.render('EXIT GAME', True, WHITE)
    exitRect = exitGame.get_rect(center=(centerX, int(blockSize*8.0)+offset))
    mainMenu.append([restart, restartRect])
    mainMenu.append([options, optionsRect])
    mainMenu.append([main, mainRect])
    mainMenu.append([exitGame, exitRect])

    return (
        restartRect.centery - offset, 
        optionsRect.centery - offset, 
        mainRect.centery - offset, 
        exitRect.centery - offset
        )

def GameMenu(DISPLAY, GRID, gOption):
    global option, bUpdateMenu
    global closeRect, xColor

    menuWidth = GRID.get_rect().width
    menuHeight = blockSize*10
    MENU = pygame.Surface((menuWidth, menuHeight))
    menuRect = MENU.get_rect(center=(DISPLAY.get_rect().width//2, DISPLAY.get_rect().height//2)) #+ int(blockSize*1.5)))
    #gridRect = GRID.get_rect(center=(DISPLAY.get_rect().width//2, DISPLAY.get_rect().height//2))

    c = 0
    #cursor = font.render('>', True, YELLOW)
    cursorPos = InitMain(menuWidth//2)
    cursorPosRect = Rect(0,0, blockSize*10, blockSize+blockSize//2)
    cursorPosRect.centerx = menuRect.left + menuWidth//2
    cursorPosRects = []
    for i in range(len(cursorPos)):
        cursorPosRect.centery = menuRect.top + cursorPos[i]
        cursorPosRects.append(cursorPosRect.copy())
    cursorPosRect.center = (menuWidth//2, cursorPos[0])
    #cursorPosRect = cursor.get_rect(center=(menuWidth//2-int(blockSize*3.5), cursorPos[c]))

    closeRect = Rect(0, 0, blockSize, blockSize)
    closeRect.center = (menuRect.right-blockSize//2, menuRect.top+blockSize//2)
    mousePos = pygame.mouse.get_pos()
    if IsMouseInCloseRect(mousePos):
        xColor = WHITE
    else:
        xColor = outlineColors[colorScheme]

    bUpdateMenu = True
    
    option = gOption
    if option == 'options':
        InitOptions(blockSize/48, menuWidth//2, 0)
        SetOptionRects(menuRect)
        c = 1
    while True:
        gOption = option
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if option == '':
                    if event.key == K_ESCAPE:
                        pygame.mixer.Sound.play(ts_drop)
                        closeRect = None
                        return 'resume'
                    
                    elif event.key == K_UP:
                        pygame.mixer.Sound.play(ts_move)
                        bUpdateMenu = True
                        if c > 0:
                            c -= 1
                        else:
                            c = 3
                    elif event.key == K_DOWN:
                        pygame.mixer.Sound.play(ts_move)
                        bUpdateMenu = True
                        if c < 3:
                            c += 1
                        else:
                            c = 0

                    elif event.key == K_RETURN:
                        bUpdateMenu = True
                        if c == 0:
                            pygame.mixer.Sound.play(ts_smashing)
                            closeRect = None
                            return 'restart'
                        elif c == 1:
                            pygame.mixer.Sound.play(ts_set)
                            option = 'options'
                            InitOptions(blockSize/48, menuWidth//2, 0)
                            SetOptionRects(menuRect)
                        elif c == 2:
                            pygame.mixer.Sound.play(ts_break)
                            return 'main'
                        elif c == 3:
                            pygame.quit()
                            sys.exit()
                else:
                    option = Option(event.key)
            
            elif event.type == MOUSEMOTION:
                if option == '':
                    mp = MouseMenuControl(cursorPosRects, c)
                    if mp != -1:
                        c = mp
                else:
                    MouseMenuControl([], -1)
                
            elif event.type == MOUSEBUTTONDOWN:
                if option == '':
                    mousePos = pygame.mouse.get_pos()
                    if( event.button == 1
                    and mousePos[0] > cursorPosRects[c].left and mousePos[0] < cursorPosRects[c].right 
                    and mousePos[1] > cursorPosRects[c].top and mousePos[1] < cursorPosRects[c].bottom ):
                        bUpdateMenu = True
                        if c == 0:
                            pygame.mixer.Sound.play(ts_smashing)
                            closeRect = None
                            return 'restart'
                        elif c == 1:
                            pygame.mixer.Sound.play(ts_set)
                            option = 'options'
                            InitOptions(blockSize/48, menuWidth//2, 0)
                            SetOptionRects(menuRect)
                        elif c == 2:
                            pygame.mixer.Sound.play(ts_break)
                            return 'main'
                        elif c == 3:
                            pygame.quit()
                            sys.exit()
                    elif event.button == 3 or event.button == 1 and IsMouseInCloseRect(mousePos):
                        pygame.mixer.Sound.play(ts_drop)
                        closeRect = None
                        return 'resume'
                    '''elif( mousePos[0] < menuRect.left or mousePos[0] > menuRect.right
                        or mousePos[1] < menuRect.top or mousePos[1] > menuRect.bottom ):'''
                else:
                    option = MouseOptionSelect(event.button)

            elif event.type == NEXT_TRACK:
                PlayNextTrack(False)

            elif event.type == PAN_TRACK:
                SetPanMusic(True)
                pygame.time.set_timer(PAN_TRACK, 0)

            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
                
        
        if option == 'sound' and bPanMusic:
            bUpdateMenu = True
        if bUpdateMenu:
            MENU.fill(colorList[colorScheme])
            pygame.draw.rect(MENU, outlineColors[colorScheme], MENU.get_rect(), winThick)
            if closeRect != None:
                DrawX(MENU, menuRect)
            bUpdateMenu = False
            if option == '':
                if gOption != option:
                    gOption = option
                    InitMain(menuWidth//2)
                cursorPosRect.centery = cursorPos[c]
                menuList = ('RESTART', 'OPTIONS', 'BACK TO TITLE', 'EXIT GAME')
                for i in range(len(mainMenu)):
                    if c == i:
                        fontColor = outlineColors[colorScheme]
                    else:
                        fontColor = WHITE
                    mainMenu[i][0] = font.render(menuList[i], True, fontColor)
                DisplayMainMenu(MENU, len(mainMenu))
                #MENU.blit(cursor, cursorPosRect)
                DISPLAY.blit(MENU, menuRect)
            else:
                OptionsMenu(MENU)
                DISPLAY.blit(MENU, menuRect)
                if option in optionList:
                    OptionMenu(DISPLAY, option=='sound')
                elif option != 'options':
                    return option
        
        FlashCursor()
        if option == '':
            pygame.draw.rect(MENU, cursorColor, cursorPosRect, winThick) #v2.4
            DISPLAY.blit(MENU, menuRect)
        elif option == 'options':
            DrawCursor(DISPLAY, MENU, menuRect)
        else:
            DrawCursor(DISPLAY, OPTIONMENU, optionMenuRect)

        pygame.display.flip()    
        pygame.time.Clock().tick(30)

#v2.4
def FlashCursor():
    global bFlashUp, FV, cursorColor
    if bFlashUp:
        if FV > 0:
            FV -= 1
        else:
            bFlashUp = False
    else:
        if FV < 5:
            FV += 1
        else:
            bFlashUp = True
    cursorColor = (
        outlineColors[colorScheme][0] - (outlineColors[colorScheme][0]-outlineColors[colorScheme][0]//2)*FV//5,
        outlineColors[colorScheme][1] - (outlineColors[colorScheme][1]-outlineColors[colorScheme][1]//2)*FV//5,
        outlineColors[colorScheme][2] - (outlineColors[colorScheme][2]-outlineColors[colorScheme][2]//2)*FV//5
    )
#v2.4
def getCursorColor():
    return cursorColor
#v2.4
def getColorScheme():
    return colorScheme

def DrawCursor(DISPLAY, MENU, menuRect):
    pygame.draw.rect(MENU, cursorColor, cPosRect, winThick) #v2.4
    DISPLAY.blit(MENU, menuRect)

def DisplayMainMenu(MENU, numItems):
    for i in range(numItems):
        MENU.blit(mainMenu[i][0], mainMenu[i][1])

def DisplayOptsMenu(MENU, numItems):
    for i in range(numItems):
        MENU.blit(optsMenu[i][0], optsMenu[i][1])
        MENU.blit(optsMenu[i][2], optsMenu[i][3])

def GeneratePlayList():
    trackList = musicList.copy()
    trackList.pop(trackList.index(playList[0]))
    playList.clear() #v2.4
    while trackList != []:
        r = randint(0, len(trackList)-1)
        playList.append(trackList[r])
        trackList.pop(r)

def PlayNextTrack(bCoerce):
    global bPlayMusic

    if musicTrack == 0:
        if bPlayMusic:
            bPlayMusic = False
            pygame.mixer.music.stop()
            #pygame.mixer.music.set_endevent()
        return False

    if bCoerce:
        if playbackMode == 0: #v2.4
            GeneratePlayList()

        if musicTrack > len(musicList): #v2.5 RANDOM TRACK
            track = randint(0, len(musicList)-1)
        else:
            track = musicTrack-1
        if musicList[track] in playList:
            playList.pop(playList.index(musicList[track]))
        playList.insert(0, musicList[track])

    elif playbackMode == 2: #v2.3
        if bPlayMusic:
            nextIndex = musicList.index(playList[0]) + 1
            if nextIndex == len(musicList):
                nextIndex = 0
            playList.pop(0)
            playList.insert(0, musicList[nextIndex])
            
    elif playbackMode == 0 and len(musicList) > 1: #v2.3
        if len(playList) == 1:
            GeneratePlayList()
        else:
            playList.pop(0)
    
    bPlayMusic = True
    pygame.mixer.music.load("music/" + playList[0])
    pygame.mixer.music.play()
    #pygame.mixer.music.set_endevent(NEXT_TRACK)
    #if len(musicList) > 1:
    #    playList.pop(0)

def SetSoundVolume(v):
    ts_move.set_volume(v)
    ts_rotate.set_volume(v)
    ts_set.set_volume(v)
    ts_drop.set_volume(v)
    ts_break.set_volume(v)
    ts_charge.set_volume(v)
    ts_smashing.set_volume(v)
    ts_endsmash.set_volume(v)
    ts_gameover.set_volume(v)
    ts_tetris[0].set_volume(v)
    ts_tetris[1].set_volume(v)
    ts_tetris[2].set_volume(v)
    ts_tetris[3].set_volume(v)
    ts_tetris[4].set_volume(v)
    ts_clinks[0].set_volume(v)
    ts_clinks[1].set_volume(v)
    ts_clinks[2].set_volume(v)
    ts_whoosh[0].set_volume(v)
    ts_whoosh[1].set_volume(v)
    ts_disintegrate[0].set_volume(v)
    ts_disintegrate[1].set_volume(v)
    ts_blast[0].set_volume(v)
    ts_blast[1].set_volume(v)
    light_noise.set_volume(v)
    arcing.set_volume(v)

def GetMusicList():
    global musicList
    return musicList
    
def GetSound(contents):
    global soundVolume, musicVolume, playbackMode, musicTrack
    global musicList, playList

    if os.path.exists('music'):
        musicList = os.listdir('music')
        if musicList != []:
            musicTrack = len(musicList)+1 #v2.5 RANDOM TRACK
            playList = [musicList[randint(0,len(musicList)-1)]]
        else:
            musicTrack = 0
    else:
        musicList = []
        musicTrack = 0

    if '[AUDIO]\n' in contents:
        k = contents.index('[AUDIO]\n')
        soundVolume = int(contents[k+1][contents[k+1].index('=')+1:len(contents[k+1])])
        musicVolume = int(contents[k+2][contents[k+2].index('=')+1:len(contents[k+2])])
        playbackMode = int(contents[k+3][contents[k+3].index('=')+1:len(contents[k+3])])
        musicTrack = int(contents[k+4][contents[k+4].index('=')+1:len(contents[k+4])])
        if musicTrack > len(musicList)+1: #v2.5 RANDOM TRACK
            musicTrack = len(musicList)+1
            SaveSettings('AUDIO')
    else:
        contents.append('[AUDIO]\n')
        contents.append('soundVolume=' + str(soundVolume) +'\n')
        contents.append('musicVolume=' + str(musicVolume) +'\n')
        contents.append('playbackMode=' + str(playbackMode) +'\n')
        contents.append('musicTrack=' + str(musicTrack) +'\n')
        f = open('tetris.ini', 'w+')#, encoding="utf-8")
        for i in range(len(contents)):
            f.write(contents[i])
        f.close()
        
    pygame.mixer.music.set_volume(float(musicVolume/100))
    SetSoundVolume(float(soundVolume/100))
    return (soundVolume, musicVolume, musicTrack)

#onLoad = True #v2.5
def GetGraphics(contents):
    global iRes, bWindowed, colourScheme, colorScheme, backdropIndex, backdrop
    global onLoad
    if '[VIDEO]\n' in contents:
        k = contents.index('[VIDEO]\n')
        resX = int(contents[k+1][contents[k+1].index('=')+1:len(contents[k+1])])
        resY = int(contents[k+2][contents[k+2].index('=')+1:len(contents[k+2])])
        bWindowed = 'True' in contents[k+3]
        #bDropFX = 'True' in contents[k+4]
        colourScheme = int(contents[k+4][contents[k+4].index('=')+1:len(contents[k+4])]) #v2.5 RANDOM SCHEME
        backdropIndex = int(contents[k+5][contents[k+5].index('=')+1:len(contents[k+5])])

        if (resX, resY) in resolutions:
            iRes = resolutions.index( (resX, resY) )
    else:
        contents.append('[VIDEO]\n')
        contents.append('resX=' + str(resolutions[iRes][0]) +'\n')
        contents.append('resY=' + str(resolutions[iRes][1]) +'\n')
        contents.append('bWindowed=' + str(bWindowed) +'\n')
        #contents.append('bDropFX=' + str(bDropFX) +'\n')
        contents.append('colorScheme=' + str(colourScheme) +'\n') #v2.5 RANDOM SCHEME
        contents.append('backdropIndex=' + str(backdropIndex) +'\n')
        f = open('tetris.ini', 'w+')#, encoding="utf-8")
        for i in range(len(contents)):
            f.write(contents[i])
        f.close()
    
    #if onLoad:
    #    onLoad = False
    if colourScheme == 8:
        colorScheme = randint(0,7) #v2.5 RANDOM SCHEME
    else:
        colorScheme = colourScheme
    if backdropIndex == len(backdrops):
        backdrop = randint(0, len(backdrops)-1) #v2.5 RANDOM BACKDROP
    else:
        backdrop = backdropIndex
    return (resolutions[iRes], bWindowed, colorScheme, backdrop) #bDropFX

def GetControls(contents):
    global leftKey, rightKey, rotateKey, dropKey, bombKey

    if '[CONTROLS]\n' in contents:
        k = contents.index('[CONTROLS]\n')
        key = contents[k+1][contents[k+1].index('=')+1:len(contents[k+1])-1]
        if len(key) > 1:
            leftKey = int(key)
        else:
            leftKey = ord(key)
        key = contents[k+2][contents[k+2].index('=')+1:len(contents[k+2])-1]
        if len(key) > 1:
            rightKey = int(key)
        else:
            rightKey = ord(key)
        key = contents[k+3][contents[k+3].index('=')+1:len(contents[k+3])-1]
        if len(key) > 1:
            rotateKey = int(key)
        else:
            rotateKey = ord(key)
        key = contents[k+4][contents[k+4].index('=')+1:len(contents[k+4])-1]
        if len(key) > 1:
            dropKey = int(key)
        else:
            dropKey = ord(key)
        key = contents[k+5][contents[k+5].index('=')+1:len(contents[k+5])-1]
        if len(key) > 1:
            bombKey = int(key)
        else:
            bombKey = ord(key)
    else:
        contents.append('[CONTROLS]\n')
        contents.append('left=' + str(leftKey) +'\n')
        contents.append('right=' + str(rightKey) +'\n')
        contents.append('rotate=' + str(rotateKey) +'\n')
        contents.append('drop=' + str(dropKey) +'\n')
        contents.append('bomb=' + str(bombKey) +'\n')
        f = open('tetris.ini', 'w+')#, encoding="utf-8")
        for i in range(len(contents)):
            f.write(contents[i])
        f.close()

    return (leftKey, rightKey, rotateKey, dropKey, bombKey)

def GetGameplay(contents):
    global startLevel, numBombs, dropMode, endLevel

    if '[GAMEPLAY]\n' in contents:
        k = contents.index('[GAMEPLAY]\n')
        startLevel = int(contents[k+1][contents[k+1].index('=')+1:len(contents[k+1])])
        numBombs = int(contents[k+2][contents[k+2].index('=')+1:len(contents[k+2])])
        dropMode = int(contents[k+3][contents[k+3].index('=')+1:len(contents[k+3])])
        endLevel = int(contents[k+4][contents[k+4].index('=')+1:len(contents[k+4])])
    else:
        contents.append('[GAMEPLAY]\n')
        contents.append('startLevel=' + str(startLevel) +'\n')
        contents.append('numBombs=' + str(numBombs) +'\n')
        contents.append('dropMode=' + str(dropMode) +'\n')
        contents.append('endLevel=' + str(endLevel) +'\n')
        f = open('tetris.ini', 'w+')
        for i in range(len(contents)):
            f.write(contents[i])
        f.close()
    
    return (startLevel, numBombs, dropMode, endLevel)

def GetTopTen():
    contents = []
    if os.path.isfile('topten.ini'):
        f = open("topten.ini", "r")#, encoding="utf-8")
        contents = f.readlines()
        f.close()

    topTen = []
    if '[TOPTEN]\n' not in contents:
        contents.clear()
        contents.append('[TOPTEN]\n')
        contents.append('Mario=100000\n')
        contents.append('Ryu=90000\n')
        contents.append('Yoshi=80000\n')
        contents.append('Peach=70000\n')
        contents.append('Bowser=60000\n')
        contents.append('Donkey=50000\n')
        contents.append('Bimmy=40000\n')
        contents.append('Samus=30000\n')
        contents.append('Megaman=20000\n')
        contents.append('Zelda=10000\n')

        f = open('topten.ini', 'w')
        f.writelines(contents)
        f.close()

    for i in range(1, len(contents)):
        topTen.append([contents[i][:contents[i].index('=')], int(contents[i][contents[i].index('=')+1:])])

    return topTen
    
def RecordTopTen(topTen):
    contents = ['[TOPTEN]\n']
    for i in range(len(topTen)):
        playerName = topTen[i][0]
        playerScore = topTen[i][1]
        contents.append(playerName+'='+str(playerScore)+'\n')

    f = open('topten.ini', 'w')
    for i in range(len(contents)):
        f.write(contents[i])
    f.close()
        
def InitSettings(s):
    switch = {
            'graphics': GetGraphics,
            'sound':    GetSound,
            'controls': GetControls,
            'gameplay': GetGameplay
            }
    
    contents = []
    if os.path.isfile('tetris.ini'):
        f = open("tetris.ini", "r")#, encoding="utf-8")
        contents = f.readlines()
        f.close()

    getSetting = switch.get(s)
    return getSetting(contents)

def GetGraphicsSettings():
    return (
        'resX='+str(resolutions[iRes][0]),
        'resY='+str(resolutions[iRes][1]),
        'bWindowed='+str(bWindowed),
        #'bDropFX='+str(bDropFX),
        'colorScheme='+str(colourScheme), #v2.5 RANDOM SCHEME
        'backdropIndex='+str(backdropIndex)
        )

def GetSoundSettings():
    return (
        'soundVolume='+str(soundVolume),
        'musicVolume='+str(musicVolume),
        'playbackMode='+str(playbackMode),
        'musicTrack='+str(musicTrack)
        )

def GetControlsSettings():
    if leftKey < 256:
        left = chr(leftKey)
    else:
        left = str(leftKey)
    if rightKey < 256:
        right = chr(rightKey)
    else:
        right = str(rightKey)
    if rotateKey < 256:
        rotate = chr(rotateKey)
    else:
        rotate = str(rotateKey)
    if dropKey < 256:
        drop = chr(dropKey)
    else:
        drop = str(dropKey)
    if bombKey < 256:
        bomb = chr(bombKey)
    else:
        bomb = str(bombKey)
        
    return (
        'left='+left,
        'right='+right,
        'rotate='+rotate,
        'drop='+drop,
        'bomb='+bomb
        )

def GetGameplaySettings():
    return (
        'startLevel='+str(startLevel),
        'numBombs='+str(numBombs),
        'dropMode='+str(dropMode),
        'endLevel='+str(endLevel)
        )

def SaveSettings(s):
    f = open("tetris.ini", "r")#, encoding="utf-8")
    r = f.readlines()
    
    switch = {
        'VIDEO': GetGraphicsSettings,
        'AUDIO':    GetSoundSettings,
        'CONTROLS': GetControlsSettings,
        'GAMEPLAY': GetGameplaySettings
    }

    getSettings = switch.get(s)
    settings = getSettings()
    bUpdate = False
    k = r.index('['+s+']\n') + 1
    for i in range(len(settings)):
        if settings[i]+'\n' != r[i+k]:
            bUpdate = True
            r[i+k] = settings[i] + '\n'

    if not bUpdate:
        f.close()
        return False
    
    f = open("tetris.ini", "w")#, encoding="utf-8")
    for i in range(len(r)):
        f.write(r[i])
    f.close()
    return True

cp = 0
def InitOptions(f, centerX, topY):
    global blockSize, font, smallFont
    global option
    global cPosRect, cPos, cp, closeRect #cursor
    global winThick
    #global bFlashUp, FV

    blockSize = int(48*f)
    '''font = pygame.font.Font('fonts/emulogic.ttf', int(30*f))
    smallFont = pygame.font.Font('fonts/emulogic.ttf', int(24*f))'''
    font = pygame.font.Font('fonts/Tetris.ttf', int(42*f))
    smallFont = pygame.font.Font('fonts/Tetris.ttf', int(32*f))

    mainMenu.clear()
    graphicsOpt = font.render('VIDEO', True, selectColor(0))
    soundOpt = font.render('AUDIO', True, selectColor(1))
    controlsOpt = font.render('CONTROLS', True, selectColor(2))
    gameplayOpt = font.render('GAMEPLAY', True, selectColor(3))
    #cursor = font.render('>', True, YELLOW)
    offset = blockSize//12
    if offset < 2:
        offset += 1
    graphicsOptRect = graphicsOpt.get_rect(center=(centerX, topY +int(blockSize*2.0)+offset))
    soundOptRect = soundOpt.get_rect(center=(centerX, topY +int(blockSize*4.0)+offset))
    controlsOptRect = controlsOpt.get_rect(center=(centerX, topY +int(blockSize*6.0)+offset)) 
    gameplayOptRect = gameplayOpt.get_rect(center=(centerX, topY +int(blockSize*8.0)+offset))
    mainMenu.append([graphicsOpt, graphicsOptRect])
    mainMenu.append([soundOpt, soundOptRect])
    mainMenu.append([controlsOpt, controlsOptRect])
    mainMenu.append([gameplayOpt, gameplayOptRect])

    option = 'options'
    cPos = (
        graphicsOptRect.centery - offset, 
        soundOptRect.centery - offset, 
        controlsOptRect.centery - offset, 
        gameplayOptRect.centery - offset
        )
    cPosRect = Rect(0,0, blockSize*10, blockSize+blockSize//2)
    cPosRect.center = (centerX, cPos[cp])
    #cPosRect = cursor.get_rect(center =(centerX-int(blockSize*3), cPos[cp]))
    winThick = blockSize//12 + 1

    if closeRect == None:
        closeRect = Rect(-blockSize, 0, blockSize, blockSize)
    if L_Rect['render'] == None:
        L_Rect.update(render=font.render('<', True, WHITE))
    if R_Rect['render'] == None:
        R_Rect.update(render=font.render('>', True, WHITE))

    #bFlashUp = True
    #FV = 130
    
def SetLR(offsetX, offsetY):
    L_Rect.update(rect=L_Rect['render'].get_rect(center=(optionMenuRect.width-int(blockSize*offsetX), cPos[cp]+offsetY)))
    L_Rect.update(select=False)
    R_Rect.update(rect=R_Rect['render'].get_rect(center=(optionMenuRect.width-blockSize//2, cPos[cp]+offsetY)))
    R_Rect.update(select=False)

def InitGraphics():
    global OPTIONMENU, optionMenuRect, optionMenuText, optionMenuTextRect
    global cPos, cp #cursor

    displayWidth = resolutions[iRes][0]
    displayHeight = resolutions[iRes][1]
    
    OPTIONMENU = pygame.Surface((blockSize*13, blockSize*9))
    optionMenuRect = OPTIONMENU.get_rect(left=blockSize, top=displayHeight//2 + blockSize)
    optionMenuText = font.render('VIDEO', True, WHITE)
    optionMenuTextRect = optionMenuText.get_rect(center=(optionMenuRect.width//2, blockSize))
    
    offset = blockSize//12
    if offset < 2:
        offset += 1
    resText = smallFont.render('Resolution', True, YELLOW)
    resTextRect = resText.get_rect(left=blockSize, centery=int(blockSize*2.5)+offset)
    
    modeText = smallFont.render('Display Mode', True, WHITE)
    modeTextRect = modeText.get_rect(left=blockSize, centery=int(blockSize*4)+offset)
    
    #dropText = smallFont.render('drop fx', True, WHITE)
    #dropTextRect = dropText.get_rect(left=blockSize, centery=int(blockSize*5.5))
    colorText = smallFont.render('Color Scheme', True, WHITE)
    colorTextRect = colorText.get_rect(left=blockSize, centery=int(blockSize*5.5)+offset)

    backdropText = smallFont.render('Backdrop', True, WHITE)
    backdropTextRect = backdropText.get_rect(left=blockSize, centery=int(blockSize*7)+offset)

    cp = 0
    cPos = (
        resTextRect.centery - offset, 
        modeTextRect.centery - offset, 
        colorTextRect.centery - offset, 
        backdropTextRect.centery - offset
        ) #dropTextRect.centery
    #cursor = smallFont.render('>', True, YELLOW)
    cPosRect.width = blockSize*13
    cPosRect.center = (optionMenuRect.width//2, cPos[0])
    #cPosRect = cursor.get_rect(center=(blockSize//2, cPos[cp]))
    SetOptionRects(optionMenuRect)

    closeRect.center = (optionMenuRect.right-blockSize//2, optionMenuRect.top+blockSize//2)
    SetLR(5.5, offset)
    
    optsMenu.clear()
    optsMenu.append([resText, resTextRect, 0,0])
    optsMenu.append([modeText, modeTextRect, 0,0])
    optsMenu.append([colorText, colorTextRect, 0,0])
    optsMenu.append([backdropText, backdropTextRect, 0,0])
    UpdateGraphicOpts()

def InitSound():
    global OPTIONMENU, optionMenuRect, optionMenuText, optionMenuTextRect
    global cPos, cp #cursor
    global MUSIC, musicRect, musicText, musicTextRect

    OPTIONMENU = pygame.Surface((blockSize*13, blockSize*9))
    optionMenuRect = OPTIONMENU.get_rect(left=resolutions[iRes][0]-blockSize*14, top=resolutions[iRes][1]//2 + blockSize)
    optionMenuText = font.render('AUDIO', True, WHITE)
    optionMenuTextRect = optionMenuText.get_rect(center=(optionMenuRect.width//2, blockSize))

    offset = blockSize//12
    if offset < 2:
        offset += 1
    sVolumeText = smallFont.render('Sound Volume', True, YELLOW)
    sVolumeTextRect = sVolumeText.get_rect(left=blockSize, centery=int(blockSize*2.5)+offset)
   
    mVolumeText = smallFont.render('Music Volume', True, WHITE)
    mVolumeTextRect = mVolumeText.get_rect(left=blockSize, centery=int(blockSize*4.0)+offset)

    mPlaybackText = smallFont.render('Playback Mode', True, WHITE)
    mPlaybackTextRect = mPlaybackText.get_rect(left=blockSize, centery=int(blockSize*5.5)+offset)
   
    mTrackText = smallFont.render('Music Track', True, WHITE)
    mTrackTextRect = mTrackText.get_rect(left=blockSize, centery=int(blockSize*7.0)+offset)

    MUSIC = pygame.Surface((blockSize*11, int(blockSize/1.5)))
    MUSIC.fill(colorList[colorScheme])
    musicRect = MUSIC.get_rect(left=blockSize, centery=int(blockSize*8.25))

    if not bPanMusic:
        if musicTrack > 0 and musicTrack < len(musicList)+1: #v2.5 RANDOM TRACK
            pygame.time.set_timer(PAN_TRACK, 3000)
            mTrack = musicList[musicTrack-1][:len(musicList[musicTrack-1])-4]
        else:
            mTrack = ''
        musicText = smallFont.render(mTrack, True, WHITE)
        musicTextRect = musicText.get_rect(left=0, top=0)
    
    cp = 0
    cPos = (
        sVolumeTextRect.centery - offset,
        mVolumeTextRect.centery - offset, 
        mPlaybackTextRect.centery - offset,
        mTrackTextRect.centery - offset
        )
    #cursor = smallFont.render('>', True, YELLOW)
    cPosRect.width = blockSize*13
    cPosRect.center = (optionMenuRect.width//2, cPos[0])
    #cPosRect = cursor.get_rect(center=(blockSize//2, cPos[cp]))
    SetOptionRects(optionMenuRect)

    closeRect.center = (optionMenuRect.left+blockSize//2, optionMenuRect.top+blockSize//2)
    SetLR(4.5, offset)

    optsMenu.clear()
    optsMenu.append([sVolumeText, sVolumeTextRect, 0,0])
    optsMenu.append([mVolumeText, mVolumeTextRect, 0,0])
    optsMenu.append([mPlaybackText, mPlaybackTextRect, 0,0])
    optsMenu.append([mTrackText, mTrackTextRect, 0,0])
    UpdateSoundOpts()

def InitControls():
    global OPTIONMENU, optionMenuRect, optionMenuText, optionMenuTextRect
    global cPos, cp #cursor

    OPTIONMENU = pygame.Surface((blockSize*13, blockSize*9))
    optionMenuRect = OPTIONMENU.get_rect(left=blockSize, top=resolutions[iRes][1]//2 + blockSize)
    optionMenuText = font.render('CONTROLS', True, WHITE)
    optionMenuTextRect = optionMenuText.get_rect(center=(optionMenuRect.width//2, blockSize))

    offset = blockSize//12
    if offset < 2:
        offset += 1
    leftText = smallFont.render('Left', True, YELLOW)
    leftTextRect = leftText.get_rect(left=blockSize, centery=int(blockSize*2.5)+offset)

    rightText = smallFont.render('Right', True, WHITE)
    rightTextRect = rightText.get_rect(left=blockSize, centery=int(blockSize*3.75)+offset)

    rotateText = smallFont.render('Rotate', True, WHITE)
    rotateTextRect = rotateText.get_rect(left=blockSize, centery=int(blockSize*5)+offset)

    dropText = smallFont.render('Drop', True, WHITE)
    dropTextRect = dropText.get_rect(left=blockSize, centery=int(blockSize*6.25)+offset)

    bombText = smallFont.render('Bomb', True, WHITE)
    bombTextRect = bombText.get_rect(left=blockSize, centery=int(blockSize*7.5)+offset)

    cp = 0
    cPos = (
        leftTextRect.centery - offset, 
        rightTextRect.centery - offset, 
        rotateTextRect.centery - offset, 
        dropTextRect.centery - offset, 
        bombTextRect.centery - offset
        )
    #cursor = smallFont.render('>', True, YELLOW)
    cPosRect.width = blockSize*13
    cPosRect.center = (optionMenuRect.width//2, cPos[0])
    #cPosRect = cursor.get_rect(center=(blockSize//2, cPos[cp]))
    SetOptionRects(optionMenuRect)
    
    closeRect.center = (optionMenuRect.right-blockSize//2, optionMenuRect.top+blockSize//2)
    L_Rect.update(rect=None)
    R_Rect.update(rect=None)

    optsMenu.clear()
    optsMenu.append([leftText, leftTextRect, 0,0])
    optsMenu.append([rightText, rightTextRect, 0,0])
    optsMenu.append([rotateText, rotateTextRect, 0,0])
    optsMenu.append([dropText, dropTextRect, 0,0])
    optsMenu.append([bombText, bombTextRect, 0,0])
    UpdateControlOpts()

def InitGameplay():
    global OPTIONMENU, optionMenuRect, optionMenuText, optionMenuTextRect
    global cPos, cp #cursor

    OPTIONMENU = pygame.Surface((blockSize*13, blockSize*9))
    optionMenuRect = OPTIONMENU.get_rect(left=resolutions[iRes][0]-blockSize*14, top=resolutions[iRes][1]//2 + blockSize)
    optionMenuText = font.render('GAMEPLAY', True, WHITE)
    optionMenuTextRect = optionMenuText.get_rect(center=(optionMenuRect.width//2, blockSize))

    offset = blockSize//12
    if offset < 2:
        offset += 1
    startLevelText = smallFont.render('Start Speed', True, YELLOW)
    startLevelTextRect = startLevelText.get_rect(left=blockSize, centery=int(blockSize*2.5)+offset)
   
    numBombsText = smallFont.render('Bomb Amount', True, WHITE)
    numBombsTextRect = numBombsText.get_rect(left=blockSize, centery=int(blockSize*4)+offset)
   
    dropModeText = smallFont.render('Drop Mode', True, WHITE)
    dropModeTextRect = dropModeText.get_rect(left=blockSize, centery=int(blockSize*5.5)+offset)

    endLevelText = smallFont.render('End Level', True, WHITE)
    endLevelTextRect = endLevelText.get_rect(left=blockSize, centery=int(blockSize*7)+offset)

    cp = 0
    cPos = (
        startLevelTextRect.centery - offset, 
        numBombsTextRect.centery - offset, 
        dropModeTextRect.centery - offset, 
        endLevelTextRect.centery - offset
        )
    #cursor = smallFont.render('>', True, YELLOW)
    cPosRect.width = blockSize*13
    cPosRect.center = (optionMenuRect.width//2, cPos[0])
    #cPosRect = cursor.get_rect(center=(blockSize//2, cPos[cp]))
    SetOptionRects(optionMenuRect)

    closeRect.center = (optionMenuRect.left+blockSize//2, optionMenuRect.top+blockSize//2)
    SetLR(4.5, offset)

    optsMenu.clear()
    optsMenu.append([startLevelText, startLevelTextRect, 0,0])
    optsMenu.append([numBombsText, numBombsTextRect, 0,0])
    optsMenu.append([dropModeText, dropModeTextRect, 0,0])
    optsMenu.append([endLevelText, endLevelTextRect, 0,0])
    UpdateGameplayOpts()
    
#ocp = -1
def Option(key):
    global option
    global cp, xColor #ocp
    global bUpdateMenu

    if not bKeyBind:
        if key == K_UP:
            pygame.mixer.Sound.play(ts_move)
            bUpdateMenu = True
            if cp > 0:
                cp -= 1
            else:
                cp = len(cPos)-1
        elif key == K_DOWN:
            pygame.mixer.Sound.play(ts_move)
            bUpdateMenu = True
            if cp < len(cPos)-1:
                cp += 1
            else:
                cp = 0

        elif option == 'options':
            if key == K_RETURN:
                pygame.mixer.Sound.play(ts_set)
                bUpdateMenu = True
                key = 0
                #ocp = cp
                option = optionList[cp]
                if option == 'graphics':
                    InitGraphics()
                elif option == 'sound':
                    InitSound()
                elif option == 'controls':
                    InitControls()
                elif option == 'gameplay':
                    InitGameplay()

                if IsMouseInCloseRect(pygame.mouse.get_pos()):
                    xColor = WHITE
                else:
                    xColor = outlineColors[colorScheme]
            elif key == K_ESCAPE:
                pygame.mixer.Sound.play(ts_drop)
                bUpdateMenu = True
                option = ''
                return option
    

    if option == 'graphics':
        option = graphicsOption(key)
        if option != 'graphics':
            cp = 0
    elif option == 'sound':
        option = soundOption(key)
        if option != 'sound':
            cp = 1
    elif option == 'controls':
        option = controlsOption(key)
        if option != 'controls':
            cp = 2
    elif option == 'gameplay':
        option = gameplayOption(key)
        if option != 'gameplay':
            cp = 3
    else:    
        cPosRect.centery = cPos[cp]
        #ocp = -1
        if bUpdateMenu:
            menuList = ('VIDEO', 'AUDIO', 'CONTROLS', 'GAMEPLAY')
            for i in range(len(mainMenu)):
                mainMenu[i][0] = font.render(menuList[i], True, selectColor(i))

    return option

def selectColor(p):
    if cp == p:
        return outlineColors[colorScheme]
    return WHITE

def gameplayOption(key):
    global startLevel, numBombs, dropMode, endLevel
    global bUpdateMenu

    if key == K_ESCAPE:
        pygame.mixer.Sound.play(ts_drop)
        bUpdateMenu = True
        if SaveSettings('GAMEPLAY'):
            return 'setgameplay'
        return 'back'
    elif key == K_LEFT:
        pygame.mixer.Sound.play(ts_rotate)
        bUpdateMenu = True
        if cp == 0:
            if startLevel > 0:
                startLevel -= 1
            else:
                startLevel = 30
        elif cp == 1:
            if numBombs > -1:
                numBombs -= 1
            else:
                numBombs = 10
        elif cp == 2:
            if dropMode > 0:
                dropMode -= 1
            else:
                dropMode = len(DROPMODE)-1
        elif cp == 3:
            if endLevel > 1:
                endLevel -= 1
            elif endLevel == -1:
                endLevel = 100
            else:
                endLevel = -1
    elif key == K_RIGHT:
        pygame.mixer.Sound.play(ts_rotate)
        bUpdateMenu = True
        if cp == 0:
            if startLevel < 30:
                startLevel += 1
            else:
                startLevel = 0
        elif cp == 1:
            if numBombs < 10:
                numBombs += 1
            else:
                numBombs = -1
        elif cp == 2:
            if dropMode < len(DROPMODE)-1:
                dropMode += 1
            else:
                dropMode = 0
        elif cp == 3:
            if endLevel < 100 and endLevel > 0:
                endLevel += 1
            elif endLevel == -1:
                endLevel = 1
            else:
                endLevel = -1

    if bUpdateMenu:
        menuList = ('Start Speed', 'Bomb Amount', 'Drop Mode', 'End Level')
        for i in range(len(optsMenu)):
            optsMenu[i][0] = smallFont.render(menuList[i], True, selectColor(i))
        UpdateGameplayOpts()
        cPosRect.centery = cPos[cp]
    #OPTIONMENU.fill(colorList[colorScheme])
    return 'gameplay'

def UpdateGameplayOpts():
    offset = blockSize//12
    if offset < 2:
        offset += 1
    optsMenu[0][2] = smallFont.render(str(startLevel), True, selectColor(0))
    optsMenu[0][3] = optsMenu[0][2].get_rect(center=(optionMenuRect.width-int(blockSize*2.5), int(blockSize*2.5)+offset))
    if numBombs > -1:
        optsMenu[1][2] = smallFont.render(str(numBombs), True, selectColor(1))
    else:
        optsMenu[1][2] = smallFont.render('DISABLED', True, selectColor(1))
    optsMenu[1][3] = optsMenu[1][2].get_rect(center=(optionMenuRect.width-int(blockSize*2.5), int(blockSize*4)+offset))
    optsMenu[2][2] = smallFont.render(DROPMODE[dropMode], True, selectColor(2))
    optsMenu[2][3] = optsMenu[2][2].get_rect(center=(optionMenuRect.width-int(blockSize*2.5), int(blockSize*5.5)+offset))
    if endLevel != -1:
        optsMenu[3][2] = smallFont.render(str(endLevel), True, selectColor(3))
    else:
        optsMenu[3][2] = smallFont.render('NO LIMIT', True, selectColor(3))
    optsMenu[3][3] = optsMenu[3][2].get_rect(center=(optionMenuRect.width-int(blockSize*2.5), int(blockSize*7)+offset))

    if L_Rect['rect'].centery != cPos[cp]+offset:
        SetLR(4.5, offset)

bKeyBind = False
def controlsOption(key):
    global leftKey, rightKey, rotateKey, dropKey, bombKey
    global bKeyBind, bUpdateMenu
    
    if key == K_ESCAPE:
        pygame.mixer.Sound.play(ts_drop)
        bUpdateMenu = True
        if bKeyBind:
            bKeyBind = False
            UpdateControlOpts()
            return 'controls'
        if SaveSettings('CONTROLS'):
            return 'keybind'
        return 'back'
    elif key == K_RETURN:
        pygame.mixer.Sound.play(ts_set)
        bUpdateMenu = True
        bKeyBind = True
    elif bKeyBind:
        pygame.mixer.Sound.play(ts_disintegrate[0])
        bUpdateMenu = True
        bKeyBind = False
        if cp==0:
            leftKey = key
        elif cp==1:
            rightKey = key
        elif cp==2:
            rotateKey = key
        elif cp==3:
            dropKey = key
        else:
            bombKey = key
                
    if bUpdateMenu:
        menuList = ('Left', 'Right', 'Rotate', 'Drop', 'Bomb')
        for i in range(len(optsMenu)):
            optsMenu[i][0] = smallFont.render(menuList[i], True, selectColor(i))
        UpdateControlOpts()
        cPosRect.centery = cPos[cp]
    #OPTIONMENU.fill(colorList[colorScheme])
    return 'controls'

def UpdateControlOpts():
    x = optionMenuRect.width-blockSize*3
    backColor = [None, None, None, None, None]
    if bKeyBind:
        backColor[cp] = BLACK
        
    offset = blockSize//12
    if offset < 2:
        offset += 1
    optsMenu[0][2] = smallFont.render(str(pygame.key.name(leftKey)), True, selectColor(0), backColor[0])
    optsMenu[0][3] = optsMenu[0][2].get_rect(center=(x, int(blockSize*2.5)+offset))
    optsMenu[1][2] = smallFont.render(str(pygame.key.name(rightKey)), True, selectColor(1), backColor[1])
    optsMenu[1][3] = optsMenu[1][2].get_rect(center=(x, int(blockSize*3.75)+offset))
    optsMenu[2][2] = smallFont.render(str(pygame.key.name(rotateKey)), True, selectColor(2), backColor[2])
    optsMenu[2][3] = optsMenu[2][2].get_rect(center=(x, int(blockSize*5)+offset))
    optsMenu[3][2] = smallFont.render(str(pygame.key.name(dropKey)), True, selectColor(3), backColor[3])
    optsMenu[3][3] = optsMenu[3][2].get_rect(center=(x, int(blockSize*6.25)+offset))
    optsMenu[4][2] = smallFont.render(str(pygame.key.name(bombKey)), True, selectColor(4), backColor[4])
    optsMenu[4][3] = optsMenu[4][2].get_rect(center=(x, int(blockSize*7.5)+offset))

def soundOption(key):
    global soundVolume, musicVolume, playbackMode, musicTrack
    global musicText, musicTextRect
    global bUpdateMenu

    if key == K_ESCAPE:
        pygame.mixer.Sound.play(ts_drop)
        bUpdateMenu = True
        if not bPanMusic:
            pygame.time.set_timer(PAN_TRACK, 0)
        SaveSettings('AUDIO')
        return 'back'
    elif key == K_LEFT:
        pygame.mixer.Sound.play(ts_rotate)
        bUpdateMenu = True
        if cp == 0:
            if soundVolume > 0:
                soundVolume -= 5
                SetSoundVolume(float(soundVolume/100))
        elif cp == 1:
            if musicVolume > 0:
                musicVolume -= 5
                pygame.mixer.music.set_volume(float(musicVolume/100))
        elif cp == 2:
            if playbackMode > 0:
                playbackMode -= 1
            else:
                playbackMode = 2
        elif cp == 3:
            if musicTrack > 0:
                musicTrack -= 1
            else:
                musicTrack = len(musicList)+1 #v2.5 RANDOM TRACK +1
            
            SetPanMusic(False)
            if musicTrack > 0 and musicTrack < len(musicList)+1: #v2.5 RANDOM TRACK
                pygame.time.set_timer(PAN_TRACK, 3000)
                mTrack = musicList[musicTrack-1][:len(musicList[musicTrack-1])-4]
            else:
                mTrack = ''
            musicText = smallFont.render(mTrack, True, WHITE)
            musicTextRect = musicText.get_rect(left=0, top=0)
            MUSIC.fill(colorList[colorScheme])
    elif key == K_RIGHT:
        pygame.mixer.Sound.play(ts_rotate)
        bUpdateMenu = True
        if cp == 0:
            if soundVolume < 100:
                soundVolume += 5
                SetSoundVolume(float(soundVolume/100))
        elif cp == 1:
            if musicVolume < 100:
                musicVolume += 5
                pygame.mixer.music.set_volume(float(musicVolume/100))
        elif cp == 2:
            if playbackMode < 2:
                playbackMode += 1
            else:
                playbackMode = 0
        elif cp == 3:
            if musicTrack < len(musicList)+1: #v2.5 RANDOM TRACK +1
                musicTrack += 1
            else:
                musicTrack = 0
            
            SetPanMusic(False)
            if musicTrack > 0 and musicTrack < len(musicList)+1: #v2.5 RANDOM TRACK
                pygame.time.set_timer(PAN_TRACK, 3000)
                mTrack = musicList[musicTrack-1][:len(musicList[musicTrack-1])-4]
            else:
                mTrack = ''
            musicText = smallFont.render(mTrack, True, WHITE)
            musicTextRect = musicText.get_rect(left=0, top=0)
            MUSIC.fill(colorList[colorScheme])
    elif key == K_RETURN and cp==3:
        pygame.mixer.Sound.play(ts_disintegrate[1])
        PlayNextTrack(True)
        
    if bUpdateMenu:
        menuList = ('Sound Volume', 'Music Volume', 'Playback Mode', 'Music Track')
        for i in range(len(optsMenu)):
            optsMenu[i][0] = smallFont.render(menuList[i], True, selectColor(i))
        UpdateSoundOpts()
        cPosRect.centery = cPos[cp]
    #OPTIONMENU.fill(colorList[colorScheme])
    return 'sound'

def UpdateSoundOpts():
    offset = blockSize//12
    if offset < 2:
        offset += 1
    if musicTrack > len(musicList):
        musicTrackStr = "RANDOM"    #v2.5 RANDOM TRACK
    elif musicTrack > 0:
        musicTrackStr = str(musicTrack)
    else:
        musicTrackStr = "OFF"
    optsMenu[0][2] = smallFont.render(str(soundVolume/10), True, selectColor(0))
    optsMenu[0][3] = optsMenu[0][2].get_rect(center=(optionMenuRect.width-int(blockSize*2.5), int(blockSize*2.5)+offset))
    optsMenu[1][2] = smallFont.render(str(musicVolume/10), True, selectColor(1))
    optsMenu[1][3] = optsMenu[1][2].get_rect(center=(optionMenuRect.width-int(blockSize*2.5), int(blockSize*4.0)+offset))
    optsMenu[2][2] = smallFont.render(PLAYBACK[playbackMode], True, selectColor(2))
    optsMenu[2][3] = optsMenu[2][2].get_rect(center=(optionMenuRect.width-int(blockSize*2.5), int(blockSize*5.5)+offset))
    optsMenu[3][2] = smallFont.render(musicTrackStr, True, selectColor(3))
    optsMenu[3][3] = optsMenu[3][2].get_rect(center=(optionMenuRect.width-int(blockSize*2.5), int(blockSize*7.0)+offset))

    if L_Rect['rect'].centery != cPos[cp]+offset:
        SetLR(4.5, offset)

bUpdateRandom = False #v2.5
def graphicsOption(key):
    global iRes, bWindowed, colourScheme, colorScheme, backdropIndex, backdrop
    global bUpdateMenu, bUpdateRandom, closeRect

    if key == K_RETURN:
        if SaveSettings('VIDEO') or bUpdateRandom: #v2.5 RANDOM
            pygame.mixer.Sound.play(ts_disintegrate[randint(0,1)])
            bUpdateRandom = False
            bUpdateMenu = True
            closeRect = None
            L_Rect['render'] = None
            R_Rect['render'] = None
            SetPanMusic(False)
            return 'setmode'
    elif key == K_ESCAPE:
        pygame.mixer.Sound.play(ts_drop)
        bUpdateMenu = True
        if SaveSettings('VIDEO') or bUpdateRandom: #v2.5 RANDOM
            bUpdateRandom = False
            closeRect = None
            L_Rect['render'] = None
            R_Rect['render'] = None
            SetPanMusic(False)
            return 'setmode'
        return 'back'
    elif key == K_LEFT:
        pygame.mixer.Sound.play(ts_rotate)
        bUpdateMenu = True
        if cp == 0:
            if iRes < len(resOpts)-1:
                iRes += 1
            else:
                iRes = 0
        elif cp == 1:
            bWindowed = not bWindowed
        elif cp == 2:
            if colourScheme > 0:
                colourScheme -= 1
            else:
                colourScheme = len(colorList) #v2.5 RANDOM SCHEME
            if colourScheme == 8:
                bUpdateRandom = True
                colorScheme = randint(0,7)
            else:
                colorScheme = colourScheme
        elif cp == 3:
            if backdropIndex > -1:
                backdropIndex -= 1
            else:
                backdropIndex = len(backdrops) 
            if backdropIndex == len(backdrops):
                bUpdateRandom = True
                backdrop = randint(0, len(backdrops)-1) #v2.5 RANDOM BACKDROP
            else:
                backdrop = backdropIndex
    elif key == K_RIGHT:
        pygame.mixer.Sound.play(ts_rotate)
        bUpdateMenu = True
        if cp == 0:
            if iRes > 0:
                iRes -= 1
            else:
                iRes = len(resOpts)-1
        elif cp == 1:
            bWindowed = not bWindowed
        elif cp == 2:
            if colourScheme < len(colorList): #v2.5 RANDOM SCHEME
                colourScheme += 1
            else:
                colourScheme = 0
            if colourScheme == 8:
                bUpdateRandom = True
                colorScheme = randint(0,7)
            else:
                colorScheme = colourScheme
        elif cp == 3:
            if backdropIndex < len(backdrops):
                backdropIndex += 1
            else:
                backdropIndex = -1
            if backdropIndex == len(backdrops):
                bUpdateRandom = True
                backdrop = randint(0, len(backdrops)-1) #v2.5 RANDOM BACKDROP
            else:
                backdrop = backdropIndex
    #elif key == K_RETURN:
    if bUpdateMenu:
        menuList = ('Resolution', 'Display Mode', 'Color Scheme', 'Backdrop')
        for i in range(len(optsMenu)):
            optsMenu[i][0] = smallFont.render(menuList[i], True, selectColor(i))
        UpdateGraphicOpts()
        cPosRect.centery = cPos[cp]
    #OPTIONMENU.fill(colorList[colorScheme])
    return 'graphics'

def UpdateGraphicOpts():
    offset = blockSize//12
    if offset < 2:
        offset += 1
    optsMenu[0][2] = smallFont.render(resOpts[iRes], True, selectColor(0))
    optsMenu[0][3] = optsMenu[0][2].get_rect(center=(optionMenuRect.width-blockSize*3, int(blockSize*2.5)+offset))
    optsMenu[1][2] = smallFont.render(SCREENMODE[int(bWindowed)], True, selectColor(1))
    optsMenu[1][3] = optsMenu[1][2].get_rect(center=(optionMenuRect.width-blockSize*3, int(blockSize*4)+offset))
    
    colorLabel = schemeNames[colourScheme] #v2.5
    
    optsMenu[2][2] = smallFont.render(colorLabel, True, selectColor(2))
    optsMenu[2][3] = optsMenu[2][2].get_rect(center=(optionMenuRect.width-blockSize*3, int(blockSize*5.5)+offset))
    if backdropIndex == len(backdrops):
        optsMenu[3][2] = smallFont.render('RANDOM', True, selectColor(3)) #v2.5 RANDOM BACKDROP
    elif backdropIndex != -1:
        optsMenu[3][2] = smallFont.render(backdrops[backdropIndex][:len(backdrops[backdropIndex])-4], True, selectColor(3))
    else:
        optsMenu[3][2] = smallFont.render('None', True, selectColor(3))
    optsMenu[3][3] = optsMenu[3][2].get_rect(center=(optionMenuRect.width-blockSize*3, int(blockSize*7)+offset))

    if L_Rect['rect'].centery != cPos[cp]+offset:
        SetLR(5.5, offset)

def OptionsMenu(MENU):
    DisplayMainMenu(MENU, len(mainMenu))
    #if option == 'options':
        #pygame.draw.rect(MENU, YELLOW, cPosRect, winThick)
        #MENU.blit(cursor, cPosRect)

def SetPanMusic(bSet):
    global bPanMusic, panDir
    bPanMusic = bSet
    if bPanMusic:
        if musicTextRect.left >= 0:
            panDir = -1
        else:
            panDir = 1

def DrawX(MENU, offsetRect):
    pygame.draw.line(MENU, xColor, 
        (closeRect.left-offsetRect.left+blockSize//4, closeRect.top-offsetRect.top+blockSize//4), 
        (closeRect.right-offsetRect.left-blockSize//4, closeRect.bottom-offsetRect.top-blockSize//4), 
        winThick)
    pygame.draw.line(MENU, xColor, 
        (closeRect.right-offsetRect.left-blockSize//4, closeRect.top-offsetRect.top+blockSize//4), 
        (closeRect.left-offsetRect.left+blockSize//4, closeRect.bottom-offsetRect.top-blockSize//4), 
        winThick)

def OptionMenu(DISPLAY, bSoundMenu):
    OPTIONMENU.fill(colorList[colorScheme])
    pygame.draw.rect(OPTIONMENU, outlineColors[colorScheme], OPTIONMENU.get_rect(), winThick)
    DrawX(OPTIONMENU, optionMenuRect)
    if option != 'controls':
        OPTIONMENU.blit(L_Rect['render'], L_Rect['rect'])
        OPTIONMENU.blit(R_Rect['render'], R_Rect['rect'])

    DisplayOptsMenu(OPTIONMENU, len(optsMenu))
    if bSoundMenu:
        if musicTextRect.width > musicRect.width and bPanMusic:
            MUSIC.fill(colorList[colorScheme])
            musicTextRect.left += panDir
            if musicTextRect.left >= 0 or musicTextRect.right <= musicRect.width:
                SetPanMusic(False)
                pygame.time.set_timer(PAN_TRACK, 3000)
        MUSIC.blit(musicText, musicTextRect)
        OPTIONMENU.blit(MUSIC, musicRect)
    OPTIONMENU.blit(optionMenuText, optionMenuTextRect)
    #OPTIONMENU.blit(cursor, cPosRect)
    pygame.draw.rect(OPTIONMENU, cursorColor, cPosRect, winThick) #v2.4
    DISPLAY.blit(OPTIONMENU, optionMenuRect)

def MouseMenuControl(cursorRects, mp):
    global cp, bUpdateMenu
    global xColor

    if cursorRects == []:
        bMainMenu = False
        cursorRects = cPosRects
        mp = cp
    else:
        bMainMenu = True

    mousePos = pygame.mouse.get_pos()
    if closeRect != None:
        if IsMouseInCloseRect(mousePos):
            if xColor != WHITE:
                bUpdateMenu = True
                xColor = WHITE
                return -1
        elif xColor == WHITE:
            xColor = outlineColors[colorScheme]
            bUpdateMenu = True

    if L_Rect['rect'] != None and R_Rect['rect'] != None:
        if( mousePos[0] > cursorRects[mp].left+L_Rect['rect'].left and mousePos[0] < cursorRects[mp].left+L_Rect['rect'].right
        and mousePos[1] > cursorRects[mp].top and mousePos[1] < cursorRects[mp].bottom ):
            if not L_Rect['select']:
                bUpdateMenu = True
                L_Rect.update(render=font.render('<', True, outlineColors[colorScheme]))
                L_Rect.update(select=True)
        elif( mousePos[0] > cursorRects[mp].left+R_Rect['rect'].left and mousePos[0] < cursorRects[mp].left+R_Rect['rect'].right
        and mousePos[1] > cursorRects[mp].top and mousePos[1] < cursorRects[mp].bottom ):
            if not R_Rect['select']:
                bUpdateMenu = True
                R_Rect.update(render=font.render('>', True, outlineColors[colorScheme]))
                R_Rect.update(select=True)
        else:
            if L_Rect['select']:
                bUpdateMenu = True
                L_Rect.update(render=font.render('<', True, WHITE))
                L_Rect.update(select=False)
            elif R_Rect['select']:
                bUpdateMenu = True
                R_Rect.update(render=font.render('>', True, WHITE))
                R_Rect.update(select=False)


    for i in range(len(cursorRects)):
        if( mousePos[0] > cursorRects[i].left and mousePos[0] < cursorRects[i].right
        and mousePos[1] > cursorRects[i].top and mousePos[1] < cursorRects[i].bottom 
        and i != mp ):
            pygame.mixer.Sound.play(ts_move)
            bUpdateMenu = True
            if not bMainMenu:
                cp = i
                Option(-1)
                break
            return i

    return -1

def IsMouseInCloseRect(mousePos):
    if( mousePos[0] > closeRect.left and mousePos[0] < closeRect.right
    and mousePos[1] > closeRect.top and mousePos[1] < closeRect.bottom ):
        return True
    return False

def MouseOptionSelect(button):
    global closeRect, xColor
    '''if option != 'options':
        menuRect = optionMenuRect'''
    mousePos = pygame.mouse.get_pos()
    if( mousePos[0] > cPosRects[cp].left and mousePos[0] < cPosRects[cp].right
    and mousePos[1] > cPosRects[cp].top and mousePos[1] < cPosRects[cp].bottom ):
        if button == 1:
            if L_Rect['select']:
                return Option(K_LEFT)
            if R_Rect['select']:
                return Option(K_RIGHT)
            return Option(K_RETURN)
        if button == 4:
            return Option(K_RIGHT)
        if button == 5:
            return Option(K_LEFT)

    if button == 3 or button == 1 and IsMouseInCloseRect(mousePos):
        if option != 'options':
            closeRect.left = -blockSize
            xColor = outlineColors[colorScheme]
        elif closeRect.left < 0:
            closeRect = None
        return Option(K_ESCAPE)
    '''elif( mousePos[0] < menuRect.left or mousePos[0] > menuRect.right 
        or mousePos[1] < menuRect.top or mousePos[1] > menuRect.bottom ):
        return Option(K_ESCAPE)'''

    return option

def SetOptionRects(menuRect):
    global cPosRects
    cPosRects = []
    cursorRect = cPosRect.copy()
    cursorRect.centerx = menuRect.left + menuRect.width//2
    for i in range(len(cPos)):
        cursorRect.centery = menuRect.top + cPos[i]
        cPosRects.append(cursorRect.copy())

def RestartMenu(DISPLAY, GRID):
    pygame.mouse.set_visible(True)

    gridLocX = DISPLAY.get_rect().width//2 - blockSize*5
    gridLocY = DISPLAY.get_rect().height//2 - blockSize*10

    gridWidth = blockSize*10
    restartHeight = blockSize*4
    RESTART = pygame.Surface((gridWidth, restartHeight))
    restartRect = RESTART.get_rect(center=(gridWidth//2, blockSize*10))
    
    reFont = pygame.font.Font('fonts/Tetris.ttf', int(42*resolutions[iRes][1]/1080))
    wouldYouLike = reFont.render("Would you like", True, WHITE)
    toStartAgain = reFont.render("to play again?", True, WHITE)
    yes = reFont.render('YES', True, outlineColors[colorScheme])
    no = reFont.render('NO', True, WHITE)
    fontColor = [outlineColors[colorScheme], WHITE]
    #arrow = font.render('>', True, YELLOW)
    offset = blockSize//12
    if offset < 2:
        offset += 1
    wouldYouLikeRect = wouldYouLike.get_rect()
    wouldYouLikeRect.center = (gridWidth//2, restartHeight//2 - (wouldYouLikeRect.height*3)//2 + offset)
    toStartAgainRect = toStartAgain.get_rect()
    toStartAgainRect.center = (gridWidth//2, restartHeight//2 - toStartAgainRect.height//2 + offset)
    yesRect = yes.get_rect()
    yesRect.center = (gridWidth//2-blockSize*2, restartHeight//2+blockSize)
    noRect = no.get_rect()
    noRect.center = (gridWidth//2+blockSize*2, restartHeight//2+blockSize)
    arrowPos = (noRect.copy(), yesRect.copy())
    noRect.centery += offset
    yesRect.centery += offset
    '''arrowRect = arrow.get_rect()
    yesPos = (yesRect.centerx-yesRect.width//2-arrowRect.width//2, yesRect.centery)
    noPos = (noRect.centerx-noRect.width//2-arrowRect.width//2, noRect.centery)'''
    arrowRects = []
    arrowRect = Rect(0,0, blockSize*4, int(blockSize*1.5))
    arrowRect.centerx = noRect.centerx + gridLocX
    arrowRect.centery = noRect.centery + restartRect.top + gridLocY - offset
    arrowRects.append(arrowRect.copy())
    arrowRect.centerx = yesRect.centerx + gridLocX
    arrowRect.centery = yesRect.centery + restartRect.top + gridLocY - offset
    arrowRects.append(arrowRect.copy())
    arrowRect.center = arrowPos[1].center
    winThick = blockSize//12 + 1

    c = 1
    bUpdate = True
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_F4 and pygame.key.get_pressed()[K_LALT]: #Alt+F4
                    pygame.quit()
                    sys.exit()

                elif event.key == K_RETURN:
                    PlayNextTrack(False)
                    #ResetGame()
                    if c == 1:
                        pygame.mixer.Sound.play(ts_smashing)
                        pygame.mouse.set_visible(False)
                        #DrawScore()
                        #SpawnShape()
                        return True
                    pygame.mixer.Sound.play(ts_break)
                    return False
                    
                elif event.key == K_LEFT or event.key == K_RIGHT:
                    pygame.mixer.Sound.play(ts_move)
                    if c == 1:
                        c = 0
                        bUpdate = True
                    else:
                        c = 1
                        bUpdate = True

                elif event.key == K_ESCAPE:
                    pygame.mouse.set_visible(False)
                    #GRID.blit(grid, (0,0))
                    #DrawBlocks()
                    return ''

            elif event.type == MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                if event.button == 1:
                    if( mousePos[0] > arrowRects[c].left and mousePos[0] < arrowRects[c].right
                    and mousePos[1] > arrowRects[c].top and mousePos[1] < arrowRects[c].bottom ):
                        bUpdate = True
                        PlayNextTrack(False)
                        #ResetGame()
                        if c == 1:
                            pygame.mixer.Sound.play(ts_smashing)
                            pygame.mouse.set_visible(False)
                            #DrawScore()
                            #SpawnShape()
                            return True
                        pygame.mixer.Sound.play(ts_break)
                        return False

                elif event.button == 3:
                    pygame.mouse.set_visible(False)
                    #GRID.blit(grid, (0,0))
                    #DrawBlocks()
                    return ''

            elif event.type == MOUSEMOTION:
                mc = MouseMenuControl(arrowRects, c)
                if mc != -1:
                    c = mc
                    bUpdate = True

            elif event.type == QUIT:
                pygame.quit()
                sys.exit()

        if bUpdate:
            bUpdate = False
            RESTART.fill(colorList[colorScheme])
            RESTART.blit(wouldYouLike, wouldYouLikeRect)
            RESTART.blit(toStartAgain, toStartAgainRect)

            for i in range(2):
                if i == c:
                    fontColor[i] = outlineColors[colorScheme]
                else:
                    fontColor[i] = WHITE
            yes = reFont.render('YES', True, fontColor[1])
            no = reFont.render('NO', True, fontColor[0])
            RESTART.blit(yes, yesRect)
            RESTART.blit(no, noRect)
            arrowRect.center = arrowPos[c].center
            #RESTART.blit(arrow, arrowRect)
            
        FlashCursor() #v2.4
        pygame.draw.rect(RESTART, cursorColor, arrowRect, winThick) #v2.4
        GRID.blit(RESTART, restartRect)
        DISPLAY.blit(GRID, (gridLocX, gridLocY))

        pygame.display.flip()
        pygame.time.Clock().tick(30)