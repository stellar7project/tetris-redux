''' TETRIS Version 2.5 '''

from tetrisMenu import *

#pygame.init()

#DISPLAY = pygame.display.set_mode((displayWidth, displayHeight))
#pygame.display.set_caption('TETRIS')

GAMEOVER = 25
shapeType = 0
dropFX = []
tetrisLines = []
FPS = 30

def SetGameplay():
    global rate, numBombs, bombs, dropMode, endLevel

    gameplay = InitSettings('gameplay')
    #level = 0
    rate = 31-gameplay[0]
    numBombs = gameplay[1]
    bombs = numBombs
    dropMode = gameplay[2]
    endLevel = gameplay[3]
    
def SetControls():
    global leftKey, rightKey, rotateKey, dropKey, bombKey
    
    controls = InitSettings('controls')
    leftKey = controls[0]
    rightKey = controls[1]
    rotateKey = controls[2]
    dropKey = controls[3]
    bombKey = controls[4]
    
def SetGraphics(resolution, bWindowed, colorScheme, backdropIndex):
    global DISPLAY, displayWidth, displayHeight
    global gridWidth, gridHeight, scoreWidth, scoreHeight, nextWidth, nextHeight
    global backdrop, backdropRect, grid, frame, tetrisOut, tetris4Out, combo
    global font, smallFont, pointFont
    global scoreTitle, levelTitle, linesTitle, nextTitle, bombsTitle #gameOver
    global blockSize, colScheme
    global monoColor #v2.5

    global GRID, SCORE, NEXT
    global gridLocX, gridLocY

    
    if bWindowed:
        DISPLAY = pygame.display.set_mode(resolution) # Obsolete --HWSURFACE|DOUBLEBUF)
    else:
        DISPLAY = pygame.display.set_mode(resolution, pygame.FULLSCREEN) # Obsolete --|HWSURFACE|DOUBLEBUF)

    displayWidth = DISPLAY.get_rect().width
    displayHeight = DISPLAY.get_rect().height
        
    f = resolution[1]/1080
    
    oldSize = blockSize
    blockSize = int(48 * f)

    if backdropIndex != -1:
        backdropImg = backdropSrc[backdropIndex].copy()
    else:
        backdropImg = colorSrc['black']
    backdrop = pygame.transform.scale(backdropImg, resolution) #(blockSize*40, blockSize*22+blockSize//2))
    backdropRect = backdrop.get_rect(center=(displayWidth//2, displayHeight//2))
    
    for k in colorSrc:
        colorSrc[k] = pygame.transform.scale(colorSrc[k], (displayWidth, displayHeight))

    gridWidth = int(blockSize*10) #480
    gridHeight = int(blockSize*20) #960
    grid = pygame.transform.scale(gridSrc[colorScheme].copy(), (gridWidth, gridHeight))
    scoreWidth = int(blockSize*5) #240
    scoreHeight = int(blockSize*9) #432
    nextWidth = int(blockSize*5)
    nextHeight = int(blockSize*9)

    SetNextList()

    fOffset = blockSize/oldSize
    ResizeBlocks(f, oldSize) #fOffset)
    #resF = f
    #heatBlock = pygame.transform.scale(heatSource.copy(), (blockSize, blockSize))
    frame = pygame.transform.scale(frameSrc[colorScheme].copy(), (gridWidth+blockSize*2, gridHeight+blockSize*2))
    aspectRatio = resolution[0]/resolution[1]
    if aspectRatio == 4/3 or aspectRatio == 5/4:
        g = 4
    elif aspectRatio == 16/10:
        g = 2.5
    else:
        g = 2
    tetrisOut = pygame.transform.scale(tetrisOutSrc[0].copy(), (int(tetrisOutSrc[0].get_rect().width*f/g), int(tetrisOutSrc[0].get_rect().height*f/g)))
    tetris4Out = pygame.transform.scale(tetrisOutSrc[1].copy(), (int(tetrisOutSrc[1].get_rect().width*f/g), int(tetrisOutSrc[1].get_rect().height*f/g)))
    combo = pygame.transform.scale(comboSrc.copy(), (int(comboSrc.get_rect().width*f/g), int(comboSrc.get_rect().height*f/g)))
    
    colScheme = colorScheme
    if colScheme == 7: #v2.5
        monoColor = randint(0,1)
    else:
        monoColor = 0

    for i in range(len(dropFX)):
        dropFX[i][0] = GetNextList(colScheme, shape[0][2])[shapeType][iRot-1].copy() #v2.5
        dropFX[i][0].set_alpha(dropFX[i][2])
        dropFX[i][1][0] = int(dropFX[i][1][0]*fOffset)
        dropFX[i][1][1] = int(dropFX[i][1][1]*fOffset)
        
    '''font = pygame.font.Font('fonts/emulogic.ttf', int(30*f))
    smallFont = pygame.font.Font('fonts/emulogic.ttf', int(24*f))
    smallerFont = pygame.font.Font('fonts/emulogic.ttf', int(16*f))'''
    font = pygame.font.Font('fonts/Tetris.ttf', int(42*f))
    smallFont = pygame.font.Font('fonts/Tetris.ttf', int(32*f))
    pointFont = pygame.font.Font('fonts/Broderbund Old Bold.ttf', int(48*f))
    scoreTitle = font.render('SCORE', True, WHITE)
    levelTitle = font.render('LEVEL', True, WHITE)
    linesTitle = font.render('LINES', True, WHITE)         
    nextTitle = font.render('NEXT', True, WHITE)
    if bombs != -1:
        bombsTitle = font.render('BOMBS', True, WHITE)
    else:
        bombsTitle = font.render('BOMBS', True, GREY)
    #gameOver = font.render('GAME OVER', True, OUTRED)
    
    GRID = pygame.Surface((gridWidth, gridHeight))
    SCORE = pygame.Surface((scoreWidth, scoreHeight))
    NEXT = pygame.Surface((nextWidth, nextHeight))
    
    gridLocX = displayWidth//2 - gridWidth//2
    gridLocY = displayHeight//2 - gridHeight//2


def GetRotCollision(tetraPos, index):
    if shapeType == 3 or shapeType == 4:
        if iRot == 0:
            hit = GetCollision(tetraPos[3][0], tetraPos[3][1])
            if hit != '':
                for i in range(len(tetraPos)):
                    tetraPos[i][0] -= blockSize
                    if i < 3:
                        hit = GetCollision(tetraPos[i][0], tetraPos[i][1])
                        if hit != '':
                            return hit
                return ''
            else:
                hit = GetCollision(tetraPos[0][0], tetraPos[0][1])
                if hit != '':
                    for i in range(len(tetraPos)):
                        tetraPos[i][0] += blockSize
                        if i > 0:
                            hit = GetCollision(tetraPos[i][0], tetraPos[i][1])
                            if hit != '':
                                return hit
                    return ''
        else:
            for i in range(3,-1,-1):
                if i > 0:
                    hit = GetCollision(tetraPos[i][0], tetraPos[i][1])
                    if hit != '':
                        return hit
            return ''
        return hit
    
    if iRot < 2:
        shift = blockSize
    else:
        shift = -blockSize

    ## Must check collision with all 4 pieces

    hit = GetCollision(tetraPos[0][0], tetraPos[0][1]) # 1st block
    if hit != '':
        for i in range(len(tetraPos)):
            tetraPos[i][index] += shift

        for i in range(1,4): # then 2nd, 3rd, 4th
            hit = GetCollision(tetraPos[i][0], tetraPos[i][1])
            if hit != '':
                break

    else:
        for i in range(2,4): # 3rd and 4th
            hit = GetCollision(tetraPos[i][0], tetraPos[i][1])
            if hit != '':
                if shapeType == 5:
                    shift *= 4 - i
                for j in range(len(tetraPos)):
                    tetraPos[j][index] -= shift
                for k in range(i): # then 1st, 2nd..
                    hit = GetCollision(tetraPos[k][0], tetraPos[k][1])
                    if hit != '':
                        break
                break

    return hit

def RotateShape(tick, bPlaySound):
    global iRot

    tetraPos = []
    for i in range(len(shape)):
        offsetX = rotOffsets[i][iRot][0] * blockSize
        offsetY = rotOffsets[i][iRot][1] * blockSize
        x = shape[i][1][0]+offsetX
        y = shape[i][1][1]+offsetY
        tetraPos.append([x,y])

    hit = GetRotCollision(tetraPos, iRot%2)
    
    if hit == '':
        if bPlaySound:
            pygame.mixer.Sound.play(ts_rotate)
        for i in range(len(shape)):
            #offsetX = rotOffsets[i][iRot][0] * blockSize
            #offsetY = rotOffsets[i][iRot][1] * blockSize
            shape[i][1][0] = tetraPos[i][0]
            shape[i][1][1] = tetraPos[i][1]
            
        iRot = (iRot + 1) % len(rotOffsets[0])
        #return tick
    return tick #0
    
def DrawBlocks():
    
    for i in range(len(blockList)):
        for j in range(len(blockList[i])):
            GRID.blit(blockList[i][j][0], tuple(blockList[i][j][1]))

    if explode >= 0:
        for i in range(len(bombList)):
            GRID.blit(blocks[bombList[i][0]], tuple(bombList[i][1]))
    else:
        for i in range(len(dropList)):
            for j in range(len(dropList[i])):
                GRID.blit(dropList[i][j][0], tuple(dropList[i][j][1]))
        
        if dropFX != []:
            for i in range(len(dropFX)):
                dropFX[i][2] -= 32
                dropFX[i][0].set_alpha(dropFX[i][2])
                GRID.blit(dropFX[i][0], tuple(dropFX[i][1]))
                
            if dropFX[0][2] < 32:
                dropFX.pop(0)

    for i in range(len(shape)):
        GRID.blit(shape[i][0], tuple(shape[i][1]))

'''def AddOutHots(tetraList, imgIndex):
    for i in range(len(tetraList)):
        hotCoords = [x-6*resF for x in tetraList[i][1]]
        hotBlock = hotBlocks[tetraList[i][imgIndex]].copy()
        outHots.append([hotBlock, hotCoords])'''

def AddToHotList(state, tetraList, imgIndex):
    for i in range(len(tetraList)):
        x = tetraList[i][1][0] + gridLocX + blockSize//2
        y = tetraList[i][1][1] + gridLocY + blockSize//2
        hotBlock = Block(state, tetraList[i][imgIndex], [x,y], [0,0], 0, 0.05, heatAlpha, 0)
        hotBlock.initPulse(127, 255, 15)
        hotList.append(hotBlock)

def HotListState(state):
    for i in range(len(hotList)):
        hotList[i].state = state
        hotList[i].heatAlpha = heatAlpha
        
def GetCollision(x, y):
    centerX = x + blockSize/2
    centerY = y + blockSize/2
    if centerX < 0 or centerX > gridWidth:
        return 'block'
    if centerY > gridHeight:
        return 'floor'

    j = 20 - y//blockSize
    if len(blockList) > 0 and j <= len(blockList):
        for i in range(len(blockList[j-1])):
            if [x, y] in blockList[j-1][i]:
                return 'floor'
            
    return ''
        
def MoveBlocks(blocks, offsetX, offsetY):
    for i in range(len(blocks)):
        hit = GetCollision(blocks[i][1][0]+offsetX, blocks[i][1][1]+offsetY)
        if hit != '':
            break
        
    if hit == '':
        for i in range(len(blocks)):
            blocks[i][1][0] += offsetX
            blocks[i][1][1] += offsetY
        '''    
        for i in range(len(dropFX)):
            for j in range(len(dropFX[i])):
                dropFX[i][j][1][0] += offsetX
                dropFX[i][j][1][1] += offsetY'''
    elif hit == 'floor':
        return True

    pygame.mixer.Sound.play(ts_move)
    return False

def AddToBlockList(blocks):
    for i in range(len(blocks)):
        y = 20 - blocks[i][1][1]//blockSize
        n = y - len(blockList) - 1
        if n >= 0:
            for j in range(n):
                blockList.append([])
            blockList.append([blocks[i]])
        else:
            if len(blockList[y-1]) > 0:
                for k in range(len(blockList[y-1])): #SORT IT
                    if blocks[i][1][0] < blockList[y-1][k][1][0]:
                        blockList[y-1].insert(k, blocks[i])
                        break
                    elif k == len(blockList[y-1]) - 1:
                        blockList[y-1].append(blocks[i])
            else:
                blockList[y-1].append(blocks[i])

def AddToDropList():
    blockFX.clear()
    k = -1
    if tetrisLines[0] > 1:
        i = tetrisLines[0]-1
    else:
        i = tetrisLines[0]
        
    while len(blockList) > i:
        k += 1
        x = blockList[i][0][1][0]
        dropList.append([blockList[i][0]])

        for j in range(1, len(blockList[i])):
            if abs(blockList[i][j][1][0] - x) == blockSize:
                x = blockList[i][j][1][0]
                dropList[k].append(blockList[i][j])
            else:
                k += 1
                x = blockList[i][j][1][0]
                dropList.append([blockList[i][j]])

        blockList.pop(i)
        
def GetBombedRow(i,x,y,z):
    bFound = False
    if x < gridWidth:  #LEFT SIDE
        x -= blockSize
        for j in range(len(blockList[z-1])):
            if [x,y] in blockList[z-1][j]:
                bombList.append([blockList[z-1][j][2], blockList[z-1][j][1]])
                blockList[z-1].pop(j)
                bFound = True
                while j > 0:
                    j -= 1
                    x -= blockSize
                    if [x,y] in blockList[z-1][j]:
                        bombList.append([blockList[z-1][j][2], blockList[z-1][j][1]])
                        blockList[z-1].pop(j)
                        continue
                    break
                break
            
        x = shape[i][1][0]
        
    if x >= 0:          #RIGHT SIDE
        x += blockSize
        for j in range(len(blockList[z-1])):
            if [x,y] in blockList[z-1][j]:
                bombList.append([blockList[z-1][j][2], blockList[z-1][j][1]])
                blockList[z-1].pop(j)
                bFound = True
                while j < len(blockList[z-1]):
                    x += blockSize
                    if [x,y] in blockList[z-1][j]:
                        bombList.append([blockList[z-1][j][2], blockList[z-1][j][1]])
                        blockList[z-1].pop(j)
                        continue
                    break
                break

    return bFound
    
def SetPointsDat(points):
    pointsMsg = pointFont.render(str(points), True, BLACK)
    pointsRect = pointsMsg.get_rect()
    pointsDat[0] = points
    if shape != []:
        centerx = gridLocX + shape[1][1][0] + blockSize//2
        if tetrisLines != []:
            top = gridLocY + (18 - tetrisLines[-1]) * blockSize
        else:
            top = gridLocY + shape[1][1][1]
        pointsDat[2] = outlineColors[tetrisColors.index(shape[1][2])]
    else:
        centerx = pointsDat[1].centerx
        top = pointsDat[1].top

    left = centerx - pointsRect.width//2
    if left < gridLocX:
        centerx += gridLocX - left
    else:
        right = left + pointsRect.width
        gridRight = gridLocX + blockSize*10
        if right > gridRight:
            centerx += gridRight - right
        
    if top < gridLocY:
        top = gridLocY
    
    pointsRect.centerx = centerx
    pointsRect.top = top
    pointsDat[1] = pointsRect
    pointsDat[3] = 255

def GetBombedList():
    for i in range(4):
        x = shape[i][1][0]
        y = shape[i][1][1]
        z = 20 - y//blockSize
        if z <= len(blockList): #LEFT-RIGHT
            if GetBombedRow(i,x,y,z):
                if (z-1) not in tetrisLines:
                    tetrisLines.append(z-1)
            
        if z > 1 and z <= len(blockList)+1: #BOTTOM
            z -= 1
            y += blockSize
            for j in range(len(blockList[z-1])):
                if [x,y] in blockList[z-1][j]:
                    bombList.append([blockList[z-1][j][2], blockList[z-1][j][1]])
                    blockList[z-1].pop(j)
                    GetBombedRow(i,x,y,z)
                    if (z-1) not in tetrisLines:
                        tetrisLines.append(z-1)
                    break

    #for i in range(4):
        bombList.append([shape[i][2], shape[i][1]])
    SetPointsDat(0)
    shape.clear()

def CheckTetris():
    global score, level, lines, rate
    
    bonus = len(tetrisLines)
    tetrisLines.clear()
    for i in range(len(blockList)):
        if len(blockList[i]) == 10:
            tetrisLines.append(i)

    nTetris = len(tetrisLines)
    if nTetris > 0:
        #blockSound.play(ts_break)
        if nTetris <= 4:
            scoreSound.play(ts_tetris[nTetris-1])
        else:
            scoreSound.play(ts_tetris[4])

        points = 100 * (nTetris + bonus)**2
        
        SetPointsDat(points)
        score += points
        lineLevel = lines//10
        lines += nTetris
        if lines//10 != lineLevel:
            level += 1
            score += bombs * 100 #v2.5
            if level < 30:
                nextRate = 31 - level
                if rate > nextRate:
                    rate = nextRate
                
        DrawScore()
        return True
    return False

def GetTetrisEffect(numLines):
    #global tetrisEffect, dIndex
    if len(tetrisLines) < 4:
        return randint(1,2)
    return 4

score = 0
level = 0
lines = 0
def DrawScore():    
    SCORE.fill(colorList[colScheme])
    pygame.draw.rect(SCORE, outlineColors[colScheme], SCORE.get_rect(), 5)

    SCORE.blit(scoreTitle, scoreTitle.get_rect(center = (scoreWidth//2, blockSize)))
    scoreText = font.render(str(score), True, WHITE)
    SCORE.blit(scoreText, scoreText.get_rect(center = (scoreWidth//2, blockSize*2)))

    SCORE.blit(levelTitle, levelTitle.get_rect(center = (scoreWidth//2, blockSize*4)))
    levelText = font.render(str(level), True, WHITE)
    SCORE.blit(levelText, levelText.get_rect(center = (scoreWidth//2, blockSize*5)))

    SCORE.blit(linesTitle, linesTitle.get_rect(center = (scoreWidth//2, blockSize*7)))
    linesText = font.render(str(lines), True, WHITE)
    SCORE.blit(linesText, linesText.get_rect(center = (scoreWidth//2, blockSize*8)))

def DrawNext(n):
    global monoColor #v2.5

    NEXT.fill(colorList[colScheme])
    pygame.draw.rect(NEXT, outlineColors[colScheme], NEXT.get_rect(), 5)
    
    NEXT.blit(nextTitle, nextTitle.get_rect(center = (nextWidth//2, blockSize)))
    if colScheme == 7: #v2.5
        monoColor = randint(0,1)
        if monoColor == 0:
            next = nextListGrey[n[0]][n[1]-1]
        else:
            next = nextListWhite[n[0]][n[1]-1]
    else:
        next = nextList[n[0]][n[1]-1]
    NEXT.blit(next, next.get_rect(center = (nextWidth//2, int(blockSize*3.5))))
    
    NEXT.blit(bombsTitle, bombsTitle.get_rect(center=(nextWidth//2, int(blockSize*6.5))))
    if bombs != -1:
        bombsText = font.render(str(bombs), True, WHITE)
        NEXT.blit(bombsText, bombsText.get_rect(center=(nextWidth//2, int(blockSize*7.5))))

screenShake = [0, 0]
def DrawDisplay():
    #global explode
    pointsMsg = None

    if bombedList != [] or screenShake[0] != 0 or hotList != []:
        updateRects.append(Rect(0,0,displayWidth,displayHeight)) #v2.5

        if screenShake[0] > 0:
            screenShake[0] -= 1
            screenShake[1] -= 1

        if screenShake[0] == 0:
            #explode = -1
            shakeX = 0
            shakeY = 0
        else:
            shakeX = int(-screenShake[0] + 2*random()*screenShake[0])
            shakeY = int(-screenShake[1] + 2*random()*screenShake[1])
        
        
        if flash == 1:
            if tetrisEffect == 4 and colScheme < 7: #v2.5
                DISPLAY.fill(outlineColors[randint(0,6)])
            else:
                DISPLAY.blit(colorSrc['white'], (shakeX, shakeY))
            if not bBombed:
                pointsMsg = pointFont.render(str(pointsDat[0]), True, WHITE)
                    
        elif flash == 0:
            DISPLAY.blit(colorSrc['black'], (shakeX, shakeY))
            DISPLAY.blit(frame, (shakeX+gridLocX-blockSize, shakeY+gridLocY-blockSize))
            if not bBombed:
                DISPLAY.blit(tetrisOut, tetrisOut.get_rect(right=displayWidth//2-blockSize*7, top=displayHeight//2+blockSize*2))
                DISPLAY.blit(tetrisOut, tetrisOut.get_rect(left=displayWidth//2+blockSize*7, top=displayHeight//2+blockSize*2))
                if bCombo:
                    DISPLAY.blit(combo, combo.get_rect(right=displayWidth//2-int(blockSize*6.5), top=displayHeight//2+blockSize*6))
                    DISPLAY.blit(combo, combo.get_rect(left=displayWidth//2+int(blockSize*6.5), top=displayHeight//2+blockSize*6))
                    pointsMsg = pointFont.render(str(pointsDat[0]), True, outlineColors[randint(0,6)])
                else:
                    pointsMsg = pointFont.render(str(pointsDat[0]), True, pointsDat[2])
        else:
            if backdropRect.bottom < displayHeight: #v2.2
                DISPLAY.blit(colorSrc['black'], (0,0))
            DISPLAY.blit(backdrop, (backdropRect.left+shakeX, backdropRect.top+shakeY))
            DISPLAY.blit(frame, (shakeX+gridLocX-blockSize, shakeY+gridLocY-blockSize))
        DISPLAY.blit(GRID,(gridLocX+shakeX, gridLocY+shakeY))
        DISPLAY.blit(SCORE,(gridLocX+gridWidth+blockSize*2+shakeX, gridLocY+blockSize+shakeY)) #(1248,108))
        DISPLAY.blit(NEXT,(gridLocX-blockSize*7+shakeX, gridLocY+blockSize+shakeY)) #(432,108))
        

        i = 0
        while i < len(hotList):
            if hotList[i].state == 'disintegrate':
                if hotList[i].disintegrate() == 'destroy':
                    del hotList[i]
                    continue
            elif hotList[i].state == 'heat':
                hotList[i].heat(heatAlpha)

            if hotList[i].location[1] > gridLocY:
                DISPLAY.blit(hotList[i].image, (hotList[i].blockRect.left+shakeX, hotList[i].blockRect.top+shakeY))
            i += 1

        # Gotta sort this shit constantly... Insertion!
        bombLen = len(bombedList)
        if bombLen > 1:
            for i in range(1, bombLen):
                for j in range(i):
                    if bombedList[i].scale < bombedList[j].scale:
                        bombedList.insert(j, bombedList[i])
                        bombedList.pop(i+1)
                        break

        i = 0
        while i < bombLen:
            x = bombedList[i].location[0]+gridLocX
            y = bombedList[i].location[1]+gridLocY
            if y > displayHeight or x < -blockSize*bombedList[i].scale or x > displayWidth:
                del bombedList[i]
                bombLen = len(bombedList)
                continue
            DISPLAY.blit(bombedList[i].image, (x,y))
            bombedList[i].update()
            
            for j in range(bombLen): # Check collision between flying blocks!
                if i != j and not bombedList[j].bCollided:
                    dist = list( map(sub, bombedList[i].location, bombedList[j].location) )
                    size = bombedList[i].scale * blockSize
                    if( 
                        abs(dist[0]) < size and abs(dist[1]) < size
                        and abs(bombedList[i].scale-bombedList[j].scale) < 1.5
                    ):
                        pygame.mixer.Sound.play(ts_clinks[randint(0,2)])
                        bombedList[i].collideWith(bombedList[j], [x//1.5 for x in dist])
                        
            i += 1

    else:
        #if outHots != []:
        #    DISPLAY.blit(frame, (gridLocX-blockSize, gridLocY-blockSize))
        DISPLAY.blit(GRID,(gridLocX, gridLocY))
        DISPLAY.blit(SCORE,(gridLocX+gridWidth+blockSize*2, gridLocY+blockSize)) #(1248,108))
        DISPLAY.blit(NEXT,(gridLocX-blockSize*7, gridLocY+blockSize)) #(432,108))
        updateRects.append(Rect(gridLocX, gridLocY, gridWidth, gridHeight))
        updateRects.append(Rect(gridLocX+gridWidth+blockSize*2, gridLocY+blockSize, scoreWidth, scoreHeight))
        updateRects.append(Rect(gridLocX-blockSize*7, gridLocY+blockSize, nextWidth, nextHeight))
        
    if pointsDat[0] != 0:
        if pointsMsg == None:
            pointsMsg = pointFont.render(str(pointsDat[0]), True, pointsDat[2])
            pointsMsg.fill((255,255,255,pointsDat[3]), None, BLEND_RGBA_MULT)
            pointsDat[3] -= 17
            pointsMove = pointsDat[1].top - max(blockSize//12, 1)
        else:
            pointsMove = pointsDat[1].top - max(blockSize//6, 1)

        if pointsMove >= gridLocY:
            pointsDat[1].top = pointsMove

        if pointsDat[3] > 0:
            DISPLAY.blit(pointsMsg,  pointsDat[1]) #v2.2
        else:
            pointsDat[0] = 0
        
        
nextShapes = []
def SpawnShape():
    global bMoved
    global shapeType, iRot
    global nextShapes

    switch = {
        0: gen7,
        1: gen7,
        2: genT,
        3: gen4,
        4: gen4,
        5: genBar,
        6: genBox
    }

    bMoved = False
    dropFX.clear()
    tetrisLines.clear()
    shape.clear()
    rotOffsets.clear()
    rotProxy.clear()
    #pointsDat.clear()
    iRot = 0

    if not pygame.mixer.music.get_busy(): #v2.2
        PlayNextTrack(False)

    if nextShapes == []:
        n = randint(0,6)
    else:
        n = nextShapes[0][0]
        DelayFrames(12)

    shapeType = n
    gen = switch.get(n)
    gen(blockSize, gridWidth//2, colScheme+monoColor, n==1 or n==4) #v2.5
        
    if nextShapes == []:
        if len(rotOffsets) > 0:
            for i in range(randint(0,3)):
                RotateShape(0, False)
        nextShapes.append((n, iRot))
    else:
        for i in range(nextShapes[0][1]):
            RotateShape(0, False)

    if len(nextShapes) == 1:
        shapeList = [0,1,2,3,4,5,6]
        shapeList.pop(shapeList.index(n))
        for i in range(6):
            r = randint(0,len(shapeList)-1)
            nextShapes.append((shapeList[r], randint(0, len(nextList[shapeList[r]])-1)))
            shapeList.pop(r)

    nextShapes.pop(0)
    DrawNext(nextShapes[0])

def AddDropFX(dropDist):
    left = gridWidth
    top = gridHeight
    for i in range(4):
        if shape[i][1][0] < left:
            left = shape[i][1][0]
        if shape[i][1][1] < top:
            top = shape[i][1][1]

    drop = GetNextList(colScheme, shape[0][2])[shapeType][iRot-1].copy() #v2.5
    if dropDist != 0:
        drop = pygame.transform.scale(drop, (drop.get_rect().width, dropDist+drop.get_rect().height))
    drop.set_alpha(150)
    dropFX.append([drop, [left, top], 150])
    

def SmashBlocks(bCentered, bQuad):
    screenShake[0] = blockSize//2
    screenShake[1] = blockSize//2
    shift = (-1, 1)
    n = len(bombList)
    biggestScaler = 0
    space = blockSize/48

    if bCentered:
        bombSound.play(ts_endsmash)
        shapePos = 4
    else:
        bombSound.play(ts_smashing)
        shapePos = int(bombList[n-1][1][0]/blockSize)
    
    for i in range(n):
        #if i < n-4:
        deltaX = int(bombList[0][1][0]/blockSize) - shapePos
        if deltaX == 0:
            deltaX += shift[randint(0,1)]
        x = int(deltaX * (8 + random()*4) * space)
        scaleOffset = 0.03 + 0.03/abs(deltaX)*random()
        '''else:
            if i < n-2:
                x = int(6 + random()*12)
            else:
                x = int(-6 - random()*12)
            scaleOffset = 0.05 + 0.15/abs(x)*random()
            x *= 4'''
        
        if bQuad:
            state = 'fly hot'
            y = int((-72 - randint(0,48)) * space)
        else:
            state = 'fly'
            y = int((-24 - randint(0,48)) * space)

        if random() < 0.5:
            rotation = int(6 + random()*24)
        else:
            rotation = int(-6 - random()*24)
        
        block = Block(state, bombList[0][0], bombList[0][1], [x,y], rotation, scaleOffset, 0, space)
        bombedList.append(block)
        '''
        #SORT THIS SHIT!
        if scaleOffset < biggestScaler:
            for j in range(len(bombedList)): #range(n-i, n):
                if scaleOffset < bombedList[j].scaleOffset:
                    bombedList.insert(j, block)
                    break
        else:
            biggestScaler = scaleOffset
            bombedList.append(block)
        '''  
        bombList.pop(0)
        
def GameStarted(bRollCredits):
    global bMoved, bDrop, bBomb, bBombed, bTetris, bDropBlocks, bCombo
    global heatAlpha, explode, bombs
    global flash, tetrisEffect
    global updateRects #v2.5

    #Initialization ==================================
    SetGameplay()

    graphics = InitSettings('graphics')
    SetGraphics(graphics[0], graphics[1], graphics[2], graphics[3])
    
    if bRollCredits: #v2.4
        RollCredits(False)
        return
    
    PlayNextTrack(True)
    
    SetControls()
    #=================================================
    mousePos = pygame.mouse.get_pos()
    SpawnShape()

    DISPLAY.blit(backdrop, backdropRect)
    DISPLAY.blit(frame, (gridLocX-blockSize, gridLocY-blockSize))
    DrawScore()

    bWait = False
    bGameOver = False
    bDrop = False
    bBomb = False
    bBombed = False
    bLanded = False
    bTetris = False
    bDropBlocks = False
    bCombo = False
    tickMove = 0
    tick = 0
    d = 0 #Tetris effect counter
    tetrisEffect = 0
    explode = -1
    flash = -1 #Screen flash
    dIndex = 0
    heatAlpha = 0
    updateRects = [] #v2.5

    #v2.5
    DrawDisplay()
    pygame.display.flip()
    pygame.time.Clock().tick(FPS)

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if Paused(False) == 'quit':
                        #ResetGame(True)
                        return True
                    #pygame.mouse.set_pos(mousePos)
                        
                elif event.key == K_F4 and pygame.key.get_pressed()[K_LALT]: #Alt+F4
                    pygame.quit()
                    sys.exit()
                #elif not bGameOver and not bTetris:
                elif shape != []:
                    if event.key == rotateKey:
                        if len(rotOffsets) > 0:
                            tick = RotateShape(tick, True)
                    elif event.key == dropKey:
                        bDrop = True
                    elif event.key == leftKey or event.key == rightKey:
                        tickMove = 1
                    elif event.key == bombKey:
                        if bombs > 0 and bombList == []:
                            bBomb = not bBomb
                            if bBomb:
                                AddToHotList('pulse', shape, 2)
                            else:
                                del hotList[:]
                            heatAlpha = 0

            elif event.type == MOUSEBUTTONDOWN:
                if shape != []:
                    if len(rotOffsets) > 0 and (event.button == 4 or event.button == 5):
                        tick = RotateShape(tick, True)
                    elif not bDrop and event.button == 3:
                        bDrop = True
                    elif bombs > 0 and event.button == 1:
                        bBomb = not bBomb
                        if bBomb:
                            AddToHotList('pulse', shape, 2)
                        else:
                            del hotList[:]
                        heatAlpha = 0

            elif event.type == KEYUP:
                if event.key == dropKey and dropMode == 1 and bDrop:
                    bDrop = False
            elif event.type == MOUSEBUTTONUP:
                if event.button == 3 and dropMode == 1 and bDrop:
                    bDrop = False

            elif event.type == NEXT_TRACK: #v2.4 Reinstated --IF UNRELIABLE: Use pygame.mixer.music.get_busy() in SpawnShape()
                PlayNextTrack(False)
                
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()


        GRID.blit(grid, (0,0))
        if not bTetris:
            tickMove = (tickMove + 1) % 2
            if tickMove == 0 or bDrop:
                keys = pygame.key.get_pressed()
                mPos = list(pygame.mouse.get_pos())
                
                if keys[leftKey] or mPos[0] < mousePos[0]-blockSize//4:
                    MoveBlocks(shape, -blockSize,0)
                if keys[rightKey] or mPos[0] > mousePos[0]+blockSize//4:
                    MoveBlocks(shape, blockSize,0)
                '''
                if dropMode == 1 and keys[dropKey] or mPos[1] > mousePos[1]+blockSize//2 or rate==1:
                    bDrop = True
                
                elif rotOffsets != [] and mPos[1] < mousePos[1]-blockSize//2:
                    bDrop = False
                    RotateShape(True)
                '''
                if mPos[0] < gridLocX:
                    mPos[0] = gridLocX+gridWidth
                    pygame.mouse.set_pos(mPos)
                    
                elif mPos[0] > gridLocX+gridWidth:
                    mPos[0] = gridLocX
                    pygame.mouse.set_pos(mPos)
                    
                elif mPos[1] < gridLocY:
                    mPos[1] = gridLocY+gridHeight
                    pygame.mouse.set_pos(mPos)
                    
                elif mPos[1] > gridLocY+gridHeight:
                    mPos[1] = gridLocY
                    pygame.mouse.set_pos(mPos)
                    
                mousePos = mPos

            tick = (tick + 1) % rate
            if tick == 0 or bDrop:
                if bDrop:
                    if dropMode == 0: # Instant Drop
                        dist = 0
                        bCollided = False
                        for i in range(20):
                            dist += blockSize
                            for j in range(4):
                                if GetCollision(shape[j][1][0], shape[j][1][1]+dist) != '':
                                    bCollided = True
                                    dist -= blockSize
                                    break
                            if bCollided:
                                break

                        if dist > 0:
                            bWait = True
                            whooshSound.play(ts_whoosh[randint(0,1)])
                            AddDropFX(dist)
                            if not bMoved:
                                bMoved = True
                            bDrop = False
                            tick = 0
                            for i in range(4):
                                shape[i][1][1] += dist
                            dist = 0
                        else:
                            bLanded = True

                        
                    else:
                        AddDropFX(0)
                        bLanded = MoveBlocks(shape, 0,blockSize)
                else:
                    bLanded = MoveBlocks(shape, 0, blockSize)

                if not bMoved and not bLanded:
                    bMoved = True

            #Bomb Pulse
            if bBomb:
                for i in range(4):
                    x = shape[i][1][0] + gridLocX + blockSize//2
                    y = shape[i][1][1] + gridLocY + blockSize//2
                    hotList[i].pulse([x,y])
            '''if bBomb:
                if bPulse:
                    if heatAlpha < 255:
                        heatAlpha += 15
                    else:
                        bPulse = False
                else:
                    if heatAlpha > 127:
                        heatAlpha -= 15
                    else:
                        bPulse = True'''

            if bLanded:
                bLanded = False
                if bDrop:
                    #bDrop = False
                    pygame.mixer.Sound.play(ts_drop)
                    dropFX.clear()
                else:
                    pygame.mixer.Sound.play(ts_set)
                    
                if bMoved:
                    if bBomb:
                        del hotList[:]
                        bBombed = True
                        bTetris = True
                        GetBombedList()
                        bombs -= 1
                        if bDrop:
                            SmashBlocks(False, False)
                            bBomb = False
                            flash = 1
                            bDropBlocks = True
                            numLines = len(tetrisLines)
                            if numLines > 0:
                                tetrisLines.sort()
                                for i in range(numLines):
                                    if len(blockList[tetrisLines[i]]) == 0:
                                        blockList.pop(tetrisLines[i])
                                        for j in range(i+1, numLines):
                                            tetrisLines[j] -= 1
                                AddToDropList()
                            '''else:
                                bBombed = False
                                bTetris = False
                                SpawnShape()'''
                        else:
                            explode = 0
                            bombSound.play(ts_charge)
                            heatAlpha = 99
                            AddToHotList('heat', bombList, 0)
                    else:
                        AddToBlockList(shape)
                        bTetris = CheckTetris()
                        if bTetris:
                            shape.clear()
                            tetrisEffect = GetTetrisEffect(len(tetrisLines))
                            effectDir = -1
                            if not bDrop:
                                explode = 0
                            else:
                                explode = 1
                        else:
                            SpawnShape()
                            
                else: #GAME OVER
                    bGameOver = True
                    pygame.mixer.music.stop()
                    pygame.time.set_timer(GAMEOVER, 5700)
                    scoreSound.play(ts_gameover)

                bDrop = False
                bDropped = False
                
        else: # Tetris/Bombing Event
            if not bDropBlocks:
                numLines = len(tetrisLines)
                if not bBombed:
                    flash = (flash+1) % 2
                    if tetrisEffect < 4:
                        if effectDir == -1:
                            if random() < 0.5:
                                effectDir = 1
                            else:
                                effectDir = 0
                        for i in range(numLines):
                            if len(blockList[tetrisLines[i]]) > 0:
                                '''if tetrisEffect > 1:
                                    blockFX.append([blockList[tetrisLines[i]][0][2], blockList[tetrisLines[i]][0][1]])
                                else:
                                    GRID.blit(blocks[blockList[tetrisLines[i]][0][2]][1], tuple(blockList[tetrisLines[i]][0][1]))
                                
                                if tetrisEffect == 2:
                                    dIndex = randint(0, len(blockList[tetrisLines[i]])-1)'''
                                if tetrisEffect == 1:
                                    if effectDir == 1:
                                        dIndex = len(blockList[tetrisLines[i]])//2
                                    else:
                                        dIndex = -flash
                                else:
                                    if effectDir == 1:
                                        dIndex = len(blockList[tetrisLines[i]]) - 1
                                    else:
                                        dIndex = 0

                                if explode == 0:
                                    bombSound.play(ts_smashing)
                                    hotCentre = blockList[tetrisLines[i]][dIndex][1]
                                    hotCentre[0] += gridLocX + blockSize//2
                                    hotCentre[1] += gridLocY + blockSize//2
                                    hotList.append(Block('disintegrate', blockList[tetrisLines[i]][dIndex][2], hotCentre, [], 0, 0.05, 255, 0))
                                else:
                                    bombList.append([blockList[tetrisLines[i]][dIndex][2], blockList[tetrisLines[i]][dIndex][1]])
                                    if i == numLines-1:
                                        SmashBlocks(True, False)

                                blockList[tetrisLines[i]].pop(dIndex)
                            else:
                                blockList.pop(tetrisLines[i])
                                for j in range(i+1, numLines):
                                    tetrisLines[j] -= 1
                                if i == numLines-1:
                                    bombSound.play(ts_disintegrate[explode])
                                    explode = -1
                                    DISPLAY.blit(backdrop, backdropRect)
                                    DISPLAY.blit(frame, (gridLocX-blockSize, gridLocY-blockSize))
                                    bDropBlocks = True

                    
                    else:
                        if d < 7:
                            if bombList == []:
                                for i in range(numLines):
                                    for j in range(10):
                                        bombList.append([blockList[tetrisLines[i]][0][2], blockList[tetrisLines[i]][0][1]])
                                        #blockList[tetrisLines[i]][j][0] = blocks[tetrisColors[d-7]][0]
                                        blockList[tetrisLines[i]].pop(0)

                                    blockList.pop(tetrisLines[i])
                                    for j in range(i+1, numLines):
                                        tetrisLines[j] -= 1

                                AddToHotList('heat', bombList, 0)
                                bBomb = True

                            if flash == 1:
                                heatAlpha = 255
                                if tetrisEffect == 4:
                                    if colScheme == 7 : #v2.5
                                        for i in range(len(hotList)):
                                            hotList[i].color = tetrisColors[randint(7,8)]
                                    else:
                                        for i in range(len(hotList)):
                                            hotList[i].color = tetrisColors[d]
                                #    DISPLAY.fill(colorList[d])
                                #else:
                                #    DISPLAY.blit(colorSrc['white'], (0,0)) --Handled in DrawDisplay()
                            else:
                                heatAlpha = 127
                                d += 1
                        else:
                            DISPLAY.blit(backdrop, backdropRect)
                            DISPLAY.blit(frame, (gridLocX-blockSize, gridLocY-blockSize))
                            d = 0
                            #if tetrisEffect == 4:
                            bQuad = True
                            if numBombs != -1:
                                bombs += 1
                            if colScheme == 7: #v2.5
                                for i in range(len(hotList)):
                                    hotList[i].color = tetrisColors[randint(7,8)]
                            else:
                                for i in range(len(hotList)):
                                    hotList[i].color = tetrisColors[randint(0,6)]
                            #else:
                            #    bQuad = False
                                    
                            bBomb = False
                            if explode != 0:
                                explode = -1
                                heatAlpha = 0
                                bDropBlocks = True
                                SmashBlocks(True, bQuad)
                                pygame.mixer.Sound.play(ts_blast[min(numLines-4, 1)])
                                del hotList[:]
                            else:
                                flash = -1
                                heatAlpha = 255
                                bBombed = True
                                bombSound.play(ts_disintegrate[1])
                                HotListState('disintegrate')
                                pygame.mixer.Sound.play(ts_blast[0])
                            bombList.clear()

                    '''else:
                        if d == 0:
                            tetris4Pos = tuple(blockList[tetrisLines[3]][0][1])
                            for i in range(numLines):
                                blockList.pop(tetrisLines[i])
                                for j in range(i+1, numLines):
                                    tetrisLines[j] -= 1

                        if d < 14:
                            GRID.blit(tetris4Blocks[d-7], tetris4Pos)
                            d += 1
                        else:
                            d = 0
                            bDropBlocks = True'''

                elif bBomb: #Disintegrating charge
                    heatAlpha += 5
                    if heatAlpha > 240:
                        bombSound.play(ts_disintegrate[1]) #(ts_disintegrate)
                        HotListState('disintegrate')
                        heatAlpha = 255
                        bBomb = False
                        bombList.clear()
                        if numLines > 0:
                            tetrisLines.sort()
                            for i in range(numLines):
                                if len(blockList[tetrisLines[i]]) == 0:
                                    blockList.pop(tetrisLines[i])
                                    for j in range(i+1, numLines):
                                        tetrisLines[j] -= 1
                                        
                    #heatBlock.set_alpha(heatAlpha)
                
                else: #DISINTEGRATE
                    heatAlpha -= 32
                    if heatAlpha < 32:
                        explode = -1
                        heatAlpha = 0
                        if numLines > 0:
                            bDropBlocks = True
                        else:
                            bBombed = False
                            bTetris = False
                            SpawnShape()
                    
                if bDropBlocks: #Split falling blocks into dropList
                    AddToDropList()
                        
            else: #Drop the remaining blocks
                flash = -1 #(flash+1) % 2
                i = 0
                while i < len(dropList):
                    if MoveBlocks(dropList[i], 0,blockSize):
                        if bDropped:
                            pygame.mixer.Sound.play(ts_set)
                        AddToBlockList(dropList[i])
                        dropList.pop(i)
                    else:
                        i += 1
                bDropped = True
                if dropList == []:
                    bBombed = False
                    bDropBlocks = False
                    if not CheckTetris():
                        bCombo = False
                        bTetris = False
                        if endLevel != -1 and level == endLevel: # YOU WIN!
                            if EndGame():
                                break
                        else:
                            SpawnShape()
                    else: # COMBO
                        bCombo = True
                        if numBombs != -1:
                            bombs += 1
                        tetrisEffect = GetTetrisEffect(len(tetrisLines))
                        effectDir = -1
                        explode = 1
                        DrawNext(nextShapes[0])


        DrawBlocks()
        DrawDisplay()
        
        if bGameOver:
            bGameOver = False
            if GameOver():
                break
        elif bWait:
            bWait = False
            pygame.time.wait(100)
            
        pygame.display.update(updateRects); updateRects.clear() #v2.5 update frame
        pygame.time.Clock().tick(FPS)


def EndGame():
    global heatAlpha #, creditRollRect

    pygame.mixer.music.stop()
    #pygame.mixer.music.set_endevent()

    #endingLevel = endLevel

    # The ultimate Tetris megabomb!
    megaBombMap = GetMegaBombMap(randint(0,3), colScheme==7)

    shape.clear()
    for i in range(20):
        for j in range(10):
            shape.append([blocks[megaBombMap[i][j]], [blockSize*j, -blockSize*(i+1)], megaBombMap[i][j]])
    
    updateRects.clear() #v2.5
    while shape[0][1][1] < blockSize*19:
        GRID.blit(grid, (0,0))
        
        # Move the shit
        pygame.mixer.Sound.play(ts_move)
        for i in range(len(shape)):
            shape[i][1][1] += blockSize

        # Check collision
        if blockList != []:
            t = len(blockList)-1
            for i in range(len(blockList[t])):
                if shape[0][1][1] == blockList[t][i][1][1]:
                    for j in range(len(blockList[t])):
                        bombList.append([blockList[t][j][2], blockList[t][j][1]])
                    blockList.pop(t)
                    #explode = 1
                    SmashBlocks(True, False)
                    break
        
        bQuitToMain = EndMenuInput()
        if bQuitToMain == True:
            return True
        elif bQuitToMain == False:
            return False

        DrawBlocks()
        DrawDisplay()
        pygame.display.update(updateRects); updateRects.clear() #v2.5 update frame
        pygame.time.Clock().tick(FPS)
    
    pygame.mixer.Sound.play(ts_smashing)
    pygame.time.wait(35)
    pygame.mixer.Sound.play(ts_drop)
    screenShake[0] = blockSize
    screenShake[1] = blockSize
    tick = 0
    while tick < 60: # Wait for it...
        GRID.blit(grid, (0,0))

        tick += 1

        bQuitToMain = EndMenuInput()
        if bQuitToMain == True:
            return True
        elif bQuitToMain == False:
            return False

        DrawBlocks()
        DrawDisplay()
        pygame.display.update(updateRects); updateRects.clear() #v2.5 update frame
        pygame.time.Clock().tick(FPS)

    # Blow this shit up to high hell!
    #ts = time.time()
    ending = randint(0,2)
    if ending == 0:
        frameLag = 46 #42
        heatAlpha = 0
        for i in range(len(shape)):
            bombList.append([shape[i][2], shape[i][1]])
        AddToHotList('heat', bombList, 0)
        bombSound.play(ts_charge)
    elif ending == 1:
        frameLag = 5
        heatAlpha = 0
    else:
        frameLag = 1
    tenCount = 10
    tenIndex = -1
    while shape != []:
        GRID.blit(grid, (0,0))

        tick = (tick + 1) % frameLag
        if tick == 0:
            bombLen = len(shape)
            if frameLag == 1:
                if tenCount == 0:
                    tenCount = 10
                    if tenIndex == -1:
                        tenIndex = bombLen-10
                    else:
                        tenIndex = -1
                bombList.append([shape[tenIndex][2], shape[tenIndex][1]])
                tenCount -= 1
                del shape[tenIndex]
                SmashBlocks(True, True)
            else:
                heatAlpha = 0
                del hotList[:]
                SmashBlocks(True, True)
                if frameLag == 5:
                    del shape[bombLen-10 : bombLen]
                    bombLen = len(shape)
                    if bombLen > 0:
                        for i in range(bombLen-10, bombLen):
                            bombList.append([shape[i][2], shape[i][1]])
                        AddToHotList('heat', bombList, 0)
                else:
                    pygame.mixer.Sound.play(ts_blast[0])
                    pygame.mixer.Sound.play(ts_blast[1])
                    del shape[:]

        elif frameLag == 5:
            heatAlpha += 50
        else:
            heatAlpha += 5 #6


        bQuitToMain = EndMenuInput()
        if bQuitToMain == True:
            return True
        elif bQuitToMain == False:
            return False

        DrawBlocks()
        DrawDisplay()
        pygame.display.update(updateRects); updateRects.clear() #v2.5 update frame
        pygame.time.Clock().tick(FPS)
    #print(time.time()-ts)
    return RollCredits(True)

def RollCredits(bEndGame):
    global creditRollRect
    VICTORY = 29
    CREDITS = 30
    DROPTETRA = 31
    bChamp = False
    
    if bEndGame:
        bInputEnabled = False
        opacity = 256
        varFPS = int(FPS*0.4)
        pygame.time.set_timer(VICTORY, 3000)
        endingLevel = endLevel
        congrats = font.render('CONGRATULATIONS!', True, WHITE, BLACK)
        congratsRect = congrats.get_rect( center=(gridWidth//2, -blockSize) )
        if endingLevel < 10:
            chumpLineSrc = "What a chump!"
        elif endingLevel < 15:
            chumpLineSrc = "Whoop-dee-doo!"
        elif endingLevel < 20:
            chumpLineSrc = "Not bad..."
        elif endingLevel < 25:
            chumpLineSrc = "OKAY!"
        elif endingLevel < 29:
            chumpLineSrc = "Gettin' good..."
        elif endingLevel < 30:
            chumpLineSrc = "Ohh so close!"
        elif endingLevel < 31:
            chumpLineSrc = "What a champ!!"
        else:
            chumpLineSrc = "* A true champion *"
        chumpLine = ""
        chumpCount = 0
        champion = font.render(chumpLineSrc, True, WHITE, BLACK)
        championRect = champion.get_rect( center=(gridWidth//2, blockSize*10) )
        #champion.set_alpha(0)
        youReached = font.render("You've reached", True, WHITE, BLACK)
        youReachedRect = youReached.get_rect(center=(gridWidth//2, blockSize*7))
        levelNum = font.render("Level "+str(endingLevel), True, WHITE, BLACK)
        levelNumRect = levelNum.get_rect(center=(gridWidth//2, blockSize*8))
    else:
        GetCredits()
        creditRollRect = CREDITROLL.get_rect( left=gridLocX, top=displayHeight )
        bInputEnabled = True
        opacity = 0
        grid.set_alpha(0)
        varFPS = FPS
        pygame.time.set_timer(DROPTETRA, 600)
    

    bRollCredits = not bEndGame
    bRollAlready = False
    #bEnd = False

    '''
        ('Music Credits', '', 
            'Caspro', '"Goosebumps"', '', 
            'Daft Punk', '"End of Line"', '', 
            'Daft Punk', '"I Feel It Coming"', '', 
            'Jake Chudnow', '"Shona"', '', 
            'Mega Drive', '"I Am the Program"', '', 
            'Pixies', '"Where Is My Mind?"', '',
            'Sandman', '"Ignite"', '',
            'Scandroid', '"Thriller"', '',
            'Technomancer', '"Blade Runner"', '',
            'Terminite', '"Evolution"', '',
            'TUNEDEF', '"Justice"', '',
            'Mohd Izzuddin', '"Tetris Synthwave"', '', 
            'Akira Staff', '"Tetris 99"', '',
            'Nintendo', '"Victory Theme"'),
        ('Special thanks to', 'Alexey Pajitnov')
    )'''
    blockFX.clear()
    fadeOut = 255
    tick = 0
    while True:
        GRID.fill(BLACK)
        GRID.blit(grid, (0,0))
        
        if not bRollCredits:
            if not bChamp and opacity > 0:
                opacity -= 10
                grid.set_alpha(opacity)

            '''if varFPS != FPS and bombedList == []:
                varFPS = FPS
                pygame.time.set_timer(VICTORY, 1000)'''
            if bChamp:
                if congratsRect.centery < blockSize*5:
                    congratsRect.centery += 12
                else:
                    if opacity < 255:
                        opacity += 16

                    if chumpCount < len(chumpLineSrc):
                        chumpCount += 1
                        chumpLine = chumpLineSrc[:chumpCount]
                        champion = font.render(chumpLine, True, WHITE, BLACK)
                    else:
                        if colScheme == 7: #v2.5
                            fontColor = outlineColors[randint(7,8)]
                        else:
                            fontColor = outlineColors[randint(0,6)]
                        champion = font.render(chumpLine, True, fontColor, BLACK)
                    #champion.set_alpha(opacity)
                    GRID.blit(youReached, youReachedRect)
                    GRID.blit(levelNum, levelNumRect)
                    GRID.blit(champion, championRect)
                
                GRID.blit(congrats, congratsRect)
                #GRID.blit(champion, championRect)
        else:
            if opacity > 0 and creditRollRect.bottom > blockSize*8:
                opacity -= 16
                congrats.set_alpha(opacity)
                champion.set_alpha(opacity)
                youReached.set_alpha(opacity)
                levelNum.set_alpha(opacity)
                GRID.blit(congrats, congratsRect)
                GRID.blit(youReached, youReachedRect)
                GRID.blit(levelNum, levelNumRect)
                GRID.blit(champion, championRect)
            else:
                if creditRollRect.bottom > blockSize*8:
                    #GRID.blit(CREDITROLL, creditRollRect)
                    creditRollRect.top -= 2
                elif bEndGame:
                    if opacity < 255:
                        opacity += 8
                        thanksFor.set_alpha(opacity)
                        playing.set_alpha(opacity)

                    CREDITROLL.blit(thanksFor, thanksForRect)
                    CREDITROLL.blit(playing, playingRect)
                else:
                    pygame.time.set_timer(DROPTETRA, 0)
                    return #v2.4 Auto credit exit

        if bInputEnabled and not bRollCredits:
            tick += 1
            if tick >= FPS*4 or bRollAlready:
                bRollCredits = True
                if colScheme == 7: #v2.5
                    randColor = outlineColors[randint(7,8)]
                else:
                    randColor = outlineColors[randint(0,6)]
                congrats = font.render('CONGRATULATIONS!', True, randColor, BLACK)
                champion = font.render(chumpLine, True, randColor, BLACK)
                youReached = font.render("You've reached", True, randColor, BLACK)
                levelNum = font.render("Level "+str(endingLevel), True, randColor, BLACK)
                pygame.mixer.music.set_endevent(NEXT_TRACK) #v2.4
                PlayNextTrack(False)
                GetCredits()
                creditRollRect = CREDITROLL.get_rect( left=gridLocX, top=displayHeight )
                thanksFor = font.render('Thank you for', True, WHITE, BLACK)
                thanksForRect = thanksFor.get_rect( center=(gridWidth//2, creditRollRect.height-blockSize*2) )
                playing = font.render('playing', True, WHITE, BLACK)
                playingRect = playing.get_rect( center=(gridWidth//2, creditRollRect.height-blockSize) )
                pygame.time.set_timer(CREDITS, 2500)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if bInputEnabled:
                    if event.key == K_ESCAPE:
                        if not bEndGame: #v2.4
                            pygame.time.set_timer(DROPTETRA, 0)
                            pygame.mixer.Sound.play(ts_break)
                            return
                        prevHeight = displayHeight
                        option = Paused(bRollCredits and creditRollRect.top < displayHeight)
                        if option == 'quit':
                            if bRollCredits:
                                pygame.time.set_timer(CREDITS, 0)
                                pygame.time.set_timer(DROPTETRA, 0)
                            PlayNextTrack(False)
                            grid.set_alpha(255)
                            return True
                        elif option == 'restart':
                            if bRollCredits:
                                pygame.time.set_timer(CREDITS, 0)
                                pygame.time.set_timer(DROPTETRA, 0)
                            grid.set_alpha(255)
                            return False
                        elif option == 'setmode':
                            GetCredits()
                            congrats = font.render('CONGRATULATIONS!', True, WHITE, BLACK)
                            congratsRect = congrats.get_rect( center=(gridWidth//2, blockSize*5) )
                            champion = font.render(chumpLine, True, WHITE, BLACK)
                            championRect = champion.get_rect( center=(gridWidth//2, blockSize*10) )
                            youReached = font.render("You've reached", True, WHITE, BLACK)
                            youReachedRect = youReached.get_rect(center=(gridWidth//2, blockSize*7))
                            levelNum = font.render("Level "+str(endLevel), True, WHITE, BLACK)
                            levelNumRect = levelNum.get_rect(center=(gridWidth//2, blockSize*8))

                            grid.set_alpha(0)
                            if bRollCredits:
                                creditRollRect = CREDITROLL.get_rect( left=gridLocX, top=int(creditRollRect.top*displayHeight/prevHeight) )
                                thanksFor = font.render('Thank you for', True, WHITE, BLACK)
                                thanksForRect = thanksFor.get_rect( center=(gridWidth//2, creditRollRect.height-blockSize*2) )
                                playing = font.render('playing', True, WHITE, BLACK)
                                playingRect = playing.get_rect( center=(gridWidth//2, creditRollRect.height-blockSize) )

                    elif not bRollCredits:
                        bRollAlready = True

                if event.key == K_F4 and pygame.key.get_pressed()[K_LALT]: #Alt+F4
                    pygame.quit()
                    sys.exit()

            elif event.type == VICTORY:
                varFPS = FPS
                bChamp = True
                pygame.mixer.music.load("sounds/victory_theme.mp3")
                pygame.mixer.music.play()
                pygame.mixer.music.set_endevent(CREDITS)
                pygame.time.set_timer(VICTORY, 0)

            elif event.type == CREDITS:
                if bRollCredits:
                    pygame.time.set_timer(CREDITS, 0)
                    pygame.time.set_timer(DROPTETRA, 500)
                else:
                    TopTen()
                    bInputEnabled = True

            elif event.type == DROPTETRA:
                i = randint(0,6)
                nextShape = GetNextList(colScheme, randint(0,1))[i][randint(0,len(nextList[i])-1)].copy() #v2.5
                shapeRect = nextShape.get_rect()
                offsetX = randint(0, displayWidth//blockSize - shapeRect.width//blockSize) * blockSize
                blockFX.append([nextShape, [offsetX, -shapeRect.height]])
                alpha = 256
                for i in range(4):
                    drop = nextShape.copy()
                    alpha //= 2
                    drop.set_alpha(alpha)
                    blockFX.append([drop, [offsetX, -shapeRect.height-blockSize*(i+1)]])

            elif event.type == NEXT_TRACK: #v2.4
                PlayNextTrack(False)

            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        if bRollCredits:
            if fadeOut > 175:
                fadeOut -= 5
                NEXT.fill((fadeOut, fadeOut, fadeOut), None, BLEND_RGB_MULT)
                SCORE.fill((fadeOut, fadeOut, fadeOut), None, BLEND_RGB_MULT)
                #backdrop.fill((fadeOut, fadeOut, fadeOut), None, BLEND_RGB_MULT)

            DISPLAY.fill(BLACK)
            if creditRollRect.top < displayHeight:
                i = 0
                while i < len(blockFX):
                    if blockFX[i][1][1]+blockSize < displayHeight:
                        blockFX[i][1][1] += blockSize
                        DISPLAY.blit(blockFX[i][0], blockFX[i][1])
                        i += 1
                    else:
                        blockFX.pop(i)
                DISPLAY.blit(CREDITROLL, creditRollRect)
            else:
                if opacity > 0:
                    if backdropIndex != len(backdrops)-1:
                        backdrop.set_alpha(opacity)
                    frame.set_alpha(opacity)
                    DISPLAY.blit(backdrop, backdropRect)
                    DISPLAY.blit(frame, (gridLocX-blockSize, gridLocY-blockSize))
                DrawDisplay()
        else:
            DrawDisplay()
        pygame.display.flip()
        pygame.time.Clock().tick(varFPS)

def GetCredits():
    global CREDITROLL

    creditList = [
        ['Program Director'] + PROGRAM_DIRECTOR,
        ['Art Design'] + ART_DESIGN,
        ['Sound FX'] + SOUND_FX,
        ['Executive Advisors'] + EXECUTIVE_ADVISORS,
        ['Quality Assurance'] + QUALITY_ASSURANCE,
    ]
    creditLength = 0
    for i in range(len(creditList)):
        creditLength += len(creditList[i])

    musicCredits = ('Music Credits', '')
    musicList = GetMusicList()
    for i in range(len(musicList)):
        if ' - ' in musicList[i]:
            musicCredits += ('"'+musicList[i][musicList[i].index('-')+2:len(musicList[i])-4]+'"', musicList[i][:musicList[i].index('-')], '')
        else:
            musicCredits += (musicList[i][:len(musicList[i])-4], '', '')
    creditLength += len(creditList)*2 + len(musicList)*3 + 15
    creditList.append( musicCredits )
    creditList.append(('Special thanks to', 'Alexey Pajitnov', 'Henk Rogers'))
    CREDITROLL = pygame.transform.scale(colorSrc['black'].copy(), (gridWidth*3, blockSize*creditLength))
    CREDITROLL.set_colorkey(BLACK)
    #CREDITROLL = pygame.Surface((gridWidth*3, blockSize*creditLength))
    #CREDITROLL.fill(BLUE)
    creditPos = 0
    for i in range(len(creditList)):
        for j in range(len(creditList[i])):
            if j == 0:
                if colScheme == 7:
                    colour = GREY #v2.5
                else:
                    colour = outlineColors[i]
            else:
                colour = WHITE
            if j > 0 and i == len(creditList)-2:
                credit = smallFont.render(creditList[i][j], True, colour, BLACK)
            else:
                credit = font.render(creditList[i][j], True, colour, BLACK)
            if i < len(creditList)-1:
                creditRect = credit.get_rect( left=blockSize//2, top=creditPos )
            else:
                creditRect = credit.get_rect( center=(gridWidth//2, creditPos) )

            creditPos += blockSize
            CREDITROLL.blit(credit, creditRect)

        creditPos += blockSize*2

    #return creditList
    
def EndMenuInput():
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                option = Paused(False)
                if option == 'quit':
                    PlayNextTrack(False)
                    #ResetGame(True)
                    return True
                elif option == 'restart':
                    return False
                    
            elif event.key == K_F4 and pygame.key.get_pressed()[K_LALT]:
                pygame.quit()
                sys.exit()

        elif event.type == QUIT:
            pygame.quit()
            sys.exit()

def Paused(bCredits):
    global dropMode, endLevel

    pygame.mouse.set_visible(True)
    pygame.mixer.Sound.play(ts_drop)
    bSetMode = False
    InitOptions(blockSize/48, gridWidth//2, 0)
    option = ''
    while True:
        if bCredits:
            DISPLAY.fill(BLACK)
            DISPLAY.blit(CREDITROLL, creditRollRect)
        else:
            DISPLAY.blit(backdrop, backdropRect)
            DISPLAY.blit(frame, (gridLocX-blockSize, gridLocY-blockSize))
            GRID.blit(grid, (0,0))
            DrawBlocks()
            DrawDisplay()
        
        option = GameMenu(DISPLAY, GRID, option)
        if option == 'resume':
            pygame.mouse.set_visible(False)
            if bSetMode:
                return 'setmode'
            else:
                break
        elif option == 'restart':
            pygame.mouse.set_visible(False)
            ResetGame()
            DrawScore()
            PlayNextTrack(True)
            SpawnShape()
            return 'restart'
        elif option == 'main':
            ResetGame()
            return 'quit'
        elif option == 'setmode':
            bSetMode = True
            graphics = InitSettings('graphics')
            SetGraphics(graphics[0], graphics[1], graphics[2], graphics[3])
            DrawScore()
            DrawNext(nextShapes[0])
            InitOptions(blockSize/48, gridWidth//2, 0)
            option = 'options'
        elif option == 'keybind':
            SetControls()
            option = 'options'
        elif option == 'setgameplay':
            gameplay = InitSettings('gameplay')
            dropMode = gameplay[2]
            endLevel = gameplay[3]
            option = 'options'
        else:
            option = 'options'

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
        
def GameOver():
    bInputEnabled = False
    gameOver = font.render('GAME OVER', True, outlineColors[colScheme]) #v2.5
    gameOverFrame = Rect(gridWidth//2-blockSize*3, gridHeight//2-blockSize, blockSize*6, blockSize*2)
    GRID.fill(BLACK, gameOverFrame)
    GRID.blit(gameOver, gameOver.get_rect(center = (gridWidth//2, gridHeight//2)))
    DISPLAY.blit(GRID,(gridLocX, gridLocY))
    pygame.display.flip()
    while True:

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_F4 and pygame.key.get_pressed()[K_LALT]: #Alt+F4
                    pygame.quit()
                    sys.exit()
                elif bInputEnabled and event.key == K_ESCAPE:
                    option = Paused(False)
                    if option == 'quit':
                        PlayNextTrack(False)
                        #ResetGame(True)
                        return True
                    elif option == 'restart':
                        return False

                    gameOver = font.render('GAME OVER', True, outlineColors[colScheme]) #v2.5
                    gameOverFrame = Rect(gridWidth//2-blockSize*3, gridHeight//2-blockSize, blockSize*6, blockSize*2)
                    GRID.fill(BLACK, gameOverFrame)
                    GRID.blit(gameOver, gameOver.get_rect(center = (gridWidth//2, gridHeight//2)))
                    DISPLAY.blit(GRID, (gridLocX, gridLocY))
                    pygame.display.flip()

            elif event.type == GAMEOVER:
                pygame.time.set_timer(GAMEOVER, 0)
                bInputEnabled = True
                TopTen()
                bRestart = RestartMenu(DISPLAY, GRID)
                if bRestart == '':
                    GRID.blit(grid, (0,0))
                    DrawBlocks()
                else:
                    ResetGame()
                    if bRestart:
                        DrawScore()
                        SpawnShape()
                        return False
                    return True
                
                GRID.fill(BLACK, gameOverFrame)
                GRID.blit(gameOver, gameOver.get_rect(center = (gridWidth//2, gridHeight//2)))
                DISPLAY.blit(GRID, (gridLocX, gridLocY))
                pygame.display.flip()

            elif event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.time.Clock().tick(FPS)


def ResetGame():
    global bDrop, bBomb, bBombed, bTetris, bDropBlocks, bCombo
    global score, level, lines, bombsTitle
    global explode

    blockFX.clear()
    blockList.clear()
    nextShapes.clear()
    bDrop = False
    bBomb = False
    bBombed = False
    bTetris = False
    bDropBlocks = False
    bCombo = False
    score = 0
    level = 0
    lines = 0
    #heatBlock.set_alpha(255)
    #tetrisEffect = 0
    explode = -1
    bombList.clear()
    del hotList[:]
    # Reset and draw backdrop and frame for endgame case
    if backdropIndex != len(backdrops)-1: # Filled coloured backgrounds should not have opacity altered >> LAG ISSUE
        backdrop.set_alpha(255)
    frame.set_alpha(255)
    DISPLAY.blit(backdrop, backdropRect)
    DISPLAY.blit(frame, (gridLocX-blockSize, gridLocY-blockSize))
    SetGameplay()
    if bombs != -1:
        bombsTitle = font.render('BOMBS', True, WHITE)
    else:
        bombsTitle = font.render('BOMBS', True, GREY)

def TopTen():
    topTen = GetTopTen()
    bNewScore = False
    for i in range(len(topTen)):
        if score >= topTen[i][1]:
            bNewScore = True
            slot = i
            topTen.insert(slot, ['', score])
            topTen.pop()
            break
    if not bNewScore:
        return False

    topScores = []
    row = 3.0
    for i in range(len(topTen)):
        if i == slot:
            playerName = smallFont.render(str(i+1)+'. '+topTen[i][0]+'_', True, outlineColors[colScheme]) #v2.5
            playerScore = smallFont.render(str(topTen[i][1]), True, outlineColors[colScheme]) #v2.5
        else:
            playerName = smallFont.render(str(i+1)+'. '+topTen[i][0], True, WHITE)
            playerScore = smallFont.render(str(topTen[i][1]), True, WHITE)
        playerNameRect = playerName.get_rect(left=blockSize//2, centery=int(blockSize*row))
        playerScoreRect = playerScore.get_rect(right=gridWidth-blockSize//2, centery=int(blockSize*row))
        topScores.append([playerName, playerNameRect, playerScore, playerScoreRect])
        row += 1.5

    topTenTitle = font.render('TOP TEN', True, WHITE)
    topTenRect = topTenTitle.get_rect(center=(gridWidth//2, int(blockSize*1.5)))
    playerName = ''
    DISPLAY.blit(backdrop, backdropRect)
    DISPLAY.blit(frame, (gridLocX-blockSize, gridLocY-blockSize))
    bUpdate = True #v2.5
    while True:
        GRID.fill(BLACK)
        GRID.blit(topTenTitle, topTenRect)
        for i in range(len(topScores)):
            GRID.blit(topScores[i][0], topScores[i][1])
            GRID.blit(topScores[i][2], topScores[i][3])
        
        DrawDisplay()
        if bUpdate: #v2.5 update frame
            bUpdate = False
            pygame.display.update(Rect(gridLocX, gridLocY, gridWidth, gridHeight))
            
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_F4 and pygame.key.get_pressed()[K_LALT]: #Alt+F4
                    pygame.quit()
                    sys.exit()
                elif bNewScore:
                    if( len(playerName) < 12 and
                        ( event.key >= ord('a') and event.key <= ord('z') or
                        event.key >= ord('0') and event.key <= ord('9') or
                        event.key == ord(' ') )
                    ):
                        bUpdate = True #v2.5
                        key = event.key
                        if pygame.key.get_pressed()[K_LSHIFT] or pygame.key.get_pressed()[K_RSHIFT]:
                            shiftedKey = key - 32
                            if shiftedKey >= ord('A') and shiftedKey <= ord('Z'):
                                key -= 32
                        playerName += chr(key)
                        topScores[slot][0] = smallFont.render(str(slot+1)+'. '+playerName+'_', True, outlineColors[colScheme]) #v2.5
                    elif event.key == K_BACKSPACE and playerName != '':
                        bUpdate = True #v2.5
                        playerName = playerName[:-1]
                        topScores[slot][0] = smallFont.render(str(slot+1)+'. '+playerName+'_', True, outlineColors[colScheme]) #v2.5
                    elif event.key == K_RETURN:
                        bUpdate = True #v2.5
                        bNewScore = False
                        topScores[slot][0] = smallFont.render(str(slot+1)+'. '+playerName, True, WHITE)
                        topScores[slot][2] = smallFont.render(str(score), True, WHITE)
                        topTen[slot][0] = playerName
                        RecordTopTen(topTen)
                        pygame.time.set_timer(31, 5000)

                elif event.key == K_ESCAPE:
                    pygame.time.set_timer(31, 0)
                    return False

            elif event.type == 31:
                pygame.time.set_timer(31, 0)
                return False

            elif event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.time.Clock().tick(FPS)

def DelayFrames(numFrames):
    i = 0
    while i < numFrames:
        i += 1
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    option = Paused(False)
                    if option == 'quit':
                        PlayNextTrack(False)
                        #ResetGame(True)
                        return True
                    elif option == 'restart':
                        return False
                        
                elif event.key == K_F4 and pygame.key.get_pressed()[K_LALT]:
                    pygame.quit()
                    sys.exit()

            elif event.type == QUIT:
                pygame.quit()
                sys.exit()

        DrawBlocks()
        DrawDisplay()
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)