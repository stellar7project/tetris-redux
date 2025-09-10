'''Version 2.5'''
import pygame, os.path
from pygame.locals import *
from random import randint, random
from operator import add, sub
#from OpenGL.GL import *

pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()

pygame.display.set_icon( pygame.image.load('tetris.ico') ) #v2.4

VideoInfo = pygame.display.Info()
pygame.display.set_mode((VideoInfo.current_w, VideoInfo.current_h), DOUBLEBUF|OPENGL) #v2.4 Do NOT use FULLSCREEN here--screws up resolution switching
pygame.display.set_caption('TETRIS Redux')

light_noise = pygame.mixer.Sound("sounds/light_noise.wav")
arcing = pygame.mixer.Sound("sounds/arcing.wav")

ts_move = pygame.mixer.Sound("sounds/ts_move.wav")
ts_rotate = pygame.mixer.Sound("sounds/dspstop.wav")
ts_set = pygame.mixer.Sound("sounds/dsswtchx.wav")
ts_drop = pygame.mixer.Sound("sounds/dsswtchn.wav")
ts_break = pygame.mixer.Sound("sounds/ts_break.wav")
ts_charge = pygame.mixer.Sound("sounds/PLSCHARG.ogg")
#ts_disintegrate = pygame.mixer.Sound("sounds/ts_explode.wav")
ts_smashing = pygame.mixer.Sound("sounds/ts_smashing.wav")
ts_endsmash = pygame.mixer.Sound("sounds/ts_endsmash.wav")
#ts_gameover = pygame.mixer.Sound("sounds/dspdiehi.wav")
ts_gameover = pygame.mixer.Sound("sounds/game_over.wav")

ts_blast = (pygame.mixer.Sound("sounds/tetris4blast.wav"),
            pygame.mixer.Sound("sounds/comboblast.wav"))

ts_tetris = (pygame.mixer.Sound("sounds/ts_bleep.wav"),
             pygame.mixer.Sound("sounds/ts_bleep2.wav"),
             pygame.mixer.Sound("sounds/ts_bleep3.wav"),
             pygame.mixer.Sound("sounds/ts_quad.wav"),
             pygame.mixer.Sound("sounds/ts_tetriscombo.wav"))

ts_clinks = (pygame.mixer.Sound("sounds/clink1.wav"),
             pygame.mixer.Sound("sounds/clink2.wav"),
             pygame.mixer.Sound("sounds/clink3.wav"))

ts_whoosh = (pygame.mixer.Sound("sounds/whoosh1.wav"),
             pygame.mixer.Sound("sounds/whoosh2.wav"))

ts_disintegrate = (pygame.mixer.Sound("sounds/disintegrate1.wav"),
                   pygame.mixer.Sound("sounds/disintegrate2.wav"))

#blockSound = pygame.mixer.Channel(0)
scoreSound = pygame.mixer.Channel(1)
bombSound = pygame.mixer.Channel(2)
whooshSound = pygame.mixer.Channel(3)

backdropSrc = []
backdrops = os.listdir('images/backdrops')
i = 0
while i < len(backdrops):
    imgFormat = backdrops[i][len(backdrops[i])-3:]
    if imgFormat == 'png' or imgFormat == 'jpg':
        backdropSrc.append( pygame.image.load("images/backdrops/"+backdrops[i]).convert_alpha() )
        i += 1
    else:
        backdrops.pop(i)

gridSrc = (
    pygame.image.load("images/schemes/gridRed.png").convert_alpha(),
    pygame.image.load("images/schemes/gridOrange.png").convert_alpha(),
    pygame.image.load("images/schemes/gridGold.png").convert_alpha(),
    pygame.image.load("images/schemes/gridGreen.png").convert_alpha(),
    pygame.image.load("images/schemes/gridCyan.png").convert_alpha(),
    pygame.image.load("images/schemes/gridBlue.png").convert_alpha(),
    pygame.image.load("images/schemes/gridIndigo.png").convert_alpha(),
    pygame.image.load("images/schemes/gridGrey.png").convert_alpha()
)
frameSrc = (
    pygame.image.load("images/schemes/frameRed.png").convert_alpha(),
    pygame.image.load("images/schemes/frameOrange.png").convert_alpha(),
    pygame.image.load("images/schemes/frameGold.png").convert_alpha(),
    pygame.image.load("images/schemes/frameGreen.png").convert_alpha(),
    pygame.image.load("images/schemes/frameCyan.png").convert_alpha(),
    pygame.image.load("images/schemes/frameBlue.png").convert_alpha(),
    pygame.image.load("images/schemes/frameIndigo.png").convert_alpha(),
    pygame.image.load("images/schemes/frameGrey.png").convert_alpha()
)
tetrisOutSrc = ((pygame.image.load("images/text/tetris_outline.png").convert(), pygame.image.load("images/text/tetris4_outline.png").convert()))
comboSrc = pygame.image.load("images/text/combo.png").convert()

blockSource = {
    'red': pygame.image.load("images/sprites/red.png").convert(), #pygame.image.load("images/sprites/red0.png").convert_alpha() ],
    'orange': pygame.image.load("images/sprites/orange.png").convert(), #pygame.image.load("images/sprites/orange0.png").convert_alpha() ],
    'yellow': pygame.image.load("images/sprites/yellow.png").convert(), #pygame.image.load("images/sprites/yellow0.png").convert_alpha() ],
    'green': pygame.image.load("images/sprites/green.png").convert(), #pygame.image.load("images/sprites/green0.png").convert_alpha() ],
    'cyan': pygame.image.load("images/sprites/cyan.png").convert(), #pygame.image.load("images/sprites/cyan0.png").convert_alpha() ],
    'blue': pygame.image.load("images/sprites/blue.png").convert(), #pygame.image.load("images/sprites/blue0.png").convert_alpha() ],
    'purple': pygame.image.load("images/sprites/purple.png").convert(), #pygame.image.load("images/sprites/purple0.png").convert_alpha() ]
    'grey': pygame.image.load("images/sprites/grey.png").convert(), 
    'white': pygame.image.load("images/sprites/white.png").convert()
}

hotSrc = {
    'red': pygame.image.load("images/sprites/hot_red.png").convert_alpha(),
    'orange': pygame.image.load("images/sprites/hot_orange.png").convert_alpha(),
    'yellow': pygame.image.load("images/sprites/hot_yellow.png").convert_alpha(),
    'green': pygame.image.load("images/sprites/hot_green.png").convert_alpha(),
    'cyan': pygame.image.load("images/sprites/hot_cyan.png").convert_alpha(),
    'blue': pygame.image.load("images/sprites/hot_blue.png").convert_alpha(),
    'purple': pygame.image.load("images/sprites/hot_violet.png").convert_alpha(),
    'grey': pygame.image.load("images/sprites/hot_grey.png").convert_alpha(),
    'white': pygame.image.load("images/sprites/hot_white.png").convert_alpha()
}
'''
tetris4Source = (
    pygame.image.load("images/red4.png").convert(),
    pygame.image.load("images/orange4.png").convert(),
    pygame.image.load("images/gold4.png").convert(),
    pygame.image.load("images/green4.png").convert(),
    pygame.image.load("images/cyan4.png").convert(),
    pygame.image.load("images/blue4.png").convert(),
    pygame.image.load("images/purple4.png").convert()
    )
'''

nextListSource = [
    [pygame.image.load("images/sprites/next7_0.png").convert(),
     pygame.image.load("images/sprites/next7_1.png").convert(),
     pygame.image.load("images/sprites/next7_2.png").convert(),
     pygame.image.load("images/sprites/next7_3.png").convert()],
    
    [pygame.image.load("images/sprites/next7m_0.png").convert(),
     pygame.image.load("images/sprites/next7m_1.png").convert(),
     pygame.image.load("images/sprites/next7m_2.png").convert(),
     pygame.image.load("images/sprites/next7m_3.png").convert()],
    
    [pygame.image.load("images/sprites/nextT_0.png").convert(),
     pygame.image.load("images/sprites/nextT_1.png").convert(),
     pygame.image.load("images/sprites/nextT_2.png").convert(),
     pygame.image.load("images/sprites/nextT_3.png").convert()],
    
    [pygame.image.load("images/sprites/next4_0.png").convert(),
     pygame.image.load("images/sprites/next4_1.png").convert()],
    
    [pygame.image.load("images/sprites/next4m_0.png").convert(),
     pygame.image.load("images/sprites/next4m_1.png").convert()],
    
    [pygame.image.load("images/sprites/nextBar_0.png").convert(),
     pygame.image.load("images/sprites/nextBar_1.png").convert(),
     pygame.image.load("images/sprites/nextBar_0.png").convert(),
     pygame.image.load("images/sprites/nextBar_1.png").convert()],
    
    [pygame.image.load("images/sprites/nextBox.png").convert()]
]
#v2.5
nextListSrcGrey = [
    [pygame.image.load("images/sprites/next7_0_grey.png").convert(),
     pygame.image.load("images/sprites/next7_1_grey.png").convert(),
     pygame.image.load("images/sprites/next7_2_grey.png").convert(),
     pygame.image.load("images/sprites/next7_3_grey.png").convert()],
    
    [pygame.image.load("images/sprites/next7m_0_grey.png").convert(),
     pygame.image.load("images/sprites/next7m_1_grey.png").convert(),
     pygame.image.load("images/sprites/next7m_2_grey.png").convert(),
     pygame.image.load("images/sprites/next7m_3_grey.png").convert()],
    
    [pygame.image.load("images/sprites/nextT_0_grey.png").convert(),
     pygame.image.load("images/sprites/nextT_1_grey.png").convert(),
     pygame.image.load("images/sprites/nextT_2_grey.png").convert(),
     pygame.image.load("images/sprites/nextT_3_grey.png").convert()],
    
    [pygame.image.load("images/sprites/next4_0_grey.png").convert(),
     pygame.image.load("images/sprites/next4_1_grey.png").convert()],
    
    [pygame.image.load("images/sprites/next4m_0_grey.png").convert(),
     pygame.image.load("images/sprites/next4m_1_grey.png").convert()],
    
    [pygame.image.load("images/sprites/nextBar_0_grey.png").convert(),
     pygame.image.load("images/sprites/nextBar_1_grey.png").convert(),
     pygame.image.load("images/sprites/nextBar_0_grey.png").convert(),
     pygame.image.load("images/sprites/nextBar_1_grey.png").convert()],
    
    [pygame.image.load("images/sprites/nextBox_grey.png").convert()]
]
#v2.5
nextListSrcWhite = [
    [pygame.image.load("images/sprites/next7_0_white.png").convert(),
     pygame.image.load("images/sprites/next7_1_white.png").convert(),
     pygame.image.load("images/sprites/next7_2_white.png").convert(),
     pygame.image.load("images/sprites/next7_3_white.png").convert()],
    
    [pygame.image.load("images/sprites/next7m_0_white.png").convert(),
     pygame.image.load("images/sprites/next7m_1_white.png").convert(),
     pygame.image.load("images/sprites/next7m_2_white.png").convert(),
     pygame.image.load("images/sprites/next7m_3_white.png").convert()],
    
    [pygame.image.load("images/sprites/nextT_0_white.png").convert(),
     pygame.image.load("images/sprites/nextT_1_white.png").convert(),
     pygame.image.load("images/sprites/nextT_2_white.png").convert(),
     pygame.image.load("images/sprites/nextT_3_white.png").convert()],
    
    [pygame.image.load("images/sprites/next4_0_white.png").convert(),
     pygame.image.load("images/sprites/next4_1_white.png").convert()],
    
    [pygame.image.load("images/sprites/next4m_0_white.png").convert(),
     pygame.image.load("images/sprites/next4m_1_white.png").convert()],
    
    [pygame.image.load("images/sprites/nextBar_0_white.png").convert(),
     pygame.image.load("images/sprites/nextBar_1_white.png").convert(),
     pygame.image.load("images/sprites/nextBar_0_white.png").convert(),
     pygame.image.load("images/sprites/nextBar_1_white.png").convert()],
    
    [pygame.image.load("images/sprites/nextBox_white.png").convert()]
]
#v2.5 COLOURS
colorSrc = {
    'black': pygame.image.load("images/BLACK.png").convert(),
    'white': pygame.image.load("images/WHITE.png").convert()
}
GREY = (88,88,88); OUTGREY = (176,176,176)
BLACK = (0,0,0); WHITE = (255,255,255)
RED = (166,0,0); OUTRED = (255,0,0)
GREEN = (0,166,0); OUTGREEN = (0,255,0)
ORANGE = (154,77,0); OUTORANGE = (255,127,0)
CYAN = (0,166,166); OUTCYAN = (0,255,255)
INDIGO = (127,0,255); OUTINDIGO = (255,0,255)
BLUE = (45,50,129); OUTBLUE = (0,166,255) #(96,200,255) #(112,100,255) #(94,128,192)
YELLOW = (255,255,0); GOLD = (153,129,54); OUTGOLD = (255,216,91)

colorList = (
    RED, ORANGE, GOLD, GREEN, CYAN, BLUE, INDIGO, GREY
)
outlineColors = (
    OUTRED, OUTORANGE, OUTGOLD, OUTGREEN, OUTCYAN, OUTBLUE, OUTINDIGO, OUTGREY, WHITE
)
schemeNames = ( #v2.5
    'Red',
    'Orange',
    'Gold',
    'Green',
    'Cyan',
    'Blue',
    'Indigo',
    'Monochrome',
    'RANDOM'
    )
tetrisColors = (
    'red',
    'orange',
    'yellow',
    'green',
    'cyan',
    'blue',
    'purple',
    'grey',
    'white'
    )

blocks = {
    'red': blockSource['red'].copy(), #blockSource['red'][1].copy() ],
    'orange': blockSource['orange'].copy(), #blockSource['orange'][1].copy() ],
    'yellow': blockSource['yellow'].copy(), #blockSource['yellow'][1].copy() ],
    'green': blockSource['green'].copy(), #blockSource['green'][1].copy() ],
    'cyan': blockSource['cyan'].copy(), #blockSource['cyan'][1].copy() ],
    'blue': blockSource['blue'].copy(), #blockSource['blue'][1].copy() ],
    'purple': blockSource['purple'].copy(), #blockSource['purple'][1].copy() ]
    'grey': blockSource['grey'].copy(),
    'white': blockSource['white'].copy()
    }

hotBlocks = {
    'red': hotSrc['red'].copy(),
    'orange': hotSrc['orange'].copy(),
    'yellow': hotSrc['yellow'].copy(),
    'green': hotSrc['green'].copy(),
    'cyan': hotSrc['cyan'].copy(),
    'blue': hotSrc['blue'].copy(),
    'purple': hotSrc['purple'].copy(),
    'grey': hotSrc['grey'].copy(),
    'white': hotSrc['white'].copy()
}

megaBombMaps = {
    0: (
        ('purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple', 'purple'),
        ('purple', 'grey', 'grey', 'blue', 'blue', 'blue', 'grey', 'grey', 'grey', 'purple'),
        ('purple', 'grey', 'grey', 'grey', 'grey', 'grey', 'blue', 'grey', 'grey', 'purple'),
        ('purple', 'grey', 'grey', 'grey', 'blue', 'blue', 'blue', 'grey', 'grey', 'purple'),
        ('purple', 'grey', 'grey', 'grey', 'blue', 'grey', 'grey', 'grey', 'cyan', 'purple'),
        ('purple', 'grey', 'grey', 'grey', 'grey', 'blue', 'blue', 'grey', 'cyan', 'purple'),
        ('purple', 'green', 'grey', 'grey', 'green', 'grey', 'grey', 'grey', 'cyan', 'purple'),
        ('purple', 'green', 'grey', 'green', 'grey', 'grey', 'grey', 'grey', 'cyan', 'purple'),
        ('purple', 'green', 'green', 'green', 'grey', 'grey', 'yellow', 'grey', 'cyan', 'purple'),
        ('purple', 'green', 'grey', 'grey', 'green', 'grey', 'yellow', 'grey', 'grey', 'purple'),
        ('purple', 'green', 'green', 'green', 'grey', 'grey', 'yellow', 'grey', 'grey', 'purple'),
        ('purple', 'grey', 'grey', 'grey', 'grey', 'grey', 'yellow', 'grey', 'grey', 'purple'),
        ('purple', 'grey', 'grey', 'grey', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'purple'),
        ('purple', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'purple'),
        ('purple', 'grey', 'grey', 'grey', 'grey', 'orange', 'orange', 'orange', 'orange', 'purple'),
        ('purple', 'grey', 'grey', 'red', 'grey', 'orange', 'grey', 'grey', 'grey', 'purple'),
        ('purple', 'grey', 'grey', 'red', 'grey', 'orange', 'orange', 'orange', 'grey', 'purple'),
        ('purple', 'grey', 'grey', 'red', 'grey', 'orange', 'grey', 'grey', 'grey', 'purple'),
        ('purple', 'grey', 'grey', 'red', 'grey', 'grey', 'orange', 'orange', 'orange', 'purple'),
        ('purple', 'red', 'red', 'red', 'red', 'red', 'grey', 'grey', 'grey', 'purple')
    ),
    1: (
        ('red', 'orange', 'yellow', 'green', 'cyan', 'purple', 'red', 'orange', 'yellow', 'green'),
        ('cyan', 'purple', 'red', 'orange', 'yellow', 'green', 'cyan', 'purple', 'red', 'orange'),
        ('yellow', 'green', 'cyan', 'purple', 'red', 'orange', 'yellow', 'green', 'cyan', 'purple'),
        ('red', 'orange', 'yellow', 'green', 'cyan', 'purple', 'red', 'orange', 'yellow', 'green'),
        ('cyan', 'purple', 'red', 'orange', 'yellow', 'green', 'cyan', 'purple', 'red', 'orange'),
        ('yellow', 'green', 'cyan', 'purple', 'red', 'orange', 'yellow', 'green', 'cyan', 'purple'),
        ('red', 'orange', 'yellow', 'green', 'cyan', 'purple', 'red', 'orange', 'yellow', 'green'),
        ('cyan', 'purple', 'red', 'orange', 'yellow', 'green', 'cyan', 'purple', 'red', 'orange'),
        ('yellow', 'green', 'cyan', 'purple', 'red', 'orange', 'yellow', 'green', 'cyan', 'purple'),
        ('red', 'orange', 'yellow', 'green', 'cyan', 'purple', 'red', 'orange', 'yellow', 'green'),
        ('cyan', 'purple', 'red', 'orange', 'yellow', 'green', 'cyan', 'purple', 'red', 'orange'),
        ('yellow', 'green', 'cyan', 'purple', 'red', 'orange', 'yellow', 'green', 'cyan', 'purple'),
        ('red', 'orange', 'yellow', 'green', 'cyan', 'purple', 'red', 'orange', 'yellow', 'green'),
        ('cyan', 'purple', 'red', 'orange', 'yellow', 'green', 'cyan', 'purple', 'red', 'orange'),
        ('yellow', 'green', 'cyan', 'purple', 'red', 'orange', 'yellow', 'green', 'cyan', 'purple'),
        ('red', 'orange', 'yellow', 'green', 'cyan', 'purple', 'red', 'orange', 'yellow', 'green'),
        ('cyan', 'purple', 'red', 'orange', 'yellow', 'green', 'cyan', 'purple', 'red', 'orange'),
        ('yellow', 'green', 'cyan', 'purple', 'red', 'orange', 'yellow', 'green', 'cyan', 'purple'),
        ('red', 'orange', 'yellow', 'green', 'cyan', 'purple', 'red', 'orange', 'yellow', 'green'),
        ('cyan', 'purple', 'red', 'orange', 'yellow', 'green', 'cyan', 'purple', 'red', 'orange')
    ),
    2: (
        ('blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue'),
        ('blue', 'grey', 'grey', 'purple', 'purple', 'purple', 'grey', 'grey', 'grey', 'blue'),
        ('blue', 'grey', 'grey', 'grey', 'grey', 'grey', 'purple', 'grey', 'grey', 'blue'),
        ('blue', 'grey', 'grey', 'grey', 'purple', 'purple', 'purple', 'grey', 'grey', 'blue'),
        ('blue', 'grey', 'grey', 'grey', 'purple', 'grey', 'grey', 'grey', 'cyan', 'blue'),
        ('blue', 'grey', 'grey', 'grey', 'grey', 'purple', 'purple', 'grey', 'cyan', 'blue'),
        ('blue', 'green', 'grey', 'grey', 'green', 'grey', 'grey', 'grey', 'cyan', 'blue'),
        ('blue', 'green', 'grey', 'green', 'grey', 'grey', 'grey', 'grey', 'cyan', 'blue'),
        ('blue', 'green', 'green', 'green', 'grey', 'grey', 'yellow', 'grey', 'cyan', 'blue'),
        ('blue', 'green', 'grey', 'grey', 'green', 'grey', 'yellow', 'grey', 'grey', 'blue'),
        ('blue', 'green', 'green', 'green', 'grey', 'grey', 'yellow', 'grey', 'grey', 'blue'),
        ('blue', 'grey', 'grey', 'grey', 'grey', 'grey', 'yellow', 'grey', 'grey', 'blue'),
        ('blue', 'grey', 'grey', 'grey', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'blue'),
        ('blue', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'grey', 'blue'),
        ('blue', 'grey', 'grey', 'grey', 'grey', 'orange', 'orange', 'orange', 'orange', 'blue'),
        ('blue', 'grey', 'grey', 'red', 'grey', 'orange', 'grey', 'grey', 'grey', 'blue'),
        ('blue', 'grey', 'grey', 'red', 'grey', 'orange', 'orange', 'orange', 'grey', 'blue'),
        ('blue', 'grey', 'grey', 'red', 'grey', 'orange', 'grey', 'grey', 'grey', 'blue'),
        ('blue', 'grey', 'grey', 'red', 'grey', 'grey', 'orange', 'orange', 'orange', 'blue'),
        ('blue', 'red', 'red', 'red', 'red', 'red', 'grey', 'grey', 'grey', 'blue')
    ),
    3: (
        ('cyan', 'cyan', 'cyan', 'cyan', 'yellow', 'yellow', 'cyan', 'cyan', 'cyan', 'cyan'),
        ('purple', 'purple', 'purple', 'red', 'yellow', 'yellow', 'green', 'purple', 'purple', 'purple'),
        ('cyan', 'purple', 'red', 'red', 'yellow', 'yellow', 'green', 'green', 'purple', 'cyan'),
        ('cyan', 'purple', 'red', 'orange', 'yellow', 'yellow', 'blue', 'green', 'purple', 'cyan'),
        ('cyan', 'purple', 'purple', 'orange', 'yellow', 'yellow', 'blue', 'purple', 'purple', 'cyan'),
        ('cyan', 'purple', 'orange', 'orange', 'yellow', 'yellow', 'blue', 'blue', 'purple', 'cyan'),
        ('red', 'red', 'blue', 'blue', 'yellow', 'yellow', 'orange', 'orange', 'green', 'green'),
        ('orange', 'red', 'red', 'blue', 'yellow', 'yellow', 'orange', 'green', 'green', 'blue'),
        ('orange', 'orange', 'orange', 'blue', 'purple', 'purple', 'orange', 'blue', 'blue', 'blue'),
        ('cyan', 'red', 'red', 'purple', 'purple', 'purple', 'purple', 'green', 'green', 'cyan'),
        ('cyan', 'green', 'red', 'red', 'purple', 'purple', 'green', 'green', 'red', 'cyan'),
        ('cyan', 'green', 'green', 'yellow', 'yellow', 'yellow', 'yellow', 'red', 'red', 'cyan'),
        ('cyan', 'purple', 'green', 'yellow', 'yellow', 'yellow', 'yellow', 'red', 'purple', 'cyan'),
        ('purple', 'purple', 'purple', 'cyan', 'cyan', 'cyan', 'cyan', 'purple', 'purple', 'purple'),
        ('blue', 'yellow', 'yellow', 'cyan', 'yellow', 'yellow', 'cyan', 'yellow', 'yellow', 'orange'),
        ('blue', 'yellow', 'yellow', 'cyan', 'yellow', 'yellow', 'cyan', 'yellow', 'yellow', 'orange'),
        ('blue', 'blue', 'red', 'cyan', 'orange', 'blue', 'cyan', 'green', 'orange', 'orange'),
        ('cyan', 'red', 'red', 'cyan', 'orange', 'blue', 'cyan', 'green', 'green', 'cyan'),
        ('cyan', 'red', 'purple', 'orange', 'orange', 'blue', 'blue', 'purple', 'green', 'cyan'),
        ('cyan', 'purple', 'purple', 'purple', 'yellow', 'yellow', 'purple', 'purple', 'purple', 'cyan'),
    ),
    4: (
        ('orange', 'orange', 'purple', 'blue', 'blue', 'blue', 'blue', 'purple', 'orange', 'orange'),
        ('orange', 'purple', 'purple', 'purple', 'blue', 'blue', 'purple', 'purple', 'purple', 'orange'),
        ('orange', 'red', 'grey', 'green', 'blue', 'blue', 'green', 'grey', 'red', 'orange'),
        ('red', 'red', 'grey', 'green', 'green', 'green', 'green', 'grey', 'red', 'red'),
        ('red', 'grey', 'grey', 'grey', 'green', 'green', 'grey', 'grey', 'grey', 'red'),
        ('orange', 'orange', 'purple', 'blue', 'blue', 'blue', 'blue', 'purple', 'orange', 'orange'),
        ('orange', 'purple', 'purple', 'purple', 'blue', 'blue', 'purple', 'purple', 'purple', 'orange'),
        ('orange', 'red', 'grey', 'green', 'blue', 'blue', 'green', 'grey', 'red', 'orange'),
        ('red', 'red', 'grey', 'green', 'green', 'green', 'green', 'grey', 'red', 'red'),
        ('red', 'grey', 'grey', 'grey', 'green', 'green', 'grey', 'grey', 'grey', 'red'),
        ('orange', 'orange', 'purple', 'blue', 'blue', 'blue', 'blue', 'purple', 'orange', 'orange'),
        ('orange', 'purple', 'purple', 'purple', 'blue', 'blue', 'purple', 'purple', 'purple', 'orange'),
        ('orange', 'red', 'grey', 'green', 'blue', 'blue', 'green', 'grey', 'red', 'orange'),
        ('red', 'red', 'grey', 'green', 'green', 'green', 'green', 'grey', 'red', 'red'),
        ('red', 'grey', 'grey', 'grey', 'green', 'green', 'grey', 'grey', 'grey', 'red'),
        ('orange', 'orange', 'purple', 'blue', 'blue', 'blue', 'blue', 'purple', 'orange', 'orange'),
        ('orange', 'purple', 'purple', 'purple', 'blue', 'blue', 'purple', 'purple', 'purple', 'orange'),
        ('orange', 'red', 'grey', 'green', 'blue', 'blue', 'green', 'grey', 'red', 'orange'),
        ('red', 'red', 'grey', 'green', 'green', 'green', 'green', 'grey', 'red', 'red'),
        ('red', 'grey', 'grey', 'grey', 'green', 'green', 'grey', 'grey', 'grey', 'red')
    ),
    'mono': (
        ('grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white'),
        ('white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey'),
        ('grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white'),
        ('white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey'),
        ('grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white'),
        ('white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey'),
        ('grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white'),
        ('white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey'),
        ('grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white'),
        ('white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey'),
        ('grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white'),
        ('white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey'),
        ('grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white'),
        ('white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey'),
        ('grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white'),
        ('white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey'),
        ('grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white'),
        ('white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey'),
        ('grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white'),
        ('white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey', 'white', 'grey')
    )
}
#v2.5
def GetMegaBombMap(mapIndex, bMonochrome):
    if mapIndex == 3:
        if bMonochrome:
            colour = 7
        else:
            colour = randint(0,6)
        return (
            (tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour]),
            (tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[8], tetrisColors[8], tetrisColors[8], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour]),
            (tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[8], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour]),
            (tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[8], tetrisColors[8], tetrisColors[8], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour]),
            (tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[8], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[8], tetrisColors[colour]),
            (tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[8], tetrisColors[8], tetrisColors[colour], tetrisColors[8], tetrisColors[colour]),
            (tetrisColors[colour], tetrisColors[8], tetrisColors[colour], tetrisColors[colour], tetrisColors[8], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[8], tetrisColors[colour]),
            (tetrisColors[colour], tetrisColors[8], tetrisColors[colour], tetrisColors[8], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[8], tetrisColors[colour]),
            (tetrisColors[colour], tetrisColors[8], tetrisColors[8], tetrisColors[8], tetrisColors[colour], tetrisColors[colour], tetrisColors[8], tetrisColors[colour], tetrisColors[8], tetrisColors[colour]),
            (tetrisColors[colour], tetrisColors[8], tetrisColors[colour], tetrisColors[colour], tetrisColors[8], tetrisColors[colour], tetrisColors[8], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour]),
            (tetrisColors[colour], tetrisColors[8], tetrisColors[8], tetrisColors[8], tetrisColors[colour], tetrisColors[colour], tetrisColors[8], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour]),
            (tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[8], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour]),
            (tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[8], tetrisColors[8], tetrisColors[8], tetrisColors[8], tetrisColors[8], tetrisColors[colour]),
            (tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour]),
            (tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[8], tetrisColors[8], tetrisColors[8], tetrisColors[8], tetrisColors[colour]),
            (tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[8], tetrisColors[colour], tetrisColors[8], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour]),
            (tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[8], tetrisColors[colour], tetrisColors[8], tetrisColors[8], tetrisColors[8], tetrisColors[colour], tetrisColors[colour]),
            (tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[8], tetrisColors[colour], tetrisColors[8], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour]),
            (tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[8], tetrisColors[colour], tetrisColors[colour], tetrisColors[8], tetrisColors[8], tetrisColors[8], tetrisColors[colour]),
            (tetrisColors[colour], tetrisColors[8], tetrisColors[8], tetrisColors[8], tetrisColors[8], tetrisColors[8], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour], tetrisColors[colour])
        )
    if mapIndex == 2:
        if bMonochrome:
            a = 7; b = 8
        else:
            a = 0; b = 6
        return (
            (tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)]),
            (tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)]),
            (tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)]),
            (tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)]),
            (tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)]),
            (tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)]),
            (tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)]),
            (tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)]),
            (tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)]),
            (tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)]),
            (tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)]),
            (tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)]),
            (tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)]),
            (tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)]),
            (tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)]),
            (tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)]),
            (tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)]),
            (tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)]),
            (tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)]),
            (tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)], tetrisColors[randint(a,b)])
        )
    elif bMonochrome:
        return megaBombMaps['mono']
    return megaBombMaps[mapIndex]

nextList = []
nextListGrey = []
nextListWhite = []
def SetNextList(): #v2.5
    nextList.clear()
    nextListGrey.clear()
    nextListWhite.clear()
    for i in range(7):
        nList = [[],[],[]]
        for j in range(len(nextListSource[i])):
            nextTetromino = nextListSource[i][j]
            nextTetromino.set_colorkey(BLACK)
            nList[0].append(nextTetromino.copy())
            nextTetromino = nextListSrcGrey[i][j]
            nextTetromino.set_colorkey(BLACK)
            nList[1].append(nextTetromino.copy())
            nextTetromino = nextListSrcWhite[i][j]
            nextTetromino.set_colorkey(BLACK)
            nList[2].append(nextTetromino.copy())
        nextList.append(nList[0])
        nextListGrey.append(nList[1])
        nextListWhite.append(nList[2])

def GetNextList(colorScheme, monoColor): #v2.5
    if colorScheme == 7:
        if monoColor == 0 or monoColor == 'grey':
            return nextListGrey
        return nextListWhite
    return nextList

pointsDat = [ #v2.2
    0,
    None,
    BLACK,
    0
]

shape = []
rotOffsets = []
rotProxy = []
blockList = []
dropList = []
blockFX = []
bombList = []
bombedList = []
hotList = []
blockSize = 48

class Block:
    scale = 1.0
    angle = 0
    gravity = 8
    bCollided = False
    bPulse = True
    
    def __init__(self, state, color, location, velocity, rotation, scaleOffset, heatAlpha, verticalSpace):
        self.velocity = velocity
        self.rotation = rotation
        self.scaleOffset = scaleOffset
        if state != 'fly':
            self.block = hotBlocks[color]
            if state == 'fly hot':
                blockRect = self.block.get_rect(centerx=location[0]+blockSize//2, centery=location[1]+blockSize//2)
                location = [blockRect.left, blockRect.top]
        else:
            self.block = blocks[color]
        self.image = self.block.copy()
        self.location = location
        self.color = color
        self.state = state
        self.heatAlpha = heatAlpha
        self.gravity *= verticalSpace

    def initPulse(self, min, max, i):
        self.minHeat = min
        self.maxHeat = max
        self.iHeat = i

    def heat(self, heatAlpha):
        self.image = hotBlocks[self.color].copy()
        self.image.fill((255,255,255, heatAlpha), None, BLEND_RGBA_MULT)
        self.blockRect = self.image.get_rect(center=self.location)

    def pulse(self, location):
        if self.bPulse:
            if self.heatAlpha < self.maxHeat:
                self.heatAlpha += self.iHeat
            else:
                self.bPulse = False
        else:
            if self.heatAlpha > self.minHeat:
                self.heatAlpha -= self.iHeat
            else:
                self.bPulse = True
        self.image = self.block.copy()
        self.image.fill((255,255,255, self.heatAlpha), None, BLEND_RGBA_MULT)
        self.blockRect = self.image.get_rect(center=location)
        self.location = location

    def disintegrate(self):
        self.heatAlpha -= 32
        if self.heatAlpha > 0:
            self.scale += self.scaleOffset
            self.image = pygame.transform.rotozoom(self.block.copy(), 0, self.scale)
            self.image.fill((255,255,255, self.heatAlpha), None, BLEND_RGBA_MULT)
            self.blockRect = self.image.get_rect(center=self.location)
        else:
            return 'destroy'

    def update(self):
        self.bCollided = False
        self.velocity[1] += self.gravity
        self.location[0] += self.velocity[0]
        self.location[1] += self.velocity[1]
        self.angle += self.rotation
        self.scale += self.scaleOffset
        self.image = pygame.transform.rotozoom(self.block.copy(), self.angle, self.scale) 
        self.image.set_colorkey(BLACK)

    def collideWith(self, other, vel):
        self.bCollided = True
        self.velocity = list( map(add, self.velocity, vel) )
        other.bCollided = True
        other.velocity = list( map(sub, other.velocity, vel) )
    
def ResizeBlocks(f, prevSize):
    size = int(48*f)
    for k in blocks:
        blocks[k] = pygame.transform.scale(blockSource[k].copy(), (size, size))
    #for k, block in blocks.items():
        #block[0] = pygame.transform.scale(blockSource[k][0].copy(), (size, size))
        #block[1] = pygame.transform.scale(blockSource[k][1].copy(), (size, size))
    
    for i in range(7):
        #tetris4Blocks[i] = pygame.transform.scale(tetris4Source[i].copy(), (int(480*f), int(192*f)))
        
        for j in range(len(nextList[i])): #v2.5
            nextTetromino = nextListSource[i][j]
            x = int(nextTetromino.get_rect().width * f)
            y = int(nextTetromino.get_rect().height * f)
            nextList[i][j] = pygame.transform.scale(nextTetromino.copy(), (x,y))
            nextTetromino = nextListSrcGrey[i][j]
            nextListGrey[i][j] = pygame.transform.scale(nextTetromino.copy(), (x,y))
            nextTetromino = nextListSrcWhite[i][j]
            nextListWhite[i][j] = pygame.transform.scale(nextTetromino.copy(), (x,y))

    for i in range(len(shape)):
        shape[i][0] = blocks[shape[i][2]]
        shape[i][1][0] = size * int(shape[i][1][0]/prevSize) #int(size/fOffset)
        shape[i][1][1] = size * int(shape[i][1][1]/prevSize)
        #shape[i][1][0] = int(shape[i][1][0]*fOffset)
        #shape[i][1][1] = int(shape[i][1][1]*fOffset)

    for i in range(len(blockList)):
        for j in range(len(blockList[i])):
            blockList[i][j][0] = blocks[blockList[i][j][2]]
            blockList[i][j][1][0] = size * int(blockList[i][j][1][0]/prevSize)
            blockList[i][j][1][1] = size * int(blockList[i][j][1][1]/prevSize)
            #blockList[i][j][1][0] = int(blockList[i][j][1][0]*fOffset)
            #blockList[i][j][1][1] = int(blockList[i][j][1][1]*fOffset)

    for i in range(len(dropList)):
        for j in range(len(dropList[i])):
            dropList[i][j][0] = blocks[dropList[i][j][2]]
            dropList[i][j][1][0] = size * int(dropList[i][j][1][0]/prevSize)
            dropList[i][j][1][1] = size * int(dropList[i][j][1][1]/prevSize)
            #dropList[i][j][1][0] = int(dropList[i][j][1][0]*fOffset)
            #dropList[i][j][1][1] = int(dropList[i][j][1][1]*fOffset)

    for i in range(len(blockFX)):
        blockFX[i][1][0] = size * int(blockFX[i][1][0]/prevSize)
        blockFX[i][1][1] = size * int(blockFX[i][1][1]/prevSize)
        #blockFX[i][1][0] = int(blockFX[i][1][0]*fOffset)
        #blockFX[i][1][1] = int(blockFX[i][1][1]*fOffset)

    #if explode == 0:
    for i in range(len(bombList)):
        bombList[i][1] = [size * int(bombList[i][1][0]/prevSize), size * int(bombList[i][1][1]/prevSize)]
        #bombList[i][1] = [int(bombList[i][1][0]*fOffset), int(bombList[i][1][1]*fOffset)]

    size = int(60*f)
    for k in hotBlocks:
        hotBlocks[k] = pygame.transform.scale(hotSrc[k].copy(), (size,size))

                
def gen7(blockSize, MID, colorSelect, bMirror):
    if colorSelect < 7:
        if bMirror:
            c = 'blue'
        else:
            c = 'orange'
    else:
        c = tetrisColors[colorSelect] #v2.4

    shape.append([blocks[c], [MID, 0], c])
    shape.append([blocks[c], [MID, -blockSize], c])
    shape.append([blocks[c], [MID, -blockSize*2], c])
    
    rotOffsets.append([[-1,-1], [1,-1], [1,1], [-1,1]])
    rotOffsets.append([[0,0],[0,0],[0,0],[0,0]])
    rotOffsets.append([[1,1], [-1,1], [-1,-1], [1,-1]])
    
    if not bMirror:
        shape.append([blocks[c], [MID-blockSize, -blockSize*2], c])
        rotOffsets.append([[2,0], [0,2], [-2,0], [0,-2]])
    else: #Mirror
        shape.append([blocks[c], [MID+blockSize, -blockSize*2], c])
        rotOffsets.append([[0,2], [-2,0], [0,-2], [2,0]])
    
    return 'gen7'

def genT(blockSize, MID, colorSelect, bMirror):
    if colorSelect > 6:
        color = tetrisColors[colorSelect] #v2.4
    else:
        color = 'purple'
    shape.append([blocks[color], [MID-blockSize, 0], color])
    shape.append([blocks[color], [MID-blockSize, -blockSize], color])
    shape.append([blocks[color], [MID, -blockSize], color])
    shape.append([blocks[color], [MID-blockSize, -blockSize*2], color])

    rotOffsets.append([[-1,-1], [1,-1], [1,1], [-1,1]])
    rotOffsets.append([[0,0],[0,0],[0,0],[0,0]])
    rotOffsets.append([[-1,1], [-1,-1], [1,-1], [1,1]])
    rotOffsets.append([[1,1], [-1,1], [-1,-1], [1,-1]])
    
    return 'genT'

def gen4(blockSize, MID, colorSelect, bMirror):
    if colorSelect < 7:
        if bMirror:
            c = 'green'
        else:
            c = 'red'
    else:
        c = tetrisColors[colorSelect] #v2.4
    shape.append([blocks[c], [MID, 0], c])
    shape.append([blocks[c], [MID, -blockSize], c])
    #rotOffsets.append([[-1,-1], [1,1]])
    #rotOffsets.append([[0,0], [0,0]])
    #rotOffsets.append([[1,-1], [-1,1]])
    #rotOffsets.append([[2,0], [-2,0]])
    
    if not bMirror:
        shape.append([blocks[c], [MID-blockSize, -blockSize], c])
        shape.append([blocks[c], [MID-blockSize, -blockSize*2], c])
        rotOffsets.append([[-1,0], [1,0]])
        rotOffsets.append([[0,0], [0,0]])
        rotOffsets.append([[1,1], [-1,-1]])
        rotOffsets.append([[2,1], [-2,-1]])
    else: #Mirror
        shape.append([blocks[c], [MID+blockSize, -blockSize], c])
        shape.append([blocks[c], [MID+blockSize, -blockSize*2], c])
        rotOffsets.append([[-1,-1], [1,1]])
        rotOffsets.append([[0,0], [0,0]])
        rotOffsets.append([[-1,1], [1,-1]])
        rotOffsets.append([[0,2], [0,-2]])
    
    return 'gen4'

def genBar(blockSize, MID, colorSelect, bMirror):
    if colorSelect > 6:
        color = tetrisColors[colorSelect] #v2.4
    else:
        color = 'cyan'
    shape.append([blocks[color], [MID, 0], color])
    shape.append([blocks[color], [MID, -blockSize], color])
    shape.append([blocks[color], [MID, -blockSize*2], color])
    shape.append([blocks[color], [MID, -blockSize*3], color])

    rotOffsets.append([[-1,-1], [1,-1], [1,1], [-1,1]])
    rotOffsets.append([[0,0],[0,0],[0,0],[0,0]])
    rotOffsets.append([[1,1], [-1,1], [-1,-1], [1,-1]])
    rotOffsets.append([[2,2], [-2,2], [-2,-2], [2,-2]])
    
    return 'genBar'
    
def genBox(blockSize, MID, colorSelect, bMirror):
    if colorSelect > 6:
        color = tetrisColors[colorSelect] #v2.4
    else:
        color = 'yellow'
    shape.append([blocks[color], [MID, 0], color])
    shape.append([blocks[color], [MID-blockSize, 0], color])
    shape.append([blocks[color], [MID-blockSize, -blockSize], color])
    shape.append([blocks[color], [MID, -blockSize], color])
    
    return 'genBox'


PROGRAM_DIRECTOR = ['Chris Arpaia']
ART_DESIGN = [
    'Chris Arpaia', 
    'The Tetris Company'
]
SOUND_FX = [
    'Capcom', 
    'id Software', 
    'Nintendo', 
    'Shayning'
]
EXECUTIVE_ADVISORS = [
    'Tom Gorodetsky',
    'Stella Lee', 
    'Lenssa Olana', 
    'Luciano Yen', 
    'Zed Zhao'
]
QUALITY_ASSURANCE = [
    'Chris Arpaia',
    'Tom Gorodetsky',
    'Gary Skliar',
    'Denis Iakobson',
    'Dmitri Marcus',
    'Kati Kotenko',
    'Matt Skliar',
    'Daniel Oprita',
    'Aleksei Fedorkov',
    'Daniel Verskin',
    'Mete Sengul',
    'Viktoriya Turukina',
    'Abigail Gal',
    'Michael Ilin',
    'Eva Kalmanson',
    'Lali Korinevska',
    'Sophia Teslia',
    'Alisa Sagals',
    'Maryanna Tkachenko',
    'Anna Maizelev',
    'Maya Pavlenko',
    'Leah Ekshtut'
]

''' OPENGL SUCKS
# basic opengl configuration
glViewport(0, 0, VideoInfo.current_w, VideoInfo.current_h)
glDepthRange(0, 1)
glMatrixMode(GL_PROJECTION)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glShadeModel(GL_SMOOTH)
glClearColor(0.0, 0.0, 0.0, 0.0)
glClearDepth(1.0)
glDisable(GL_DEPTH_TEST)
glDisable(GL_LIGHTING)
glDepthFunc(GL_LEQUAL)
glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
glEnable(GL_BLEND)
###
### Function to convert a PyGame Surface to an OpenGL Texture
### Maybe it's not necessary to perform each of these operations
### every time.
###
texID = glGenTextures(1)
def surfaceToTexture( pygame_surface ):
    global texID
    rgb_surface = pygame.image.tostring( pygame_surface, 'RGB')
    glBindTexture(GL_TEXTURE_2D, texID)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    surface_rect = pygame_surface.get_rect()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, surface_rect.width, surface_rect.height, 0, GL_RGB, GL_UNSIGNED_BYTE, rgb_surface)
    glGenerateMipmap(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, 0)

def glDraw(screen):
    
    # prepare to render the texture-mapped rectangle
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glDisable(GL_LIGHTING)
    glEnable(GL_TEXTURE_2D)

    # draw texture openGL Texture
    surfaceToTexture( screen )
    glBindTexture(GL_TEXTURE_2D, texID)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(-1, 1)
    glTexCoord2f(0, 1); glVertex2f(-1, -1)
    glTexCoord2f(1, 1); glVertex2f(1, -1)
    glTexCoord2f(1, 0); glVertex2f(1, 1)
    glEnd()
'''