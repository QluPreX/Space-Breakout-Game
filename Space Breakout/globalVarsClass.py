import os
import pygame
from pygame import *
    #statische variabelen
WIDTH = 800
HEIGHT = 600
KEYBOARD_SPEED = 20
DEVELOPER_TOOLS = True #verander dit voor Cheatkeys te gebruiken
SCORE_FOR_EXTRA_LIFE = 12
GAME_FOLDER = os.path.dirname(__file__)
ASSETS_FOLDER = os.path.join(GAME_FOLDER,"Assets")
#dynamsche variabelen
showMenu = True #default True
gameOn = True
levelsPlaying = False
gameOverMenu = False #default False
changeLevel = False
showCheatKeys = False
ballServed = False
changeBall = False
changeBat = False
#integers
level = 1
score = 0
scoreTemp = 0
yBg = 0
xBg = 0
playerY = 540
lives = 3
maxLives = 6
scoreComboMultiplier = 2
ballSpeed = 4
ballMaxSpeed = 10
#Strings
keyDown = None
cheatStringList = ("key 1:..increase combo score","key 2:..................delete steen","key 3:.................volgend level","key 4:....................extra leven","key 5:.............maak bal groot","key 6:........maak player groot","key 7:........increase ball speed","key ENTER:..........Keys Menu")
stringMenuList = ('Gebruik ARROW KEYS of je MUIS','Druk SPATIE of op je muisknop voor de ball te starten!','Press any key to continue...')
gameOverStringList = ("Druk SPATIE voor opnieuw te spelen","Druk ESC voor af te sluiten")
#arrays
upgradeRectList = []
pygame.init()
FPSCLOCK = pygame.time.Clock()
#initiatleer DISPLAYS
mainSurface = pygame.display.set_mode((WIDTH,HEIGHT))

black = pygame.Color(0,0,0)
white = pygame.Color(255,255,255)
fontobj = pygame.font.Font("freesansbold.ttf", 14)
fontobjTITEL = pygame.font.Font("freesansbold.ttf", 24)
fontobjCOMBO = pygame.font.Font("freesansbold.ttf",30)
fontCheatKeys = pygame.font.Font(None,22)
#labels
welkomLabel = fontobjTITEL.render('SPACE BREAKOUT!', True, white,black)
#adding sounds
batBotsingSound = pygame.mixer.Sound(os.path.join(ASSETS_FOLDER,"drop-a-brick.wav"))
#sprites & achtergrond(en)
bgMain = pygame.image.load(os.path.join(ASSETS_FOLDER,"bg.png"))
gameOverBg = pygame.image.load(os.path.join(ASSETS_FOLDER,"gameOver.png"))
bg1 = pygame.image.load(os.path.join(ASSETS_FOLDER,"bg1.jpg")).convert()
bg2 = pygame.image.load(os.path.join(ASSETS_FOLDER,"bg2.jpg")).convert()
bg3 = pygame.image.load(os.path.join(ASSETS_FOLDER,"bg3.jpg")).convert()
bg4 = pygame.image.load(os.path.join(ASSETS_FOLDER,"bg4.jpg")).convert()
nextLevelBg = pygame.image.load(os.path.join(ASSETS_FOLDER,"nextLevelBg.jpg")).convert()
#dynamische X en Y voor bewegende achtergronden
# pallet initialiseren
batSprite = pygame.image.load(os.path.join(ASSETS_FOLDER,"bat.png")).convert()
batLangSprite = pygame.image.load(os.path.join(ASSETS_FOLDER,"bat_lang.png")).convert()
upgradeBlauw = pygame.image.load(os.path.join(ASSETS_FOLDER,"upgrade1.png")).convert()
upgradeGeel = pygame.image.load(os.path.join(ASSETS_FOLDER,"upgrade2.png")).convert()
upgradeSleutel = pygame.image.load(os.path.join(ASSETS_FOLDER,"upgrade_sleutel.png")).convert()
heartSprite = pygame.image.load(os.path.join(ASSETS_FOLDER,"heart.png")).convert()
heartRect = heartSprite.get_rect()# change topleft

bx, by = (int(WIDTH/2), playerY)
sx, sy = (ballSpeed, ballSpeed)
ballSprite = pygame.image.load(os.path.join(ASSETS_FOLDER,"ball.png"))
ballBigSprite = pygame.image.load(os.path.join(ASSETS_FOLDER,"ball_normal_big.png"))
batRect = batSprite.get_rect(topleft=(bx-22,playerY))
batLangRect = batLangSprite.get_rect(topleft=(bx-22,playerY))
ballRect = ballSprite.get_rect(topleft=(bx+int(batRect[2]/2)-26,by-int(batRect[3])))
ballBigRect = ballBigSprite.get_rect(topleft = (bx,by))
mouseX = bx
# steen initialiseren
brick = pygame.image.load(os.path.join(ASSETS_FOLDER,"brick.png")) #ID = 0
brickBlauw = pygame.image.load(os.path.join(ASSETS_FOLDER,"brick_blue_purple.png")) #ID = 1
brickGeel = pygame.image.load(os.path.join(ASSETS_FOLDER,"brick_yellow_black.png")) #ID = 2
brickSleutel = pygame.image.load(os.path.join(ASSETS_FOLDER,"brick_sleutel.png"))   #ID = 3
