import pygame, os, sys
from pygame import *
import random as r
#Globale statische variabelen
WIDTH = 800
HEIGHT = 600
DEVTOOLS = False #verander dit voor Cheatkeys te gebruiken
    # key 1: increase combo score
    # key 2: delete steen
    # key 3: volgend level
    # key 4: extra leven
    # key ENTER: toon cheatKeys
game_folder = os.path.dirname(__file__)
#game_folder = os.path.dirname("__file__") #enkel nodig voor als je een build wilt maken met cx_Freeze "python setup.py build"
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
    level = 1
    keyDown = None
    fontobj = pygame.font.Font("freesansbold.ttf", 14)
    fontobjTITEL = pygame.font.Font("freesansbold.ttf", 24)
    fontobjCOMBO = pygame.font.Font("freesansbold.ttf",30)
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
    heartSprite = pygame.image.load(os.path.join(assets_folder,"heart.png")).convert()
    heartRect = heartSprite.get_rect()# change topleft
    upgrade1RectList = []
    playerY = 540
    lives = 3
    bx, by = (int(WIDTH/2), playerY)
    ballSpeed = 5
    sx, sy = (ballSpeed, ballSpeed)
    ballSprite = pygame.image.load(os.path.join(assets_folder,"ball.png"))
    ballServed = False
    changeBall = False
    ballBigSprite = pygame.image.load(os.path.join(assets_folder,"ball_normal_big.png"))
    batRect = batSprite.get_rect(topleft=(bx-22,by))
    ballRect = ballSprite.get_rect(topleft=(bx+int(batRect[2]/2)-26,by-int(batRect[3])))    
    ballBigRect = ballBigSprite.get_rect(topleft = (bx,by))
    mouseX = int(WIDTH/2)
    # steen initialiseren
    brick = pygame.image.load(os.path.join(assets_folder,"brick.png"))
    brickSpecial = pygame.image.load(os.path.join(assets_folder,"brick_blue_special.png"))
    bricksRects,bricks = createBricks(10*level) #aatalSpecialeBricks
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
                mainSurface.blit(heartSprite,(x,y)
                )
            #onscreen text
            scoreLabel = fontobjTITEL.render(str(score),True,(255,255,255),None)
            scoreComboLabel = fontobjCOMBO.render("combo!  "+ str(scoreTemp),True,(255,255,255),None)
            mainSurface.blit(scoreLabel,(WIDTH-scoreLabel.get_width()-5,5))
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
                        batRect.topleft = (mouseX-int(batRect[2]/2),playerY)
                    else:
                        batRect.topleft = (800-55, playerY)
                    if not ballServed:
                        bx,by = (mouseX-int(ballRect[2]/2),playerY-batRect[3])                    
                        ballRect.topleft = (bx,by)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        keyDown = "K_LEFT"
                        if not ballServed:
                            bx,by = (batRect[0]-int(batRect[2]/2)-int(ballRect[2]/2),playerY-batRect[3])
                            ballRect.topleft = (bx,by)
                        batRect.topleft = (batRect[0]-1,playerY)
                    if event.key == pygame.K_RIGHT:
                        keyDown = "K_RIGHT"
                        if not ballServed:
                            bx,by = (batRect[0]-int(batRect[2]/2)-int(ballRect[2]/2),playerY-batRect[3])
                            ballRect.topleft = (bx,by)
                        batRect.topleft = (batRect[0]+1,playerY)
                    if DEVTOOLS:
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
                    batRect.topleft = (batRect[0]-10,playerY)
                    if not ballServed:
                        bx,by = (batRect[0]+int(batRect[2]/2)-int(ballRect[2]/2),playerY-batRect[3])
                        ballRect.topleft = (bx,by)
                if keyDown == "K_RIGHT":
                    batRect.topleft = (batRect[0]+10,playerY)
                    if not ballServed:
                        bx,by = (batRect[0]+int(batRect[2]/2)-int(ballRect[2]/2),playerY-batRect[3])
                        ballRect.topleft = (bx,by)
            # teken stenen
            for c in bricksRects:
                status = None
                index = None
                for b in bricks:
                    if b[-1] and b[-2]==c:
                        status = True
                    if not b[-1] and b[-2]==c:
                        status = False
                if status:
                    index = bricks.index((c,True))
                    mainSurface.blit(brickSpecial,bricks[index][-2])
                else:
                    index = bricks.index((c,False))
                    mainSurface.blit(brick,bricks[index][-2])
            #teken upgrades
            for u in upgrade1RectList:
                mainSurface.blit(upgrade1,u)
                u.topleft = (u[0],u[1]+2)
                #collision detection
                if(batRect.colliderect(u)):
                    del(upgrade1RectList[upgrade1RectList.index(u)])
                    changeBall = True
                #out of bound detection
                if(u[1] >= HEIGHT-8):
                    del(upgrade1RectList[upgrade1RectList.index(u)])
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
            mainSurface.blit(batSprite, batRect)
            # hoofdlogicad
            # botsingen detecteren
            if not changeBall and (ballRect.colliderect(batRect)):
                by = playerY-8
                sy *= -1
                if scoreTemp >= 50:
                    lives += 1
                score += scoreTemp
                scoreTemp = 0
            elif (ballBigRect.colliderect(batRect)):
                by = playerY-16
                sy *= -1
                changeBall = False
                if scoreTemp >= 25:
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
                    if b[-1] and b[-2]==hb:
                        upX,upY = hb.topleft
                        upgrade1RectList.append(upgrade1.get_rect(topleft=(upX+8,(upY+int((hb.height/2)+8)))))
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
            levelLabel = fontobjCOMBO.render("Congratz!    You beat level "+ str(level),True,(255,255,255),None)
            nextLevelLabel = fontobjTITEL.render("Next level?   press SPACE..",True,(255,255,255),None)
            nextLevelSurface.blit(levelLabel,(400-int(levelLabel.get_width()/2),int(HEIGHT/2)))
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
                        del upgrade1RectList[:]
                        ballServed = False
                        changeBall = False
                        ballSpeed += 1
                        sx, sy = (ballSpeed, ballSpeed)
                        bx,by = (mouseX-int(ballRect[2]/2),playerY-batRect[3])                    
                        ballRect.topleft = (bx,by)
                        bricksRects,bricks = createBricks(10*level)
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
                        del upgrade1RectList[:]
                        ballServed = False
                        changeBall = False
                        level = 1
                        bricksRects,bricks = createBricks(10*level)
                    if event.key == pygame.K_ESCAPE:
                        gameOn = False
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
            fpsClock.tick(10)

def createBricks(rands):
    bricksArray = []
    randomIndex = []
    bricks = []
    y_range = 5
    x_range = 10
    for i in range(rands): #4
            randomIndex.append((r.randrange(x_range),r.randrange(y_range))) #random (x,y) 
    for y in range(y_range): 
        brickY = (y * 24) + 100
        for x in range(x_range):
            brickX = (x*48) + 160
            if (x,y) in randomIndex:
                bricksArray.append((Rect(brickX,brickY,48,16),True)) #voor special bricks te tekenen
            else:
                bricksArray.append((Rect(brickX,brickY,48,16),False))
            bricks.append(Rect(brickX,brickY,48,16))
    return bricks,bricksArray
def createRandoms(randoms):
    rands = []
    for i in range(randoms):
        rands.append(r.randrange(1,10))
    return rands
if __name__ == '__main__':  
    main()