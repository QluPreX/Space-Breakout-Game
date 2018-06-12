import pygame, os, sys
from pygame import *
import random as r
#GLOBALE  VARIABELEN
def main():
    pygame.init()
    pygame.display.set_mode((0,0))
    pygame.display.set_caption("Bricks")
    pygame.mouse.set_visible(0)
    pygame.mixer.music.load(os.path.join(gb.ASSETS_FOLDER,"8-bit-music-loop.wav"))
    # events
    gb.menuSurface.fill(gb.black)
    #setup variabelen
        #booleans
    while gb.gameOn:
        pygame.mixer.music.play(-1)
        while gb.showMenu:
            welkomLabel = gb.fontobjTITEL.render('SPACE BREAKOUT!', True, gb.white,gb.black)
            uitlegLijn1Label = gb.fontobj.render('Gebruik ARROW KEYS of je MUIS',True,gb.white,gb.black)
            uitleglijn2Label = gb.fontobj.render('Druk SPATIE of op je muisknop voor de ball te starten!', True, gb.white,gb.black)
            startLabel = gb.fontobj.render('Press any key to continue...',True, gb.white,gb.black)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
                    gb.showMenu = False
                    gb.levelsPlaying = True
            drawMultipleLines()
            gb.menuSurface.blit(gb.bgMain,(0,0))
            gb.menuSurface.blit(welkomLabel,(400-int(welkomLabel.get_width()/2),50))
            gb.menuSurface.blit(uitlegLijn1Label,(400-int(uitlegLijn1Label.get_width()/2),150))
            gb.menuSurface.blit(uitleglijn2Label,(400-int(uitleglijn2Label.get_width()/2),180))
            gb.menuSurface.blit(startLabel,(400-int(startLabel.get_width()/2),300))
            pygame.display.update()
            gb.FPSCLOCK.tick(10)
        gb.mainSurface.fill(gb.black)
        #setup upgrades
        gb.bricksRects,gb.bricks = createBricks(4,2,2) #aatalSpecialeBricks
        while gb.levelsPlaying:
            #backgrouns scrolling
            setDynamicBackground()
            #levens
            for i in range(gb.lives): #3 levens = 0,1,2
                x,y = ((gb.heartRect[2]*i)+5,5)
                gb.mainSurface.blit(gb.heartSprite,(x,y))
            #onscreen text
            scoreLabel = gb.fontobjTITEL.render(str(gb.score),True,gb.white,None)
            scoreComboLabel = gb.fontobjCOMBO.render("combo!  "+ str(gb.scoreTemp),True,gb.white,None)
            LevelindicatorLabel = gb.fontobj.render("Level:"+str(gb.level),True,gb.white,None)
            gb.mainSurface.blit(scoreLabel,(gb.WIDTH-scoreLabel.get_width()-5,5))
            if gb.DEVELOPER_TOOLS and gb.showCheatKeys:

            if gb.scoreTemp > 4 and gb.changeBall:
                gb.mainSurface.blit(scoreComboLabel,(400-int(scoreComboLabel.get_width()/2),6))
            if gb.scoreTemp > 2 and not gb.changeBall:
                gb.mainSurface.blit(scoreComboLabel,(400-int(scoreComboLabel.get_width()/2),6))
            gb.mainSurface.blit(LevelindicatorLabel,(0,gb.HEIGHT-LevelindicatorLabel.get_height()-10))
            #events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if not gb.ballServed:
                        gb.ballServed = True
                elif event.type == pygame.MOUSEMOTION:
                    checkMouseEvents(event)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        gb.keyDown = "K_LEFT"
                        if gb.changeBat:
                            if gb.batLangRect[0] > 0:
                                if not gb.ballServed:
                                    gb.bx,gb.by = (gb.batLangRect[0]-int(gb.batLangRect[2]/2)-int(gb.ballRect[2]/2),gb.playerY-gb.batLangRect[3])
                                    gb.ballRect.topleft = (gb.bx,gb.by)
                                gb.batLangRect.topleft = (gb.batLangRect[0]-gb.KEYBOARD_SPEED,gb.playerY)
                        elif not gb.changeBat:
                            if gb.batRect[0] > 0:
                                if not gb.ballServed:
                                    gb.bx,gb.by = (gb.batRect[0]-int(gb.batRect[2]/2)-int(gb.ballRect[2]/2),gb.playerY-gb.batRect[3])
                                    gb.ballRect.topleft = (gb.bx,gb.by)
                                gb.batRect.topleft = (gb.batRect[0]-gb.KEYBOARD_SPEED,gb.playerY)
                    if event.key == pygame.K_RIGHT:
                        gb.keyDown = "K_RIGHT"
                        if gb.changeBat:
                            if gb.batLangRect[0] < gb.WIDTH-gb.batLangRect[2]:
                                if not gb.ballServed:
                                    gb.bx,gb.by = (gb.batLangRect[0]-int(gb.batLangRect[2]/2)-int(gb.ballRect[2]/2),gb.playerY-gb.batLangRect[3])
                                    gb.ballRect.topleft = (gb.bx,gb.by)
                                gb.batLangRect.topleft = (gb.batLangRect[0]+gb.KEYBOARD_SPEED,gb.playerY)
                        elif not gb.changeBat:
                            if gb.batRect[0] < gb.WIDTH-gb.batRect[2]:
                                if not gb.ballServed:
                                    gb.bx,gb.by = (gb.batRect[0]-int(gb.batRect[2]/2)-int(gb.ballRect[2]/2),gb.playerY-gb.batRect[3])
                                    gb.ballRect.topleft = (gb.bx,gb.by)
                                gb.batRect.topleft = (gb.batRect[0]+20,gb.playerY)
                    if(gb.DEVELOPER_TOOLS):
                        showCheatMenu(event)
                    if event.key == pygame.K_SPACE:
                        if not gb.ballServed:
                            gb.ballServed = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and gb.keyDown == "K_LEFT":
                        gb.keyDown = None
                    if event.key == pygame.K_RIGHT and gb.keyDown == "K_RIGHT":
                        gb.keyDown = None
            if gb.keyDown:
                if gb.keyDown == "K_LEFT":
                    if gb.changeBat:
                        if gb.batLangRect[0] > 0:
                            gb.batLangRect.topleft = (gb.batLangRect[0]-gb.KEYBOARD_SPEED,gb.playerY)
                        else:
                            gb.batLangRect.topleft = (0,gb.playerY)
                        if not gb.ballServed:
                                gb.bx,gb.by = (gb.batLangRect[0]+int(gb.batLangRect[2]/2)-int(gb.ballRect[2]/2),gb.playerY-gb.batLangRect[3])
                                gb.ballRect.topleft = (gb.bx,gb.by)
                    elif not gb.changeBat:
                        if gb.batRect[0] > 0:
                            gb.batRect.topleft = (gb.batRect[0]-gb.KEYBOARD_SPEED,gb.playerY)
                        else:
                            gb.batRect.topleft = (0,gb.playerY)
                        if not gb.ballServed:
                            gb.bx,gb.by = (gb.batRect[0]+int(gb.batRect[2]/2)-int(gb.ballRect[2]/2),gb.playerY-gb.batRect[3])
                            gb.ballRect.topleft = (gb.bx,gb.by)
                if gb.keyDown == "K_RIGHT":
                    if gb.changeBat:
                        if gb.batLangRect[0] < gb.WIDTH-gb.batLangRect[2]:
                            gb.batLangRect.topleft = (gb.batLangRect[0]+gb.KEYBOARD_SPEED,gb.playerY)
                        else:
                            gb.batLangRect.topleft = (gb.WIDTH-gb.batLangRect[2],gb.playerY)
                        if not gb.ballServed:
                            gb.bx,gb.by = (gb.batLangRect[0]+int(gb.batLangRect[2]/2)-int(gb.ballRect[2]/2),gb.playerY-gb.batLangRect[3])
                            gb.ballRect.topleft = (gb.bx,gb.by)
                    elif not gb.changeBat:
                        if gb.batRect[0] < gb.WIDTH-gb.batRect[2]:
                            gb.batRect.topleft = (gb.batRect[0]+gb.KEYBOARD_SPEED,gb.playerY)
                        else:
                            gb.batRect.topleft = (gb.WIDTH-gb.batRect[2],gb.playerY)
                        if not gb.ballServed:
                            gb.bx,gb.by = (gb.batRect[0]+int(gb.batRect[2]/2)-int(gb.ballRect[2]/2),gb.playerY-gb.batRect[3])
                            gb.ballRect.topleft = (gb.bx,gb.by)
            if gb.changeBat:
                gb.mainSurface.blit(gb.batLangSprite, gb.batLangRect)
            if not gb.changeBat:
                gb.mainSurface.blit(gb.batSprite, gb.batRect)
            # teken stenen
            for c in gb.bricksRects:
                status = ""
                index = None
                for b in gb.bricks:
                    if b[-1] == 0 and b[-2]==c:
                        status = ""
                    elif b[-1] == 1 and b[-2]==c:
                        status = "upgradeBlauw"
                    elif b[-1] == 2 and b[-2]==c:
                        status = "upgradeGeel"
                    elif b[-1] == 3 and b[-2]==c:
                        status = "upgradeSleutel"
                if status == "":
                    index = gb.bricks.index((c,0))
                    gb.mainSurface.blit(gb.brick,gb.bricks[index][-2])
                elif status == "upgradeBlauw":
                    index = gb.bricks.index((c,1))
                    gb.mainSurface.blit(gb.brickBlauw,gb.bricks[index][-2])
                elif status == "upgradeGeel":
                    index = gb.bricks.index((c,2))
                    gb.mainSurface.blit(gb.brickGeel,gb.bricks[index][-2])
                elif status == "upgradeSleutel":
                    index = gb.bricks.index((c,3))
                    gb.mainSurface.blit(gb.brickSleutel,gb.bricks[index][-2])
            #teken upgrades
            for u in gb.upgradeRectList:
                #collision detection
                if(u[-1]==1):
                    gb.mainSurface.blit(gb.upgradeBlauw,(u[-2].topleft))
                elif(u[-1]==2):
                    gb.mainSurface.blit(gb.upgradeGeel,(u[-2].topleft))
                elif(u[-1]==3):
                    gb.mainSurface.blit(gb.upgradeSleutel,(u[-2].topleft))
                u[-2].topleft = (u[-2][0],u[-2][1]+gb.ballSpeed-2) #upgrades naar beneden laten vallen, speed = 2
                if gb.changeBat:
                    if(gb.batLangRect.colliderect(u[-2]) and u[-1]==1):
                        del(gb.upgradeRectList[gb.upgradeRectList.index(u)])
                        gb.changeBall = True
                    elif(gb.batLangRect.colliderect(u[-2]) and u[-1]==2):
                        del(gb.upgradeRectList[gb.upgradeRectList.index(u)])
                        gb.batLangRect.topleft = gb.batRect.topleft
                        gb.changeBat = True
                elif not gb.changeBat:
                    if(gb.batRect.colliderect(u[-2]) and u[-1]==1):
                        del(gb.upgradeRectList[gb.upgradeRectList.index(u)])
                        gb.changeBall = True
                    elif(gb.batRect.colliderect(u[-2]) and u[-1]==2):
                        del(gb.upgradeRectList[gb.upgradeRectList.index(u)])
                        gb.batLangRect.topleft = gb.batRect.topleft
                        gb.changeBat = True
                if(gb.batRect.colliderect(u[-2]) and u[-1]==3) or (gb.batLangRect.colliderect(u[-2]) and u[-1]==3):
                    del(gb.upgradeRectList[gb.upgradeRectList.index(u)])
                    gb.changeBat = False
                    gb.levelsPlaying = False
                    gb.changeLevel = True
                    gb.score += gb.scoreTemp

                #out of bound detection
                if(u[-2][1] >= gb.HEIGHT-8):
                    del(gb.upgradeRectList[gb.upgradeRectList.index(u)])
            # teken pallet en bal
            if gb.ballServed:
                gb.bx -= gb.sx
                gb.by -=gb.sy
                gb.ballRect.topleft = (gb.bx,gb.by)
                gb.ballBigRect.topleft = (gb.bx,gb.by)
            if(gb.by <= 0): #onderkant collide
                gb.by = 0
                gb.sy *= -1
            if(gb.changeBall and gb.by >= gb.HEIGHT-24 ) or (not gb.changeBall and gb.by >= gb.HEIGHT-16):  #bovenkant collide
                if not gb.changeBall:
                    gb.by = gb.HEIGHT-16
                else:
                    gb.by = gb.HEIGHT-24
                gb.sy *= -1
                gb.ballServed = False
                if gb.changeBall:
                    gb.changeBall = False
                gb.scoreTemp = 0
                gb.bx,gb.by = (gb.batRect[0]+int((gb.batRect[2]/2)-gb.ballRect[2]/2),gb.playerY-gb.ballRect[3])
                gb.ballRect.topleft = gb.bx,gb.by
                gb.lives -= 1
                if gb.lives == 0:
                    gb.levelsPlaying = False
                    gb.gameOverMenu = True
            if(gb.bx <= 0):
                gb.sx *= -1
                gb.bx = 0
            if(gb.bx >= gb.WIDTH):
                gb.sx *= -1
                gb.bx = gb.WIDTH
            if not gb.changeBall:
                gb.mainSurface.blit(gb.ballSprite, gb.ballRect)
            else:
                gb.ballBigRect.topleft = (gb.bx,gb.by)
                gb.mainSurface.blit(gb.ballBigSprite,gb.ballBigRect)
            # hoofdlogicad
            # botsingen detecteren
            if not gb.changeBall and ((gb.ballRect.colliderect(gb.batRect) and not gb.changeBat)or(gb.ballRect.colliderect(gb.batLangRect) and gb.changeBat)):
                #botsting met kleine bal
                pygame.mixer.Sound.play(gb.batBotsingSound)
                gb.by = gb.playerY-16
                gb.sy *= -1
                if gb.scoreTemp >= gb.SCORE_FOR_EXTRA_LIFE and gb.lives < gb.maxLives:
                    gb.lives += 1
                gb.score += gb.scoreTemp
                gb.scoreTemp = 0
                if gb.changeBat:
                    gb.batRect.topleft = gb.batLangRect.topleft
                gb.changeBat = False
            elif gb.changeBall and ((gb.ballBigRect.colliderect(gb.batRect) and not gb.changeBat)or(gb.ballBigRect.colliderect(gb.batLangRect) and gb.changeBat)):
                #botsing met grote bal
                pygame.mixer.Sound.play(gb.batBotsingSound)
                gb.by = gb.playerY-24
                gb.sy *= -1
                gb.changeBall = False
                if gb.changeBat:
                    gb.batRect.topleft = gb.batLangRect.topleft
                changeBat = False
                if gb.scoreTemp >= gb.SCORE_FOR_EXTRA_LIFE and gb.lives < gb.maxLives:
                    gb.lives += 1
                gb.score += gb.scoreTemp*gb.scoreComboMultiplier
                gb.scoreTemp = 0
            brickHitIndex = []
            if not gb.changeBall:
                brickHitIndex = gb.ballRect.collidelist(gb.bricksRects)
            else:
                brickHitIndex = gb.ballBigRect.collidelist(gb.bricksRects)
            if brickHitIndex >= 0: # geen botsing = -1
                if gb.changeBall and gb.scoreTemp > 4:
                    gb.scoreTemp += 4
                if not gb.changeBall and gb.scoreTemp > 2:
                    gb.scoreTemp += 2
                else:
                    gb.scoreTemp += 1
                hb = gb.bricksRects[brickHitIndex]
                for b in gb.bricks:
                    if b[-1] == 1 and b[-2]==hb:
                        upX,upY = hb[0],hb[1]
                        gb.upgradeRectList.append(( Rect(upX+8, (upY+int((hb.height/2)+8)),16,16),1))
                    elif b[-1] == 2 and b[-2]==hb:
                        upX,upY = hb[0],hb[1]
                        gb.upgradeRectList.append(( Rect(upX+8, (upY+int((hb.height/2)+8)),16,16),2))
                    elif b[-1] == 3 and b[-2]==hb:
                        upX,upY = hb[0],hb[1]
                        gb.upgradeRectList.append(( Rect(upX+8, (upY+int((hb.height/2)+8)),16,16),3))
                mx = gb.bx + 4
                if mx > hb.x + hb.width or mx < hb.x:
                    gb.sx *= -1
                else:
                    gb.sy *= -1
                del(gb.bricksRects[brickHitIndex])
            if not gb.bricksRects:
                gb.levelsPlaying = False
                gb.changeLevel = True
            pygame.display.update()
            gb.FPSCLOCK.tick(30) #FPS op juiste snelheid zetten
        gb.mainSurface.fill(gb.black)
        while gb.changeLevel:
            #draw backgroud
            relatief_X = gb.xBg % gb.nextLevelSurface.get_rect().height
            gb.nextLevelSurface.blit(gb.nextLevelBg,(relatief_X - gb.nextLevelSurface.get_rect().width,0))
            if relatief_X < gb.WIDTH:
                gb.nextLevelSurface.blit(gb.nextLevelBg, (relatief_X,0))
            gb.xBg += 1
            #draw labels
            levelLabel1 = gb.fontobjCOMBO.render("Congratulation!",True,gb.white,None)
            levelLabel2 = gb.fontobjCOMBO.render("You completed LEVEL "+ str(gb.level) + "!",True,gb.white,None)
            nextLevelLabel = gb.fontobjTITEL.render("proceed to next level, press SPACE..",True,gb.white,None)
            gb.nextLevelSurface.blit(levelLabel1,(400-int(levelLabel1.get_width()/2),int(gb.HEIGHT/4)))
            gb.nextLevelSurface.blit(levelLabel2,(400-int(levelLabel2.get_width()/2),int(gb.HEIGHT/4)+40))
            gb.nextLevelSurface.blit(nextLevelLabel,(400-int(nextLevelLabel.get_width()/2),int(gb.HEIGHT/2)+50))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        gb.keyDown = ""
                        gb.scoreTemp = 0
                        gb.changeLevel = False
                        gb.levelsPlaying = True
                        gb.level += 1
                        del gb.upgradeRectList[:]
                        gb.ballServed = False
                        gb.changeBall = False
                        if gb.ballSpeed <gb.ballMaxSpeed:
                            gb.ballSpeed += 1
                        gb.sx, gb.sy = (gb.ballSpeed, gb.ballSpeed)
                        gb.bx,gb.by = (gb.mouseX-int(gb.ballRect[2]/2),gb.playerY-gb.batRect[3])
                        gb.ballRect.topleft = (gb.bx,gb.by) = ((gb.WIDTH/2)-int(gb.ballRect[2]/2),gb.playerY-gb.ballRect[3])
                        gb.batRect.topleft = gb.batLangRect.topleft = ((gb.WIDTH/2)-int(gb.batRect[2]/2),gb.playerY)
                        gb.bricksRects,bricks = createBricks(4,2,2)
            pygame.display.update()
            gb.FPSCLOCK.tick(30)
            gb.mainSurface.fill(gb.black)
        while gb.gameOverMenu:
            eindScore = gb.fontobjTITEL.render("Eindscore: " + str(gb.score), True, gb.white, None)
            opnieuwText = gb.fontobj.render("Druk SPATIE voor opnieuw te spelen", True, gb.white,None)
            afsluitText = gb.fontobj.render("Druk ESC voor af te sluiten", True, gb.white,None)
            gb.gameOverSurface.blit(gb.gameOverBg,(0,0))
            gb.gameOverSurface.blit(eindScore,(400-int(eindScore.get_width()/2),50))
            gb.gameOverSurface.blit(opnieuwText,(400-int(opnieuwText.get_width()/2),500))
            gb.gameOverSurface.blit(afsluitText,(400-int(afsluitText.get_width()/2),550))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        resetForNewGame()
                    if event.key == pygame.K_ESCAPE:
                        gb.gameOn = False
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
class gb():
        #statische variabelen
    pygame.init()
    WIDTH = 800
    HEIGHT = 600
    KEYBOARD_SPEED = 20
    DEVELOPER_TOOLS = True #verander dit voor Cheatkeys te gebruiken
    SCORE_FOR_EXTRA_LIFE = 12
    GAME_FOLDER = os.path.dirname(__file__)
    ASSETS_FOLDER = os.path.join(GAME_FOLDER,"Assets")
    #dynamsche variabelen
    showMenu = True
    gameOn = True
    levelsPlaying = False
    gameOverMenu = False
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
    #arrays
    upgradeRectList = []
    FPSCLOCK = pygame.time.Clock()
    #initiatleer DISPLAYS
    mainSurface = pygame.display.set_mode((WIDTH,HEIGHT))
    menuSurface = pygame.display.set_mode((WIDTH,HEIGHT))
    gameOverSurface = pygame.display.set_mode((WIDTH,HEIGHT))
    nextLevelSurface = pygame.display.set_mode((WIDTH,HEIGHT))

    black = pygame.Color(0,0,0)
    white = pygame.Color(255,255,255)
    fontobj = pygame.font.Font("freesansbold.ttf", 14)
    fontobjTITEL = pygame.font.Font("freesansbold.ttf", 24)
    fontobjCOMBO = pygame.font.Font("freesansbold.ttf",30)
    fontCheatKeys = pygame.font.Font(None,22)

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

def createBricks(specials1PerLevel,specials2PerLevel,sleutels, lvl = gb.level,height = gb.HEIGHT, width = gb.WIDTH):
    rands = specials1PerLevel*lvl
    rands2 = specials2PerLevel*lvl
    rands3 = sleutels
    bricksTemp,bricksRectsTemp,randomIndex1,randomIndex2,randomIndex3 = [],[],[],[],[]
    YrangeVoorX,YrangeVoorY = 4+lvl,8+lvl
    XrangeVoorX,XrangeVoorY = 5+lvl,9+lvl
    if(YrangeVoorY >= 20):
        YrangeVoorX,YrangeVoorY = 13,20
    if (XrangeVoorY >= 16):
        XrangeVoorX,XrangeVoorY = 13,16
    yRange = r.randrange(YrangeVoorX,YrangeVoorY)
    xRange = r.randrange(XrangeVoorX,XrangeVoorY) #max 16
    for i in range(rands):
        randomIndex1.append((r.randrange(xRange),r.randrange(yRange)))
    for i in range(rands2):
        randomIndex2.append((r.randrange(xRange),r.randrange(yRange)))
    for i in range(rands3):
        randomIndex3.append((r.randrange(xRange),r.randrange(yRange)))
    for y in range(yRange):
        brickY = (y * 16) -100 + ((height-(yRange*16))/2)
        for x in range(xRange):
            brickX = (x*48) + ((width-(xRange*48))/2)
            if lvl >= 10:
                tekenkansY = r.randrange(0,2)
            else:
                tekenkansY = r.randrange(0,12-lvl)
            if tekenkansY != 0 or (x,y) in randomIndex3: #100% kans voor 2 sleutels
                if (x,y) in randomIndex3:
                    bricksTemp.append((Rect(brickX,brickY,48,16),3)) #brick_sleutel
                elif (x,y) in randomIndex2:
                    bricksTemp.append((Rect(brickX,brickY,48,16),2)) #brick_geel
                elif(x,y) in randomIndex1:
                    bricksTemp.append((Rect(brickX,brickY,48,16),1)) #brick_blauw
                else:
                    bricksTemp.append((Rect(brickX,brickY,48,16),0)) #brick
                bricksRectsTemp.append(Rect(brickX,brickY,48,16))
    print(YrangeVoorX,YrangeVoorY, ":",XrangeVoorX,XrangeVoorY )
    return bricksRectsTemp,bricksTemp
def showCheatMenu(event):
    if event.key == pygame.K_RETURN:
        if gb.showCheatKeys:
            gb.showCheatKeys = False
        else:
            gb.showCheatKeys = True
    if event.key == pygame.K_1:
        gb.scoreTemp +=1
    if event.key == pygame.K_2:
        del gb.bricksRects[0]
        gb.scoreTemp += 1
    if event.key == pygame.K_3:
        del(gb.bricksRects[:])
    if event.key == pygame.K_4:
        if(gb.lives < gb.maxLives):
            gb.lives += 1
    if event.key == pygame.K_5:
        gb.changeBall = True
    if event.key == pygame.K_6:
        gb.changeBat = True
    if event.key == pygame.K_7:
        if gb.ballSpeed < gb.ballMaxSpeed:
            gb.ballSpeed += 1
            if gb.sx < 0 and gb.sy < 0:
                gb.sx,gb.sy = (gb.ballSpeed,gb.ballSpeed)
            elif gb.sx > 0 and gb.sy > 0:
                gb.sx,gb.sy = (gb.ballSpeed,gb.ballSpeed)
def resetForNewGame():
    gb.gameOverMenu = False
    gb.levelsPlaying = True
    gb.eindScore,gb.score,gb.scoreTemp = 0,0,0
    gb.lives = 3
    del gb.upgradeRectList[:]
    gb.ballServed = False
    gb.changeBall = False
    gb.ballSpeed = 4
    gb.sx,gb.y = (gb.ballSpeed,gb.ballSpeed)
    gb.level = 1
    gb.keyDown = ""
    gb.bricksRects,gb.bricks = createBricks(4,2,2)
def createRandoms(randoms):
    rands = []
    for i in range(randoms):
        rands.append(r.randrange(1,10))
    return rands
def checkMouseEvents(event):
    gb.mouseX = event.pos[0] #mousex = X positie van de muis
    if(gb.mouseX < gb.WIDTH or gb.mouseX <= 0 ):#
        if gb.changeBat:
            gb.batLangRect.topleft = (gb.mouseX-int(gb.batLangRect[2]/2),gb.playerY)
            gb.ballRect.topleft = (gb.batLangRect[2]/2,gb.playerY)
        elif not gb.changeBat:
            gb.batRect.topleft = (gb.mouseX-int(gb.batRect[2]/2),gb.playerY)
            gb.ballRect.topleft = (gb.batRect[2]/2,gb.playerY)
    if not gb.ballServed:
        if gb.changeBat:
            if gb.changeBall:
                gb.bx,gb.by = (gb.mouseX-int(gb.ballBigRect[2]/2),gb.playerY-gb.batLangRect[3])
            elif not gb.changeBall:
                gb.bx,gb.by = (gb.mouseX-int(gb.ballRect[2]/2),gb.playerY-gb.batLangRect[3])
            gb.ballRect.topleft = (gb.bx,gb.by)
        elif not gb.changeBat:
            if gb.changeBall:
                gb.bx,gb.by = (gb.mouseX-int(gb.ballBigRect[2]/2),gb.playerY-gb.batRect[3])
            elif not gb.changeBall:
                gb.bx,gb.by = (gb.mouseX-int(gb.ballRect[2]/2),gb.playerY-gb.batRect[3])
            gb.ballRect.topleft = (gb.bx,gb.by)
def setDynamicBackground():
    if (gb.level%4) == 0:
        relatief_Y = gb.yBg % gb.bg1.get_rect().height
        gb.mainSurface.blit(gb.bg1,(0,relatief_Y - gb.bg1.get_rect().height))
        if relatief_Y < gb.HEIGHT:
            gb.mainSurface.blit(gb.bg1, (0,relatief_Y))
    if (gb.level%4) == 1:
        relatief_Y = gb.yBg % gb.bg2.get_rect().height
        gb.mainSurface.blit(gb.bg2,(0,relatief_Y - gb.bg2.get_rect().height))
        if relatief_Y < gb.HEIGHT:
            gb.mainSurface.blit(gb.bg2, (0,relatief_Y))
    if (gb.level%4) == 2:
        relatief_Y = gb.yBg % gb.bg3.get_rect().height
        gb.mainSurface.blit(gb.bg3,(0,relatief_Y - gb.bg3.get_rect().height))
        if relatief_Y < gb.HEIGHT:
            gb.mainSurface.blit(gb.bg3, (0,relatief_Y))
    if (gb.level%4) == 3:
        relatief_Y = gb.yBg % gb.bg4.get_rect().height
        gb.mainSurface.blit(gb.bg4,(0,relatief_Y - gb.bg4.get_rect().height))
        if relatief_Y < gb.HEIGHT:
            gb.mainSurface.blit(gb.bg4, (0,relatief_Y))
    gb.yBg += 1
def drawMultipleLines(stringArray,color):
    for string in stringArray:
        stringLabel = gb.fontCheatKeys.render(string,True,color,None)
        gb.mainSurface.blit(stringLabel,(gb.WIDTH-string.get_width(),gb.HEIGHT-string.get_height()*))

    cheatKeysLabel1 = gb.fontCheatKeys.render("key 1:..increase combo score",True,gb.white,None)
    cheatKeysLabel2 = gb.fontCheatKeys.render("key 2:..................delete steen",True,gb.white,None)
    cheatKeysLabel3 = gb.fontCheatKeys.render("key 3:.................volgend level",True,gb.white,None)
    cheatKeysLabel4 = gb.fontCheatKeys.render("key 4:....................extra leven",True,gb.white,None)
    cheatKeysLabel5 = gb.fontCheatKeys.render("key 5:.............maak bal groot",True,gb.white,None)
    cheatKeysLabel6 = gb.fontCheatKeys.render("key 6:........maak player groot",True,gb.white,None)
    cheatKeysLabel7 = gb.fontCheatKeys.render("key 7:........increase ball speed",True,gb.white,None)
    cheatKeysLabel8 = gb.fontCheatKeys.render("key ENTER:..........Keys Menu",True,gb.white,None)
    gb.mainSurface.blit(cheatKeysLabel1,(gb.WIDTH-cheatKeysLabel1.get_width(),gb.HEIGHT-cheatKeysLabel1.get_height()*1))
    gb.mainSurface.blit(cheatKeysLabel2,(gb.WIDTH-cheatKeysLabel2.get_width(),gb.HEIGHT-cheatKeysLabel1.get_height()*2))
    gb.mainSurface.blit(cheatKeysLabel3,(gb.WIDTH-cheatKeysLabel3.get_width(),gb.HEIGHT-cheatKeysLabel1.get_height()*3))
    gb.mainSurface.blit(cheatKeysLabel4,(gb.WIDTH-cheatKeysLabel4.get_width(),gb.HEIGHT-cheatKeysLabel1.get_height()*4))
    gb.mainSurface.blit(cheatKeysLabel5,(gb.WIDTH-cheatKeysLabel5.get_width(),gb.HEIGHT-cheatKeysLabel1.get_height()*5))
    gb.mainSurface.blit(cheatKeysLabel6,(gb.WIDTH-cheatKeysLabel6.get_width(),gb.HEIGHT-cheatKeysLabel1.get_height()*6))
    gb.mainSurface.blit(cheatKeysLabel7,(gb.WIDTH-cheatKeysLabel7.get_width(),gb.HEIGHT-cheatKeysLabel1.get_height()*7))
    gb.mainSurface.blit(cheatKeysLabel8,(gb.WIDTH-cheatKeysLabel8.get_width(),gb.HEIGHT-cheatKeysLabel1.get_height()*8))
if __name__ == '__main__':

    main()
