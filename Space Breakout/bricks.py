import pygame, os, sys
from pygame import *
import random as r
#GLOBALE STATISCHE VARIABELEN
WIDTH = 800
HEIGHT = 600
KEYBOARD_SPEED = 20
DEVELOPER_TOOLS = True #verander dit voor Cheatkeys te gebruiken
GAME_FOLDER = os.path.dirname(__file__)
#GAME_FOLDER = os.path.dirname("__file__") 
#                                 ^
# enkel nodig voor als je een build wilt maken met cx_Freeze "python setup.py build"
ASSETS_FOLDER = os.path.join(GAME_FOLDER,"Assets")
def main():
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    #initiatleer DISPLAYS
    mainSurface = pygame.display.set_mode((WIDTH,HEIGHT))
    menuSurface = pygame.display.set_mode((WIDTH,HEIGHT))
    gameOverSurface = pygame.display.set_mode((WIDTH,HEIGHT))
    nextLevelSurface = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Bricks")
    pygame.mouse.set_visible(0)
    #kleuren voordien instellen
    black = pygame.Color(0,0,0)
    white = pygame.Color(255,255,255)
    #Lijst van Dynamische Variabelen
    showMenu = True     #Toont MENU DISPsLAY
    gameOn = True       #Laat het volledige spel afspelen.False: Spel stopt
    levelsPlaying = False   #toont het DISPLAY waar levels worden gespeeld
    gameOverMenu = False    #Toont het DISPLAY GAME OVER
    changeLevel = False     #
    showCheatKeys = False
    level = 1
    keyDown = None
    fontobj = pygame.font.Font("freesansbold.ttf", 14)
    fontobjTITEL = pygame.font.Font("freesansbold.ttf", 24)
    fontobjCOMBO = pygame.font.Font("freesansbold.ttf",30)
    fontCheatKeys = pygame.font.Font(None,22)
    score = 0
    scoreTemp = 0   
    #adding sounds
    #FIXME:PATH NOT CORRECT!FIXME:
    pygame.mixer.music.load(os.path.join(ASSETS_FOLDER,"8-bit-music-loop.wav"))
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
    yBg = 0 
    xBg = 0
    # pallet initialiseren
    batSprite = pygame.image.load(os.path.join(ASSETS_FOLDER,"bat.png")).convert()
    batLangSprite = pygame.image.load(os.path.join(ASSETS_FOLDER,"bat_lang.png")).convert()
    upgradeBlauw = pygame.image.load(os.path.join(ASSETS_FOLDER,"upgrade1.png")).convert()
    upgradeGeel = pygame.image.load(os.path.join(ASSETS_FOLDER,"upgrade2.png")).convert()
    upgradeSleutel = pygame.image.load(os.path.join(ASSETS_FOLDER,"upgrade_sleutel.png")).convert()
    heartSprite = pygame.image.load(os.path.join(ASSETS_FOLDER,"heart.png")).convert()
    heartRect = heartSprite.get_rect()# change topleft
    upgradeRectList = []
    playerY = 540
    lives = 3
    bx, by = (int(WIDTH/2), playerY)
    ballSpeed = 4
    ballMaxSpeed = 10
    sx, sy = (ballSpeed, ballSpeed)
    ballSprite = pygame.image.load(os.path.join(ASSETS_FOLDER,"ball.png"))
    ballServed = False
    changeBall = False
    changeBat = False
    scoreForExtraLife = 12
    maxLives = 6
    scoreComboMultiplier = 2
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
    bricksRects,bricks = createBricks(4,2,2,level) #aatalSpecialeBricks
    # events
    menuSurface.fill(black)
    while gameOn:
        pygame.mixer.music.play(-1)
        while showMenu:
            welkomLabel = fontobjTITEL.render('SPACE BREAKOUT!', True, white,black)
            uitlegLijn1Label = fontobj.render('Gebruik ARROW KEYS of je MUIS',True,white,black)
            uitleglijn2Label = fontobj.render('Druk SPATIE of op je muisknop voor de ball te starten!', True, white,black)
            startLabel = fontobj.render('Press any key to continue...',True, white,black)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
                    showMenu = False
                    levelsPlaying = True
            menuSurface.blit(bgMain,(0,0))
            menuSurface.blit(welkomLabel,(400-int(welkomLabel.get_width()/2),50))
            menuSurface.blit(uitlegLijn1Label,(400-int(uitlegLijn1Label.get_width()/2),150))
            menuSurface.blit(uitleglijn2Label,(400-int(uitleglijn2Label.get_width()/2),180))
            menuSurface.blit(startLabel,(400-int(startLabel.get_width()/2),300))
            pygame.display.update()
            FPSCLOCK.tick(10)
        mainSurface.fill(black)
        #setup upgrades
        while levelsPlaying:
            #backgrouns scrolling
            if (level%4) == 0:
                relatief_Y = yBg % bg1.get_rect().height
                mainSurface.blit(bg1,(0,relatief_Y - bg1.get_rect().height))
                if relatief_Y < HEIGHT:
                    mainSurface.blit(bg1, (0,relatief_Y))
            if (level%4) == 1:
                relatief_Y = yBg % bg2.get_rect().height
                mainSurface.blit(bg2,(0,relatief_Y - bg2.get_rect().height))
                if relatief_Y < HEIGHT:
                    mainSurface.blit(bg2, (0,relatief_Y))
            if (level%4) == 2:
                relatief_Y = yBg % bg3.get_rect().height
                mainSurface.blit(bg3,(0,relatief_Y - bg3.get_rect().height))
                if relatief_Y < HEIGHT:
                    mainSurface.blit(bg3, (0,relatief_Y))
            if (level%4) == 3:
                relatief_Y = yBg % bg4.get_rect().height
                mainSurface.blit(bg4,(0,relatief_Y - bg4.get_rect().height))
                if relatief_Y < HEIGHT:
                    mainSurface.blit(bg4, (0,relatief_Y))
            yBg += 1
            #levens
            for i in range(lives): #3 levens = 0,1,2
                x,y = ((heartRect[2]*i)+5,5)
                mainSurface.blit(heartSprite,(x,y))
            #onscreen text
            scoreLabel = fontobjTITEL.render(str(score),True,white,None)
            scoreComboLabel = fontobjCOMBO.render("combo!  "+ str(scoreTemp),True,white,None)
            LevelindicatorLabel = fontobj.render("Level:"+str(level),True,white,None)
            mainSurface.blit(scoreLabel,(WIDTH-scoreLabel.get_width()-5,5))
            if DEVELOPER_TOOLS and showCheatKeys:
                cheatKeysLabel1 = fontCheatKeys.render("key 1:..increase combo score",True,white,None)
                cheatKeysLabel2 = fontCheatKeys.render("key 2:..................delete steen",True,white,None)
                cheatKeysLabel3 = fontCheatKeys.render("key 3:.................volgend level",True,white,None)
                cheatKeysLabel4 = fontCheatKeys.render("key 4:....................extra leven",True,white,None)
                cheatKeysLabel5 = fontCheatKeys.render("key 5:.............maak bal groot",True,white,None)
                cheatKeysLabel6 = fontCheatKeys.render("key 6:........maak player groot",True,white,None)
                cheatKeysLabel7 = fontCheatKeys.render("key 7:........increase ball speed",True,white,None)
                cheatKeysLabel8 = fontCheatKeys.render("key ENTER:..........Keys Menu",True,white,None)
                mainSurface.blit(cheatKeysLabel1,(WIDTH-cheatKeysLabel1.get_width(),HEIGHT-cheatKeysLabel1.get_height()*1))
                mainSurface.blit(cheatKeysLabel2,(WIDTH-cheatKeysLabel2.get_width(),HEIGHT-cheatKeysLabel1.get_height()*2))
                mainSurface.blit(cheatKeysLabel3,(WIDTH-cheatKeysLabel3.get_width(),HEIGHT-cheatKeysLabel1.get_height()*3))
                mainSurface.blit(cheatKeysLabel4,(WIDTH-cheatKeysLabel4.get_width(),HEIGHT-cheatKeysLabel1.get_height()*4))
                mainSurface.blit(cheatKeysLabel5,(WIDTH-cheatKeysLabel5.get_width(),HEIGHT-cheatKeysLabel1.get_height()*5))
                mainSurface.blit(cheatKeysLabel6,(WIDTH-cheatKeysLabel6.get_width(),HEIGHT-cheatKeysLabel1.get_height()*6))
                mainSurface.blit(cheatKeysLabel7,(WIDTH-cheatKeysLabel7.get_width(),HEIGHT-cheatKeysLabel1.get_height()*7))
                mainSurface.blit(cheatKeysLabel8,(WIDTH-cheatKeysLabel8.get_width(),HEIGHT-cheatKeysLabel1.get_height()*8))
            if scoreTemp > 4 and changeBall:
                mainSurface.blit(scoreComboLabel,(400-int(scoreComboLabel.get_width()/2),6))
            if scoreTemp > 2 and not changeBall:
                mainSurface.blit(scoreComboLabel,(400-int(scoreComboLabel.get_width()/2),6))
            mainSurface.blit(LevelindicatorLabel,(0,HEIGHT-LevelindicatorLabel.get_height()-10))
            #events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if not ballServed:
                        ballServed = True
                elif event.type == pygame.MOUSEMOTION:
                    mouseX = event.pos[0] #mousex = X positie van de muis
                    if(mouseX < WIDTH -55 or mouseX <= 55 ):#
                        if changeBat:
                            batLangRect.topleft = (mouseX-int(batLangRect[2]/2),playerY)
                            ballRect.topleft = (batLangRect[2]/2,playerY)
                        elif not changeBat:
                            batRect.topleft = (mouseX-int(batRect[2]/2),playerY)
                            ballRect.topleft = (batRect[2]/2,playerY)
                    else:
                        if changeBat:
                            batLangRect.topleft =(WIDTH-55,playerY)
                        if not changeBat:
                            batRect.topleft = (WIDTH-55, playerY)
                    if not ballServed:
                        if changeBat:
                            if changeBall:
                                bx,by = (mouseX-int(ballBigRect[2]/2),playerY-batLangRect[3])
                            elif not changeBall:
                                bx,by = (mouseX-int(ballRect[2]/2),playerY-batLangRect[3])
                            ballRect.topleft = (bx,by)                    
                        elif not changeBat:
                            if changeBall:
                                bx,by = (mouseX-int(ballBigRect[2]/2),playerY-batRect[3])
                            elif not changeBall:
                                bx,by = (mouseX-int(ballRect[2]/2),playerY-batRect[3])
                            ballRect.topleft = (bx,by)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        keyDown = "K_LEFT"
                        if changeBat:
                            if not ballServed:
                                bx,by = (batLangRect[0]-int(batLangRect[2]/2)-int(ballRect[2]/2),playerY-batLangRect[3])
                                ballRect.topleft = (bx,by)
                            batLangRect.topleft = (batLangRect[0]-KEYBOARD_SPEED,playerY)
                        elif not changeBat:
                            if not ballServed:
                                bx,by = (batRect[0]-int(batRect[2]/2)-int(ballRect[2]/2),playerY-batRect[3])
                                ballRect.topleft = (bx,by)
                            batRect.topleft = (batRect[0]-KEYBOARD_SPEED,playerY)
                    if event.key == pygame.K_RIGHT:
                        keyDown = "K_RIGHT"
                        if changeBat:
                            if not ballServed:
                                bx,by = (batLangRect[0]-int(batLangRect[2]/2)-int(ballRect[2]/2),playerY-batLangRect[3])
                                ballRect.topleft = (bx,by)
                            batLangRect.topleft = (batLangRect[0]+KEYBOARD_SPEED,playerY)
                        elif not changeBat:
                            if not ballServed:
                                bx,by = (batRect[0]-int(batRect[2]/2)-int(ballRect[2]/2),playerY-batRect[3])
                                ballRect.topleft = (bx,by)
                            batRect.topleft = (batRect[0]+20,playerY)
                    if DEVELOPER_TOOLS:
                        if event.key == pygame.K_RETURN:
                            if showCheatKeys:
                                showCheatKeys = False
                            else:
                                showCheatKeys = True
                        if event.key == pygame.K_1:
                            scoreTemp +=1
                        if event.key == pygame.K_2:
                            del bricksRects[0]
                            scoreTemp += 1
                        if event.key == pygame.K_3:
                            del(bricksRects[:])
                        if event.key == pygame.K_4:
                            if(lives < maxLives):
                                lives += 1
                        if event.key == pygame.K_5:
                            changeBall = True
                        if event.key == pygame.K_6:
                            changeBat = True
                        if event.key == pygame.K_7:
                            if ballSpeed < ballMaxSpeed:
                                ballSpeed += 1
                                if sx < 0 and sy < 0:
                                    sx,sy = (ballSpeed,ballSpeed)
                                elif sx > 0 and sy > 0:
                                    sx,sy = (ballSpeed,ballSpeed)
                    if event.key == pygame.K_SPACE:
                        if not ballServed:
                            ballServed = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and keyDown == "K_LEFT":
                        keyDown = None
                    if event.key == pygame.K_RIGHT and keyDown == "K_RIGHT":
                        keyDown = None
            if keyDown:
                if keyDown == "K_LEFT":
                    batRect.topleft = (batRect[0]-KEYBOARD_SPEED,playerY)
                    batLangRect.topleft = (batLangRect[0]-KEYBOARD_SPEED,playerY)
                    if changeBat:
                        if not ballServed:
                            bx,by = (batLangRect[0]+int(batLangRect[2]/2)-int(ballRect[2]/2),playerY-batLangRect[3])
                            ballRect.topleft = (bx,by)
                    elif not changeBat:
                        if not ballServed:
                            bx,by = (batRect[0]+int(batRect[2]/2)-int(ballRect[2]/2),playerY-batRect[3])
                            ballRect.topleft = (bx,by)
                if keyDown == "K_RIGHT":
                    batLangRect.topleft = (batLangRect[0]+KEYBOARD_SPEED,playerY)
                    batRect.topleft = (batRect[0]+KEYBOARD_SPEED,playerY)
                    if changeBat:
                        if not ballServed:
                            bx,by = (batLangRect[0]+int(batLangRect[2]/2)-int(ballRect[2]/2),playerY-batLangRect[3])
                            ballRect.topleft = (bx,by)
                    elif not changeBat:
                        if not ballServed:
                            bx,by = (batRect[0]+int(batRect[2]/2)-int(ballRect[2]/2),playerY-batRect[3])
                            ballRect.topleft = (bx,by)
            if changeBat:
                mainSurface.blit(batLangSprite, batLangRect)
            if not changeBat:
                mainSurface.blit(batSprite, batRect)
            # teken stenen
            for c in bricksRects:
                status = ""
                index = None
                for b in bricks:
                    if b[-1] == 0 and b[-2]==c:
                        status = ""
                    elif b[-1] == 1 and b[-2]==c:
                        status = "upgradeBlauw"
                    elif b[-1] == 2 and b[-2]==c:
                        status = "upgradeGeel"
                    elif b[-1] == 3 and b[-2]==c:
                        status = "upgradeSleutel"
                if status == "":
                    index = bricks.index((c,0))
                    mainSurface.blit(brick,bricks[index][-2])
                elif status == "upgradeBlauw":
                    index = bricks.index((c,1))
                    mainSurface.blit(brickBlauw,bricks[index][-2])
                elif status == "upgradeGeel":
                    index = bricks.index((c,2))
                    mainSurface.blit(brickGeel,bricks[index][-2])
                elif status == "upgradeSleutel":
                    index = bricks.index((c,3))
                    mainSurface.blit(brickSleutel,bricks[index][-2])
            #teken upgrades
            for u in upgradeRectList:
                #collision detection
                if(u[-1]==1):
                    mainSurface.blit(upgradeBlauw,(u[-2].topleft))
                elif(u[-1]==2):
                    mainSurface.blit(upgradeGeel,(u[-2].topleft))
                elif(u[-1]==3):
                    mainSurface.blit(upgradeSleutel,(u[-2].topleft))
                u[-2].topleft = (u[-2][0],u[-2][1]+ballSpeed-1) #upgrades naar beneden laten vallen, speed = 2
                if changeBat:
                    if(batLangRect.colliderect(u[-2]) and u[-1]==1):
                        del(upgradeRectList[upgradeRectList.index(u)])
                        changeBall = True
                    elif(batLangRect.colliderect(u[-2]) and u[-1]==2):
                        del(upgradeRectList[upgradeRectList.index(u)])
                        batLangRect.topleft = batRect.topleft
                        changeBat = True
                elif not changeBat:
                    if(batRect.colliderect(u[-2]) and u[-1]==1):
                        del(upgradeRectList[upgradeRectList.index(u)])
                        changeBall = True
                    elif(batRect.colliderect(u[-2]) and u[-1]==2):
                        del(upgradeRectList[upgradeRectList.index(u)])
                        batLangRect.topleft = batRect.topleft
                        changeBat = True
                if(batRect.colliderect(u[-2]) and u[-1]==3) or (batLangRect.colliderect(u[-2]) and u[-1]==3):
                    del(upgradeRectList[upgradeRectList.index(u)])
                    changeBat = False
                    levelsPlaying = False
                    changeLevel = True
                    score += scoreTemp

                #out of bound detection
                if(u[-2][1] >= HEIGHT-8): 
                    del(upgradeRectList[upgradeRectList.index(u)])
            # teken pallet en bal
            if ballServed:
                bx -= sx
                by -= sy
                ballRect.topleft = (bx,by)
                ballBigRect.topleft = (bx,by)
            if(by <= 0): #onderkant collide
                by = 0 
                sy *= -1
            if(changeBall and by >= HEIGHT-24 ) or (not changeBall and by >= HEIGHT-16):  #bovenkant collide
                if not changeBall:
                    by = HEIGHT-16
                else:
                    by = HEIGHT-24
                sy *= -1
                ballServed = False
                if changeBat:
                    bx,by = (mouseX-int(ballRect[2]/2),playerY-batLangRect[3])
                elif not changeBat:
                    bx,by = (mouseX-int(ballRect[2]/2),playerY-batRect[3])
                if changeBall:
                    changeBall = False
                scoreTemp = 0
                ballRect.topleft = (bx,by)
                lives -= 1
                if lives == 0:
                    levelsPlaying = False
                    gameOverMenu = True                
            if(bx <= 0):
                sx *= -1
                bx = 0
            if(bx >= WIDTH):
                sx *= -1
                bx = WIDTH
            if not changeBall:
                mainSurface.blit(ballSprite, ballRect)
            else:
                ballBigRect.topleft = (bx,by)
                mainSurface.blit(ballBigSprite,ballBigRect)
            # hoofdlogicad
            # botsingen detecteren
            if not changeBall and ((ballRect.colliderect(batRect) and not changeBat)or(ballRect.colliderect(batLangRect) and changeBat)):
                #botsting met kleine bal
                pygame.mixer.Sound.play(batBotsingSound)
                by = playerY-16
                sy *= -1
                if scoreTemp >= scoreForExtraLife and lives < maxLives:
                    lives += 1
                score += scoreTemp
                scoreTemp = 0
                if changeBat:
                    batRect.topleft = batLangRect.topleft
                changeBat = False
            elif changeBall and ((ballBigRect.colliderect(batRect) and not changeBat)or(ballBigRect.colliderect(batLangRect) and changeBat)):
                #botsing met grote bal
                pygame.mixer.Sound.play(batBotsingSound)
                by = playerY-24
                sy *= -1
                changeBall = False
                if changeBat:
                    batRect.topleft = batLangRect.topleft
                changeBat = False
                if scoreTemp >= scoreForExtraLife and lives < maxLives:
                    lives += 1
                score += scoreTemp*scoreComboMultiplier
                scoreTemp = 0
            brickHitIndex = []
            if not changeBall:
                brickHitIndex = ballRect.collidelist(bricksRects)
            else:
                brickHitIndex = ballBigRect.collidelist(bricksRects)
            if brickHitIndex >= 0: # geen botsing = -1
                if changeBall and scoreTemp > 4:
                    scoreTemp += 4
                if not changeBall and scoreTemp > 2:
                    scoreTemp += 2
                else:
                    scoreTemp += 1
                hb = bricksRects[brickHitIndex]
                for b in bricks:
                    if b[-1] == 1 and b[-2]==hb:
                        upX,upY = hb[0],hb[1]
                        upgradeRectList.append(( Rect(upX+8, (upY+int((hb.height/2)+8)),16,16),1))
                    elif b[-1] == 2 and b[-2]==hb:
                        upX,upY = hb[0],hb[1]
                        upgradeRectList.append(( Rect(upX+8, (upY+int((hb.height/2)+8)),16,16),2))
                    elif b[-1] == 3 and b[-2]==hb:
                        upX,upY = hb[0],hb[1]
                        upgradeRectList.append(( Rect(upX+8, (upY+int((hb.height/2)+8)),16,16),3))
                mx = bx + 4
                if mx > hb.x + hb.width or mx < hb.x:
                    sx *= -1
                else:
                    sy *= -1
                del(bricksRects[brickHitIndex])
            if not bricksRects:
                levelsPlaying = False
                changeLevel = True
            pygame.display.update()
            FPSCLOCK.tick(30) #FPS op juiste snelheid zetten
        mainSurface.fill(black)
        while changeLevel:
            #draw backgroud
            relatief_X = xBg % nextLevelSurface.get_rect().height
            nextLevelSurface.blit(nextLevelBg,(relatief_X - nextLevelSurface.get_rect().width,0))
            if relatief_X < WIDTH:
                nextLevelSurface.blit(nextLevelBg, (relatief_X,0))
            xBg += 1
            #draw labels
            levelLabel1 = fontobjCOMBO.render("Congratulation!",True,white,None)
            levelLabel2 = fontobjCOMBO.render("You completed LEVEL "+ str(level) + "!",True,white,None)
            nextLevelLabel = fontobjTITEL.render("proceed to next level, press SPACE..",True,white,None)
            nextLevelSurface.blit(levelLabel1,(400-int(levelLabel1.get_width()/2),int(HEIGHT/4)))
            nextLevelSurface.blit(levelLabel2,(400-int(levelLabel2.get_width()/2),int(HEIGHT/4)+40))
            nextLevelSurface.blit(nextLevelLabel,(400-int(nextLevelLabel.get_width()/2),int(HEIGHT/2)+50))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        keyDown = ""
                        scoreTemp = 0
                        changeLevel = False
                        levelsPlaying = True
                        level += 1
                        del upgradeRectList[:]
                        ballServed = False
                        changeBall = False
                        if ballSpeed < ballMaxSpeed:
                            ballSpeed += 1
                        sx, sy = (ballSpeed, ballSpeed)
                        bx,by = (mouseX-int(ballRect[2]/2),playerY-batRect[3])                    
                        ballRect.topleft = (bx,by) = ((WIDTH/2)-int(ballRect[2]/2),playerY-ballRect[3]) #FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:FIXME:
                        batRect.topleft = batLangRect.topleft = ((WIDTH/2)-int(batRect[2]/2),playerY)
                        bricksRects,bricks = createBricks(4,2,2,level)
            pygame.display.update()
            FPSCLOCK.tick(30)
            mainSurface.fill(black)
        while gameOverMenu:
            eindScore = fontobjTITEL.render("Eindscore: " + str(score), True, white, None)
            opnieuwText = fontobj.render("Druk SPATIE voor opnieuw te spelen", True, white,None)
            afsluitText = fontobj.render("Druk ESC voor af te sluiten", True, white,None)
            gameOverSurface.blit(gameOverBg,(0,0))
            gameOverSurface.blit(eindScore,(400-int(eindScore.get_width()/2),50))
            gameOverSurface.blit(opnieuwText,(400-int(opnieuwText.get_width()/2),500))
            gameOverSurface.blit(afsluitText,(400-int(afsluitText.get_width()/2),550))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        gameOverMenu = False
                        levelsPlaying = True
                        eindScore,score,scoreTemp = 0,0,0
                        lives = 3
                        del upgradeRectList[:]
                        ballServed = False
                        changeBall = False
                        ballSpeed = 4
                        sx,sy = (ballSpeed,ballSpeed)
                        level = 1
                        bricksRects,bricks = createBricks(4,2,2,level)
                    if event.key == pygame.K_ESCAPE:
                        gameOn = False
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
            FPSCLOCK.tick(10)
def createBricks(specials1PerLevel,specials2PeLevel,sleutels,level):
    rands = specials1PerLevel*level
    rands2 = specials2PeLevel*level
    rands3 = sleutels
    bricksTemp,bricksRectsTemp,randomIndex1,randomIndex2,randomIndex3 = [],[],[],[],[]
    YrangeVoorX,YrangeVoorY = 3+level,6+level
    XrangeVoorX,XrangeVoorY = 4+level,8+level
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
        brickY = (y * 16) -100 + ((HEIGHT-(yRange*16))/2)
        for x in range(xRange):
            brickX = (x*48) + ((WIDTH-(xRange*48))/2)
            if level >= 10:
                tekenkansY = r.randrange(0,2)
            else:
                tekenkansY = r.randrange(0,12-level)
            if tekenkansY != 0 or (x,y) in randomIndex3:
                if (x,y) in randomIndex3:
                    bricksTemp.append((Rect(brickX,brickY,48,16),3)) #brick_sleutel
                elif (x,y) in randomIndex2:
                    bricksTemp.append((Rect(brickX,brickY,48,16),2)) #brick_geel
                elif(x,y) in randomIndex1:
                    bricksTemp.append((Rect(brickX,brickY,48,16),1)) #brick_blauw
                else:
                    bricksTemp.append((Rect(brickX,brickY,48,16),0)) #brick
                bricksRectsTemp.append(Rect(brickX,brickY,48,16))
    return bricksRectsTemp,bricksTemp
def createRandoms(randoms):
    rands = []
    for i in range(randoms):
        rands.append(r.randrange(1,10))
    return rands
if __name__ == '__main__':  
    main()
