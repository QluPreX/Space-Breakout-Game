import pygame, os, sys
from pygame import *
import random as r
#Globale statische variabelen
WIDTH = 800
HEIGHT = 600
DEVTOOLS = True #verander dit voor Cheatkeys te gebruiken
#game_folder = os.path.dirname(__file__)
game_folder = os.path.dirname("__file__") #enkel nodig voor als je een build wilt maken met cx_Freeze "python setup.py build"
assets_folder = os.path.join(game_folder,"Assets")
def main():
    pygame.init()
    fpsClock = pygame.time.Clock()
    mainSurface = pygame.display.set_mode((WIDTH,HEIGHT))
    menuSurface = pygame.display.set_mode((WIDTH,HEIGHT))
    gameOverSurface = pygame.display.set_mode((WIDTH,HEIGHT))
    nextLevelSurface = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Bricks")
    black = pygame.Color(0,0,0)
    showMenu = True
    gameOn = True
    levelsPlaying = False
    gameOverMenu = False
    changeLevel = False
    showCheatKeys = False
    level = 1
    keyDown = None
    fontobj = pygame.font.Font("freesansbold.ttf", 14)
    fontobjTITEL = pygame.font.Font("freesansbold.ttf", 24)
    fontobjCOMBO = pygame.font.Font("freesansbold.ttf",30)
    fontCheatKeys = pygame.font.Font(None,22)
    score = 0
    scoreTemp = 0
    #sprites & achtergrond(en)
    bgMain = pygame.image.load(os.path.join(assets_folder,"bg.png"))
    gameOverBg = pygame.image.load(os.path.join(assets_folder,"gameOver.png"))
    bg1 = pygame.image.load(os.path.join(assets_folder,"bg1.jpg")).convert()
    bg2 = pygame.image.load(os.path.join(assets_folder,"bg2.jpg")).convert()
    nextLevelBg = pygame.image.load(os.path.join(assets_folder,"nextLevelBg.jpg")).convert()
    yBg = 0
    xBg = 0
    # pallet initialiseren
    batSprite = pygame.image.load(os.path.join(assets_folder,"bat.png")).convert()
    batLangSprite = pygame.image.load(os.path.join(assets_folder,"bat_lang.png")).convert()
    upgrade1 = pygame.image.load(os.path.join(assets_folder,"upgrade1.png")).convert()
    upgrade2 = pygame.image.load(os.path.join(assets_folder,"upgrade2.png")).convert()
    heartSprite = pygame.image.load(os.path.join(assets_folder,"heart.png")).convert()
    heartRect = heartSprite.get_rect()# change topleft
    upgradeRectList = []
    playerY = 540
    lives = 3
    bx, by = (int(WIDTH/2), playerY)
    ballSpeed = 5
    sx, sy = (ballSpeed, ballSpeed)
    ballSprite = pygame.image.load(os.path.join(assets_folder,"ball.png"))
    ballServed = False
    changeBall = False
    changeBat = False
    ballBigSprite = pygame.image.load(os.path.join(assets_folder,"ball_normal_big.png"))
    batRect = batSprite.get_rect(topleft=(bx-22,by))
    batLangRect = batLangSprite.get_rect(topleft=(bx-22,by))
    ballRect = ballSprite.get_rect(topleft=(bx+int(batRect[2]/2)-26,by-int(batRect[3])))    
    ballBigRect = ballBigSprite.get_rect(topleft = (bx,by))
    mouseX = int(WIDTH/2)
    # steen initialiseren
    brick = pygame.image.load(os.path.join(assets_folder,"brick.png"))
    brickSpecial = pygame.image.load(os.path.join(assets_folder,"brick_blue_purple.png"))
    brickSpecial2 = pygame.image.load(os.path.join(assets_folder,"brick_yellow_black.png"))
    bricksRects,bricks = createBricks(5*level,2*level) #aatalSpecialeBricks
    # events
    menuSurface.fill(black)
    while gameOn:
        while showMenu:
            welkom = fontobjTITEL.render('SPACE BREAKOUT!', True, (255,255,255),black)
            uitleg = fontobj.render('Gebruik ARROW KEYS of je MUIS',True,(255,255,255),black)
            uitleg2 = fontobj.render('Druk SPATIE of op je muisknop voor de ball te starten!', True, (255,255,255),black)
            start = fontobj.render('Press any key to continue...',True, (255,255,255),black)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
                    showMenu = False
                    levelsPlaying = True
            menuSurface.blit(bgMain,(0,0))
            menuSurface.blit(welkom,(400-int(welkom.get_width()/2),50))
            menuSurface.blit(uitleg,(400-int(uitleg.get_width()/2),150))
            menuSurface.blit(uitleg2,(400-int(uitleg2.get_width()/2),180))
            menuSurface.blit(start,(400-int(start.get_width()/2),300))
            pygame.display.update()
            fpsClock.tick(10)
        mainSurface.fill(black)
        #setup upgrades
        while levelsPlaying:
            #backgrouns scrolling
            if (level%2) == 0:
                relatief_Y = yBg % bg1.get_rect().height
                mainSurface.blit(bg1,(0,relatief_Y - bg1.get_rect().height))
                if relatief_Y < HEIGHT:
                    mainSurface.blit(bg1, (0,relatief_Y))
            if (level%2) == 1:
                relatief_Y = yBg % bg2.get_rect().height
                mainSurface.blit(bg2,(0,relatief_Y - bg2.get_rect().height))
                if relatief_Y < HEIGHT:
                    mainSurface.blit(bg2, (0,relatief_Y))
            yBg += 1
            #levens
            for i in range(lives): #3 levens = 0,1,2
                x,y = ((heartRect[2]*i)+5,5)
                mainSurface.blit(heartSprite,(x,y))
            #onscreen text
            scoreLabel = fontobjTITEL.render(str(score),True,(255,255,255),None)
            scoreComboLabel = fontobjCOMBO.render("combo!  "+ str(scoreTemp),True,(255,255,255),None)
            mainSurface.blit(scoreLabel,(WIDTH-scoreLabel.get_width()-5,5))
            if DEVTOOLS and showCheatKeys:
                cheatKeysLabel1 = fontCheatKeys.render("key 1:__increase combo score",True,(255,255,255),None)
                cheatKeysLabel2 = fontCheatKeys.render("key 2:__________delete steen",True,(255,255,255),None)
                cheatKeysLabel3 = fontCheatKeys.render("key 3:_________volgend level",True,(255,255,255),None)
                cheatKeysLabel4 = fontCheatKeys.render("key 4:___________extra leven",True,(255,255,255),None)
                cheatKeysLabel5 = fontCheatKeys.render("key ENTER:___________Keys Menu",True,(255,255,255),None)
                mainSurface.blit(cheatKeysLabel1,(WIDTH-cheatKeysLabel1.get_width(),HEIGHT-cheatKeysLabel1.get_height()*5))
                mainSurface.blit(cheatKeysLabel2,(WIDTH-cheatKeysLabel2.get_width(),HEIGHT-cheatKeysLabel2.get_height()*4))
                mainSurface.blit(cheatKeysLabel3,(WIDTH-cheatKeysLabel3.get_width(),HEIGHT-cheatKeysLabel2.get_height()*3))
                mainSurface.blit(cheatKeysLabel4,(WIDTH-cheatKeysLabel4.get_width(),HEIGHT-cheatKeysLabel2.get_height()*2))
                mainSurface.blit(cheatKeysLabel5,(WIDTH-cheatKeysLabel5.get_width(),HEIGHT-cheatKeysLabel2.get_height()*1))
            if scoreTemp > 4 and changeBall:
                mainSurface.blit(scoreComboLabel,(400-int(scoreComboLabel.get_width()/2),6))
            if scoreTemp > 2 and not changeBall:
                mainSurface.blit(scoreComboLabel,(400-int(scoreComboLabel.get_width()/2),6))
            #events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if not ballServed:
                        ballServed = True
                elif event.type == pygame.MOUSEMOTION:
                    mouseX = event.pos[0]
                    if(mouseX < 800 -55):
                        if changeBat:
                            batLangRect.topleft = (mouseX-int(batLangRect[2]/2),playerY)
                        elif not changeBat:
                            batRect.topleft = (mouseX-int(batRect[2]/2),playerY)
                    else:
                        if changeBat:
                            batLangRect.topleft = (800-55, playerY)
                        elif not changeBat:
                            batRect.topleft = (800-55, playerY)
                    if not ballServed:
                        if changeBat:
                            bx,by = (mouseX-int(ballRect[2]/2),playerY-batLangRect[3])                    
                            ballRect.topleft = (bx,by)
                        elif not changeBat:
                            bx,by = (mouseX-int(ballRect[2]/2),playerY-batRect[3])                    
                            ballRect.topleft = (bx,by)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        keyDown = "K_LEFT"
                        if changeBat:
                            if not ballServed:
                                bx,by = (batLangRect[0]-int(batLangRect[2]/2)-int(ballRect[2]/2),playerY-batLangRect[3])
                                ballRect.topleft = (bx,by)
                            batLangRect.topleft = (batLangRect[0]-1,playerY)
                        elif not changeBat:
                            if not ballServed:
                                bx,by = (batRect[0]-int(batRect[2]/2)-int(ballRect[2]/2),playerY-batRect[3])
                                ballRect.topleft = (bx,by)
                            batRect.topleft = (batRect[0]-1,playerY)
                    if event.key == pygame.K_RIGHT:
                        keyDown = "K_RIGHT"
                        if changeBat:
                            if not ballServed:
                                bx,by = (batLangRect[0]-int(batLangRect[2]/2)-int(ballRect[2]/2),playerY-batLangRect[3])
                                ballRect.topleft = (bx,by)
                            batLangRect.topleft = (batLangRect[0]+1,playerY)
                        elif not changeBat:
                            if not ballServed:
                                bx,by = (batRect[0]-int(batRect[2]/2)-int(ballRect[2]/2),playerY-batRect[3])
                                ballRect.topleft = (bx,by)
                            batRect.topleft = (batRect[0]+1,playerY)
                    if DEVTOOLS:
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
                            lives += 1
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
                    if changeBat:
                        batLangRect.topleft = (batLangRect[0]-10,playerY)
                        if not ballServed:
                            bx,by = (batLangRect[0]+int(batLangRect[2]/2)-int(ballRect[2]/2),playerY-batLangRect[3])
                            ballRect.topleft = (bx,by)
                    elif not changeBat:
                        batRect.topleft = (batRect[0]-10,playerY)
                        if not ballServed:
                            bx,by = (batRect[0]+int(batRect[2]/2)-int(ballRect[2]/2),playerY-batRect[3])
                            ballRect.topleft = (bx,by)
                if keyDown == "K_RIGHT":
                    if changeBat:
                        batLangRect.topleft = (batLangRect[0]+10,playerY)
                        if not ballServed:
                            bx,by = (batLangRect[0]+int(batLangRect[2]/2)-int(ballRect[2]/2),playerY-batLangRect[3])
                            ballRect.topleft = (bx,by)
                    elif not changeBat:
                        batRect.topleft = (batRect[0]+10,playerY)
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
                        status = "upgrade1"
                    elif b[-1] == 2 and b[-2]==c:
                        status = "upgrade2"
                if status == "":
                    index = bricks.index((c,0))
                    mainSurface.blit(brick,bricks[index][-2])
                elif status == "upgrade1":
                    index = bricks.index((c,1))
                    mainSurface.blit(brickSpecial,bricks[index][-2])
                elif status == "upgrade2":
                    index = bricks.index((c,2))
                    mainSurface.blit(brickSpecial2,bricks[index][-2])
            #teken upgrades
            for u in upgradeRectList:
                #collision detection
                if(u[-1]==1):
                    mainSurface.blit(upgrade1,(u[-2].topleft))
                elif(u[-1]==2):
                    mainSurface.blit(upgrade2,(u[-2].topleft))
                u[-2].topleft = (u[-2][0],u[-2][1]+2) #upgrades naar beneden laten vallen, speed = 2
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
            if(by >= HEIGHT-8):  #bovenkant collide
                by = HEIGHT-8
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
                by = playerY-8
                sy *= -1
                if scoreTemp >= 25:
                    lives += 1
                score += scoreTemp
                scoreTemp = 0
                batRect.topleft = batLangRect.topleft
                changeBat = False
            elif ((ballRect.colliderect(batRect) and not changeBat)or(ballRect.colliderect(batLangRect) and changeBat)):
                by = playerY-16
                sy *= -1
                changeBall = False
                batRect.topleft = batLangRect.topleft
                changeBat = False
                if scoreTemp >= 12:
                    lives += 1
                score += scoreTemp*2
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
                        #upgradeRectList.append( (Rect(16,16,TEMP,TEMP)),(2))
                        upgradeRectList.append(( Rect(upX+8, (upY+int((hb.height/2)+8)),16,16),2))
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
            fpsClock.tick(30) #FPS op juiste snelheid zetten
        mainSurface.fill(black)
        while changeLevel:
            #draw backgroud
            relatief_X = xBg % nextLevelSurface.get_rect().height
            nextLevelSurface.blit(nextLevelBg,(relatief_X - nextLevelSurface.get_rect().width,0))
            if relatief_X < WIDTH:
                nextLevelSurface.blit(nextLevelBg, (relatief_X,0))
            xBg += 1
            #draw labels
            levelLabel1 = fontobjCOMBO.render("Congratulation!",True,(255,255,255),None)
            levelLabel2 = fontobjCOMBO.render("You completed LEVEL "+ str(level) + "!",True,(255,255,255),None)
            nextLevelLabel = fontobjTITEL.render("proceed to next level, press SPACE..",True,(255,255,255),None)
            nextLevelSurface.blit(levelLabel1,(400-int(levelLabel1.get_width()/2),int(HEIGHT/4)))
            nextLevelSurface.blit(levelLabel2,(400-int(levelLabel2.get_width()/2),int(HEIGHT/4)+40))
            nextLevelSurface.blit(nextLevelLabel,(400-int(nextLevelLabel.get_width()/2),int(HEIGHT/2)+50))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        changeLevel = False
                        levelsPlaying = True
                        level += 1
                        del upgradeRectList[:]
                        ballServed = False
                        changeBall = False
                        ballSpeed += 1
                        sx, sy = (ballSpeed, ballSpeed)
                        bx,by = (mouseX-int(ballRect[2]/2),playerY-batRect[3])                    
                        ballRect.topleft = (bx,by)
                        bricksRects,bricks = createBricks(5*level,2*level)
            pygame.display.update()
            fpsClock.tick(30)
            mainSurface.fill(black)
        while gameOverMenu:
            eindScore = fontobjTITEL.render("Eindscore: " + str(score), True, (255,255,255), None)
            opnieuwText = fontobj.render("Druk SPATIE voor opnieuw te spelen", True, (255,255,255),None)
            afsluitText = fontobj.render("Druk ESC voor af te sluiten", True, (255,255,255),None)
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
                        level = 1
                        bricksRects,bricks = createBricks(5*level,2*level)
                    if event.key == pygame.K_ESCAPE:
                        gameOn = False
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
            fpsClock.tick(10)
def createBricks(rands,rands2):
    bricksTemp = []
    randomIndex1 = []
    randomIndex2 = []
    bricksRectsTemp = []
    y_range = 5
    x_range = 10
    for i in range(rands):
        randomIndex1.append((r.randrange(x_range),r.randrange(y_range))) #random (x,y) bvb: ((4,2),(1,1),(4,9),(0,2),(3,7))
    for i in range(rands2):
        randomIndex2.append((r.randrange(x_range),r.randrange(y_range))) #random (x,y) bvb: ((0,2))
    for y in range(y_range): 
        brickY = (y * 24) + 100
        for x in range(x_range):
            brickX = (x*48) + 160
            if (x,y) in randomIndex1:
                bricksTemp.append((Rect(brickX,brickY,48,16),1)) #voor special bricks te tekenen
            elif(x,y) in randomIndex2:
                bricksTemp.append((Rect(brickX,brickY,48,16),2))
            else:
                bricksTemp.append((Rect(brickX,brickY,48,16),0))
            bricksRectsTemp.append(Rect(brickX,brickY,48,16))
    return bricksRectsTemp,bricksTemp
def createRandoms(randoms):
    rands = []
    for i in range(randoms):
        rands.append(r.randrange(1,10))
    return rands
if __name__ == '__main__':  
    main()