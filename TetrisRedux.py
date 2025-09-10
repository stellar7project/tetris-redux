''' TETRIS Redux Version 2.5 '''
from random import randint
from tetrisGame import GameStarted
from tetrisMenu import *

GAMEVERSION = '2.5.1'

mainFrameSrc = (
    pygame.image.load("images/schemes/mainFrameRed.png").convert(),
    pygame.image.load("images/schemes/mainFrameOrange.png").convert(),
    pygame.image.load("images/schemes/mainFrameGold.png").convert(),
    pygame.image.load("images/schemes/mainFrameGreen.png").convert(),
    pygame.image.load("images/schemes/mainFrameCyan.png").convert(),
    pygame.image.load("images/schemes/mainFrameBlue.png").convert(),
    pygame.image.load("images/schemes/mainFrameIndigo.png").convert(),
    pygame.image.load("images/schemes/mainFrameGrey.png").convert()
)
tetrisGridSrc = (
    pygame.image.load("images/schemes/TETRIS_gridRed.png").convert(),
    pygame.image.load("images/schemes/TETRIS_gridOrange.png").convert(),
    pygame.image.load("images/schemes/TETRIS_gridGold.png").convert(),
    pygame.image.load("images/schemes/TETRIS_gridGreen.png").convert(),
    pygame.image.load("images/schemes/TETRIS_gridCyan.png").convert(),
    pygame.image.load("images/schemes/TETRIS_gridBlue.png").convert(),
    pygame.image.load("images/schemes/TETRIS_gridIndigo.png").convert(),
    pygame.image.load("images/schemes/TETRIS_gridGrey.png").convert()
)
#tetrisMaskSource = pygame.image.load("images/TETRIS_mask.png").convert_alpha()
#rainbowSource = pygame.image.load("images/rainbow.png").convert()
tetrisLogoSrc = pygame.image.load("images/text/tetris.png").convert_alpha()
tetrisLogoWhite = pygame.image.load("images/text/tetris_white.png").convert_alpha() #v2.4

redux = []
reduxSrc = (
    [pygame.image.load("images/text/redux_off.png").convert_alpha()],
    (pygame.image.load("images/text/redux_magenta.png").convert_alpha(), pygame.image.load("images/text/reduxMag_glow.png").convert_alpha()),
    (pygame.image.load("images/text/redux_blue.png").convert_alpha(), pygame.image.load("images/text/reduxBlue_glow.png").convert_alpha()),
    (pygame.image.load("images/text/redux_cyan.png").convert_alpha(), pygame.image.load("images/text/reduxCyan_glow.png").convert_alpha()),
    (pygame.image.load("images/text/redux_green.png").convert_alpha(), pygame.image.load("images/text/reduxGreen_glow.png").convert_alpha()),
    (pygame.image.load("images/text/redux_yellow.png").convert_alpha(), pygame.image.load("images/text/reduxYellow_glow.png").convert_alpha()),
    (pygame.image.load("images/text/redux_orange.png").convert_alpha(), pygame.image.load("images/text/reduxOrange_glow.png").convert_alpha()),
    (pygame.image.load("images/text/redux_red.png").convert_alpha(), pygame.image.load("images/text/reduxRed_glow.png").convert_alpha()),
    (pygame.image.load("images/text/redux_off.png").convert_alpha(), pygame.image.load("images/text/redux_glow.png").convert_alpha())
)

def SetRes(resolution, bWindowed, colorScheme, backdropIndex):
    global DISPLAY, TETRIS, displayWidth, displayHeight
    global mainFrame, mainFrameRect, tetrisGrid, tetrisLogo, tetrisLogoRect, reduxRect #tetrisMask, rainbow, rainbowRect
    global tetrisRect, cursorRect, cursorRects
    global cursorPos, winThick #cursor
    global font, smallFont
    global version, versionRect
    global backdrop, frame
    global blockSize

    #v2.4 RESOLUTION
    if bWindowed:
        DISPLAY = pygame.display.set_mode(resolution)
    else:
        DISPLAY = pygame.display.set_mode(resolution, pygame.FULLSCREEN)

    displayWidth = DISPLAY.get_rect().width
    displayHeight = DISPLAY.get_rect().height

    f = resolution[1]/1080
    oldSize = blockSize
    blockSize = int(48*f)
        
    if backdropIndex != -1:
        backdrop = pygame.transform.scale(backdropSrc[backdropIndex].copy(), resolution) #(blockSize*40, blockSize*22+blockSize//2))
    else:
        backdrop = None

    SetNextList()
    ResizeBlocks(f, oldSize) #blockSize/oldSize)

    #dimensions = (int(frameSrc[colorScheme].get_rect().width*f), int(frameSrc[colorScheme].get_rect().height*f))
    dimensions = (blockSize*12, blockSize*22)
    frame = pygame.transform.scale(frameSrc[colorScheme].copy(), dimensions)
    
    #dimensions = (int(mainFrameSrc[colorScheme].get_rect().width*f), int(mainFrameSrc[colorScheme].get_rect().height*f))
    dimensions = (blockSize*32, blockSize*22)
    mainFrame = pygame.transform.scale(mainFrameSrc[colorScheme].copy(), dimensions)
    mainFrame.set_colorkey(BLACK)
    mainFrameRect = mainFrame.get_rect(center=(displayWidth//2, displayHeight//2))

    dimensions = ( int(blockSize * 30), int(blockSize * 20) ) #1440, 960
    tetrisGrid = pygame.transform.scale(tetrisGridSrc[colorScheme].copy(), dimensions)
    tetrisGrid.set_colorkey(BLACK)
    TETRIS = pygame.Surface(dimensions) #, pygame.SRCALPHA) TOO SLOW
    tetrisRect = TETRIS.get_rect( center=(displayWidth//2, displayHeight//2) )
    '''
    dimensions = ( int(1440 * f), int(288 * f) )
    tetrisMask = pygame.transform.scale(tetrisMaskSource.copy(), dimensions)
    MASK = tetrisMask.copy()
    
    dimensions = ( int(1440 * f), int(576 * f) )
    rainbow = pygame.transform.scale(rainbowSource.copy(), dimensions)
    rainbowRect = rainbow.get_rect(center=(dimensions[0]//2, 0))
    '''
    if colorScheme == 7:
        tetrisLogoSource = tetrisLogoWhite.copy()
    else:
        tetrisLogoSource = tetrisLogoSrc.copy()
    
    dimensions = (int(tetrisLogoSource.get_rect().width * f), int(tetrisLogoSource.get_rect().height * f))
    tetrisLogo = pygame.transform.scale(tetrisLogoSource, dimensions)
    tetrisLogoRect = tetrisLogo.get_rect(center=(tetrisRect.width//2, int(blockSize*5.0)))

    dimensions = (int(reduxSrc[0][0].get_rect().width * f), int(reduxSrc[0][0].get_rect().height * f))
    redux.clear()
    redux.append([pygame.transform.scale(reduxSrc[0][0].copy(), dimensions)])
    for i in range(1, len(reduxSrc)):
        redux.append( [pygame.transform.scale(reduxSrc[i][0].copy(), dimensions), pygame.transform.scale(reduxSrc[i][1].copy(), dimensions)] )
    reduxRect = redux[0][0].get_rect(center=(tetrisRect.width//2, int(blockSize*8.5)))

    smallFont = pygame.font.Font('fonts/Tetris.ttf', int(32*f))
    font = pygame.font.Font('fonts/Tetris.ttf', int(42*f))
    #cursor = font.render('>', True, YELLOW)
    cursorRect = Rect(0, 0, blockSize*10, blockSize+blockSize//2)
    cursorRect.centerx = tetrisRect.left + tetrisRect.width//2
    cursorPos = (
        tetrisRect.height//2+blockSize*2+blockSize//2, 
        tetrisRect.height//2+blockSize*4+blockSize//2, 
        tetrisRect.height//2+blockSize*6+blockSize//2, #v2.4
        tetrisRect.height//2+blockSize*8+blockSize//2
        )
    cursorRects = []
    for i in range(4): #v2.4 Needs 4 cursorRects for main menu
        cursorRect.centery = tetrisRect.top + cursorPos[i]
        cursorRects.append(cursorRect.copy())
    cursorRect.center = (tetrisRect.width//2, cursorPos[0])
    winThick = blockSize//12 + 1

    #v2.4 GAME VERSION
    broderbund = pygame.font.Font('fonts/Broderbund Old Bold.ttf', int(33*f))
    version = broderbund.render(f'Version  {GAMEVERSION}', False, outlineColors[colorScheme])
    versionRect = version.get_rect() #(right=displayWidth, bottom=displayHeight)
    versionRect.center = (mainFrameRect.width//2, mainFrameRect.height-versionRect.height//1.7)
    

def ShowLogo():
    logoSrc = []
    logodir = os.listdir('images/logos')
    for logo in logodir:
        imgFormat = logo[len(logo)-3:]
        if imgFormat == 'png' or imgFormat == 'jpg':
            logoSrc.append( pygame.image.load(f'images/logos/{logo}').convert_alpha() )

    logos = []
    f = displayWidth/1920
    for i in range(len(logoSrc)):
        dimensions = ( int(logoSrc[i].get_rect().width * f), int(logoSrc[i].get_rect().height * f) )
        logo = pygame.transform.scale(logoSrc[i].copy(), dimensions)
        logoRect = logo.get_rect( center=(displayWidth//2, displayHeight//2) )
        logos.append([logo, logoRect])
    
    if not logos:
        print("MISSING LOGOS >> Loading main title...")
        return

    LOGOTIME = 28
    bFadeOut = False
    opacity = 0
    i = 0
    pygame.time.set_timer(LOGOTIME, 4000)

    while i < len(logos):
        DISPLAY.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == LOGOTIME or event.type == KEYDOWN:
                pygame.time.set_timer(LOGOTIME, 0)
                bFadeOut = True
                break

        logos[i][0].set_alpha(opacity)
        DISPLAY.blit(logos[i][0], logos[i][1])
        
        if bFadeOut:
            if opacity > 0:
                opacity -= 16
            else:
                i += 1
                bFadeOut = False
                if i < len(logos):
                    pygame.time.set_timer(LOGOTIME, 4000)
                
        elif opacity < 255:
            opacity += 16

        pygame.display.flip()
        pygame.time.Clock().tick(30)
        
def ShowTopTen():
    topTenTitle = font.render('TOP TEN', True, WHITE)
    topTenRect = topTenTitle.get_rect(center=(displayWidth//2, int(blockSize*2.75)))
    topTen = GetTopTen()

    topScores = []
    row = 4.25
    for i in range(len(topTen)):
        playerName = smallFont.render(str(i+1)+'. '+topTen[i][0], True, WHITE)
        playerScore = smallFont.render(str(topTen[i][1]), True, WHITE)
        playerNameRect = playerName.get_rect(left=displayWidth//2-int(blockSize*4.5), centery=int(blockSize*row))
        playerScoreRect = playerScore.get_rect(right=displayWidth//2+int(blockSize*4.5), centery=int(blockSize*row))
        topScores.append([playerName, playerNameRect, playerScore, playerScoreRect])
        row += 1.5

    if backdrop != None:
        DISPLAY.blit(backdrop, backdrop.get_rect(center=(displayWidth//2, displayHeight//2)))
    else:
        DISPLAY.fill(BLACK)
    DISPLAY.blit(frame, frame.get_rect(center=(displayWidth//2, displayHeight//2)))
    DISPLAY.blit(topTenTitle, topTenRect)
    for i in range(len(topScores)):
        DISPLAY.blit(topScores[i][0], topScores[i][1])
        DISPLAY.blit(topScores[i][2], topScores[i][3])

    pygame.display.flip() #v2.5
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_F4 and pygame.key.get_pressed()[K_LALT]: #Alt+F4
                    pygame.quit()
                    sys.exit()
                elif event.key == K_ESCAPE:
                    pygame.time.set_timer(USEREVENT, randint(10000, 20000))
                    return False

            elif event.type == USEREVENT:
                pygame.time.set_timer(USEREVENT, randint(10000, 20000))
                return False

            elif event.type == NEXT_TRACK:
                PlayNextTrack(False)

            elif event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.time.Clock().tick(30)
        
def InitMain():
    offset = blockSize//12
    if offset < 2:
        offset += 1
    mainMenu.clear()
    startGame = font.render('START', True, outlineColors[getColorScheme()]) #v2.4
    options = font.render('OPTIONS', True, WHITE)
    credits = font.render('CREDITS', True, WHITE)
    exitGame = font.render('EXIT', True, WHITE)
    startRect = startGame.get_rect(center=(tetrisRect.width//2, tetrisRect.height//2+blockSize*2+blockSize//2+offset))  #3
    optionsRect = options.get_rect(center=(tetrisRect.width//2, tetrisRect.height//2+blockSize*4+blockSize//2+offset))  #5
    creditsRect = credits.get_rect(center=(tetrisRect.width//2, tetrisRect.height//2+blockSize*6+blockSize//2+offset)) #v2.4
    exitRect = exitGame.get_rect(center=(tetrisRect.width//2, tetrisRect.height//2+blockSize*8+blockSize//2+offset))    #7
    mainMenu.append([startGame, startRect])
    mainMenu.append([options, optionsRect])
    mainMenu.append([credits, creditsRect])
    mainMenu.append([exitGame, exitRect])

def LaunchGame(bRollCredits=False):
    pygame.mixer.Sound.stop(light_noise)
    pygame.time.set_timer(USEREVENT, 0)
    pygame.mixer.Sound.play(ts_smashing)
    pygame.mouse.set_visible(False)
    GameStarted(bRollCredits)
    pygame.mouse.set_visible(True)
    screenSet = InitSettings('graphics')
    SetRes(screenSet[0], screenSet[1], screenSet[2], screenSet[3]) #Reset screen mode on return
    InitMain()

def main():
    #INITIALIZE ========================
    screenSet = InitSettings('graphics')
    SetRes(screenSet[0], screenSet[1], screenSet[2], screenSet[3])
    ShowLogo()

    InitSettings('sound')
    PlayNextTrack(False)

    InitSettings('controls')

    InitSettings('gameplay')
    #===================================
    tetra = []
    glow = 0
    #tick = 0
    c = 0
    #bPanMusic = False
    pygame.time.set_timer(USEREVENT+1, 1000)
    pygame.time.set_timer(USEREVENT, randint(10000, 20000))
    bRestartTopTenTimer = False
    option = ''
    InitMain()
    flickerInt = 60
    flickerLen = 30
    flickerTimer = 30
    deltaFlick = 1
    lightIndex = 0 #randint(0, len(redux)-1)
    bRefreshBackdrop = False
    bMouseControl = False
    bUpdate = False
    mousePos = pygame.mouse.get_pos()

    if backdrop != None:
        DISPLAY.blit(backdrop, backdrop.get_rect(center=(displayWidth//2, displayHeight//2)))
        TETRIS.blit(backdrop, backdrop.get_rect(center=(blockSize*15, blockSize*10)))
    while True:
        gOption = option

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_F4 and pygame.key.get_pressed()[K_LALT]: #Alt+F4
                    pygame.quit()
                    sys.exit()
                elif option == '':
                    if event.key == K_UP:
                        pygame.mixer.Sound.play(ts_move)
                        bUpdate = True
                        c -= 1
                        if c < 0:
                            c = 3
                    elif event.key == K_DOWN:
                        pygame.mixer.Sound.play(ts_move)
                        bUpdate = True
                        c += 1
                        if c > 3:
                            c = 0
                            
                    elif event.key == K_RETURN:
                        bUpdate = True
                        if c == 0:
                            LaunchGame()
                            bRefreshBackdrop = True
                            if lightIndex != 0 and flickerTimer > flickerLen:
                                pygame.mixer.Sound.play(light_noise, -1)
                        elif c == 1:
                            pygame.mixer.Sound.play(ts_set)
                            option = 'options'
                            InitOptions(blockSize/48, tetrisRect.width//2, tetrisRect.height//2+blockSize)
                            SetOptionRects(tetrisRect)
                        elif c == 2: #v2.4
                            LaunchGame(True)
                            bRefreshBackdrop = True
                            if lightIndex != 0 and flickerTimer > flickerLen:
                                pygame.mixer.Sound.play(light_noise, -1)
                        else:
                            pygame.quit()
                            sys.exit()

                else:
                    option = Option(event.key)

                pygame.time.set_timer(USEREVENT, randint(10000, 20000))

            elif event.type == MOUSEMOTION:
                bMouseControl = True
                if not bRestartTopTenTimer:
                    bRestartTopTenTimer = True
                    pygame.time.set_timer(USEREVENT, 0)

            elif event.type == MOUSEBUTTONDOWN:
                if option == '':
                    mousePos = pygame.mouse.get_pos()
                    if( event.button == 1
                    and mousePos[0] > cursorRects[c].left and mousePos[0] < cursorRects[c].right
                    and mousePos[1] > cursorRects[c].top and mousePos[1] < cursorRects[c].bottom ):
                        bUpdate = True
                        if c == 0:
                            LaunchGame()
                            bRefreshBackdrop = True
                            if lightIndex != 0 and flickerTimer > flickerLen:
                                pygame.mixer.Sound.play(light_noise, -1)
                        elif c == 1:
                            pygame.mixer.Sound.play(ts_set)
                            option = 'options'
                            InitOptions(blockSize/48, tetrisRect.width//2, tetrisRect.height//2+blockSize)
                            SetOptionRects(tetrisRect)
                        elif c == 2: #v2.4
                            LaunchGame(True)
                            bRefreshBackdrop = True
                            if lightIndex != 0 and flickerTimer > flickerLen:
                                pygame.mixer.Sound.play(light_noise, -1)
                        else:
                            pygame.quit()
                            sys.exit()
                else:
                    #mainMenuRect = Rect(0,0, blockSize*10, blockSize*9)
                    #mainMenuRect.center = (displayWidth//2, displayHeight//2 + int(blockSize*5.5))
                    option = MouseOptionSelect(event.button)

                pygame.time.set_timer(USEREVENT, randint(10000, 20000))

            elif event.type == USEREVENT+1:
                i = randint(0,6)
                nextShape = GetNextList(getColorScheme(), randint(0,1))[i][randint(0,len(nextList[i])-1)].copy() #v2.5
                shapeRect = nextShape.get_rect()
                nextShape.set_alpha(256)
                offsetX = randint(0,2)
                offsetX = (randint(0, 10 - shapeRect.width//blockSize) + offsetX*10) * blockSize
                tetra.append([nextShape, [offsetX, -shapeRect.height], shapeRect.height])
                alpha = 256
                for i in range(3):
                    drop = nextShape.copy()
                    alpha //= 2
                    drop.set_alpha(alpha)
                    tetra.append([drop, [offsetX, -shapeRect.height-blockSize*(i+1)], shapeRect.height])
                
            elif event.type == NEXT_TRACK:
                PlayNextTrack(False)
                
            elif event.type == PAN_TRACK:
                pygame.time.set_timer(PAN_TRACK, 0)
                SetPanMusic(True)

            elif event.type == USEREVENT:
                ShowTopTen()
                bRefreshBackdrop = True

            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
                
        if bRefreshBackdrop:
            if backdrop != None:
                bRefreshBackdrop = False
                DISPLAY.blit(backdrop, backdrop.get_rect(center=(displayWidth//2, displayHeight//2)))
                TETRIS.blit(backdrop, backdrop.get_rect(center=(blockSize*15, blockSize*10)))
            else:
                bRefreshBackdrop = False
                DISPLAY.fill(BLACK)
        TETRIS.blit(tetrisGrid, (0,0))
        
        i = 0
        while i < len(tetra):
            if tetra[i][1][1] < tetrisRect.height-blockSize*3:
                tetra[i][1][1] += blockSize
            else:
                tetra.pop(i)
                continue

            if (tetra[i][1][0] < blockSize*10 or tetra[i][1][0] >= blockSize*20) and tetra[i][1][1]+tetra[i][2] > blockSize*10:
                tetraHeight = blockSize*10-tetra[i][1][1]
                if tetraHeight > 0:
                    TETRIS.blit(tetra[i][0], tetra[i][1], tetra[i][0].get_rect(height=tetraHeight))
                else:
                    tetra.pop(i)
                    continue
            else:
                if tetra[i][1][1] > blockSize*10:
                    tetra[i][0].set_alpha(tetra[i][0].get_alpha()//2)
                TETRIS.blit(tetra[i][0], tetra[i][1])

            i += 1
            

        if option == '':
            # Mouse Control
            if bMouseControl:
                bMouseControl = False
                mc = MouseMenuControl(cursorRects, c)
                if mc != -1:
                    c = mc
                    bUpdate = True

            elif bRestartTopTenTimer:
                bRestartTopTenTimer = False
                pygame.time.set_timer(USEREVENT, randint(10000, 20000))

            if gOption != option:
                gOption = option
                InitMain()

            if bUpdate:
                bUpdate = False
                cursorRect.centery = cursorPos[c]
                menuList = ('START', 'OPTIONS', 'CREDITS', 'EXIT') #v2.4
                for i in range(len(mainMenu)):
                    if c == i:
                        fontColor = outlineColors[getColorScheme()] #v2.4
                    else:
                        fontColor = WHITE
                    mainMenu[i][0] = font.render(menuList[i], True, fontColor)
            DisplayMainMenu(TETRIS, len(mainMenu))
            #TETRIS.blit(cursor, cursorRect)
            FlashCursor() #v2.4
            pygame.draw.rect(TETRIS, getCursorColor(), cursorRect, winThick)
        else:
            if bMouseControl:
                bMouseControl = False
                MouseMenuControl([], -1)
            elif bRestartTopTenTimer:
                bRestartTopTenTimer = False
                pygame.time.set_timer(USEREVENT, randint(10000, 20000))
            OptionsMenu(TETRIS)
            FlashCursor()
            if option == 'options':
                SetOptionRects(tetrisRect)
                DrawCursor(DISPLAY, TETRIS, tetrisRect)

        if flickerTimer == flickerInt:
            pygame.mixer.Sound.stop(light_noise)
            flickerTimer = 0
            flickerInt = randint(150, 360)
            flickerLen = randint(30, 90)
        flickerTimer += 1
        if flickerTimer < flickerLen:
            if flickerTimer == deltaFlick:
                deltaFlick = flickerTimer + randint(1,2)
                if random() < 0.35:
                    glow = 0
                    if lightIndex != 0:
                        lightIndex = 0
                else:
                    pygame.mixer.Sound.play(arcing)
                    glow = randint(32, 192)
                    if lightIndex == 0:
                        if getColorScheme() == 7: #v2.4
                            lightIndex = len(redux)-1
                        else:
                            lightIndex = randint(1, len(redux)-1)
        else:
            if flickerTimer == flickerLen:
                pygame.mixer.Sound.stop(arcing)
                pygame.mixer.Sound.play(light_noise, -1)
                if getColorScheme() == 7: #v2.4
                    lightIndex = len(redux)-1
                else:
                    lightIndex = randint(1, len(redux)-1)
                deltaFlick = 1
            if lightIndex != 0:
                glow = randint(166, 200)
            
        #MASK.blit(tetrisMask, (0,0))
        #MASK.blit(rainbow, rainbowRect, None, BLEND_RGBA_MULT)
        #TETRIS.blit(MASK, (0, blockSize*2))
        TETRIS.blit(tetrisLogo, tetrisLogoRect)
        TETRIS.blit(redux[lightIndex][0], reduxRect)
        mainFrame.blit(version, versionRect) #v2.4
        if lightIndex != 0:
            reduxGlowCopy = redux[lightIndex][1].copy()
            reduxGlowCopy.fill((255,255,255, glow), None, BLEND_RGBA_MULT)
            TETRIS.blit(reduxGlowCopy, reduxRect)
        DISPLAY.blit(TETRIS, tetrisRect)
        DISPLAY.blit(mainFrame, mainFrameRect)
        #DISPLAY.blit(version, versionRect)

        if option in optionList:
            OptionMenu(DISPLAY, option=='sound')
        elif option != '' and option != 'options':
            if option == 'setmode':
                screenSet = InitSettings('graphics')
                SetRes(screenSet[0], screenSet[1], screenSet[2], screenSet[3])
            InitOptions(blockSize/48, tetrisRect.width//2, tetrisRect.height//2+blockSize)
            option = 'options'
            bRefreshBackdrop = True

        pygame.display.flip()
        pygame.time.Clock().tick(30)

#pygame.mouse.set_visible(False)
main()