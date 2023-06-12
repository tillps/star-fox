import pygame
import os
import random
import math
from pygame import mixer

mixer.init()
pygame.init()
clock = pygame.time.Clock()

mixer.music.load(os.path.join('assets', 'bgm.mp3'))
mixer.music.play(-1)

WIDTH, HEIGHT, = 850,950
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Star Fox Campaign')
icon = pygame.image.load(os.path.join('assets', 'startup.png'))
pygame.display.set_icon(icon)


ship_wid, ship_height = 100, 85


#props
background = pygame.image.load(os.path.join('assets', 'background.png'))
playerimg = pygame.image.load(os.path.join('assets', 'star fox.png'))
playerot = pygame.transform.rotate(pygame.transform.scale(playerimg, (ship_wid, ship_height)), 270)
enemyimg = pygame.image.load(os.path.join('assets', 'enemy.png'))

laserpng = pygame.image.load(os.path.join('assets', 'laser.png'))
laserrot = pygame.transform.rotate(pygame.transform.scale(laserpng, (ship_wid, ship_height)), 90)
check = False

enemyimg = []
eposX = []
eposY = []
enemyvelX = []

no_of_npcs = 6

for i in range(no_of_npcs):
    
    enemyimg.append(pygame.image.load(os.path.join('assets', 'enemy.png')))
    eposX.append(random.randint(0, 850))
    eposY.append(random.randint(30, HEIGHT/2 - 70))
    enemyvelX.append(-5)

score = 0



pos_x = WIDTH/2 - 50
pos_y = HEIGHT - 150
velX = 0
velY = 0

laserX = pos_x + 8
laserY = pos_y - 80

def player():
    screen.blit(playerot,(pos_x, pos_y))


running = True


font = pygame.font.SysFont('Comic Sans', 32, 'bold')

def score_text():
    img = font.render(f'Score:{score}', True, 'white')
    screen.blit(img, (10,10))

font_gameover = pygame.font.SysFont('Comic Sans', 64, 'bold')


def gameover():
    img_gameover = font_gameover.render('GAME OVER', True, 'white')
    img = font.render(f'Score: {score}', True, 'white')
    screen.blit(img,(WIDTH/2 - 200,HEIGHT/2 - 200) )
    screen.blit(img_gameover, (WIDTH/2 - 200,HEIGHT/2 - 100))
    
while running:
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a: #left
                velX -= 15
            if event.key == pygame.K_d: #right
                velX += 15
            if event.key == pygame.K_SPACE:
                if check == False:
                    laser_sound = mixer.Sound(os.path.join('assets', 'lasershoot.mp3')) 
                    laser_sound.play()

                    check = True
                    laserX = pos_x + 8 
            
        if event.type == pygame.KEYUP:
            velX = 0
    pos_x += velX
    if pos_x <= 0:
        pos_x = 0
    elif pos_x >= WIDTH - ship_wid + 15:
        pos_x = WIDTH - ship_wid + 15
        
        
    for i in range(no_of_npcs):
        if eposY[i] >= pos_y - 130:
            for j in range(no_of_npcs):
                eposY[j] = 100000
            gameover()
            break
        
        eposX[i]+= enemyvelX[i]
        if eposX[i] <= 0:
            enemyvelX[i] = random.randint(5, 20)
            eposY[i] += 20
        if eposX[i] >= 810:
            enemyvelX[i] =- random.randint(5, 20)
            eposY[i] += 20
        
        distance = math.sqrt(math.pow(laserX-eposX[i],2) + math.pow(laserY-eposY[i],2))
        if distance < 50:
            killsound = mixer.Sound(os.path.join('assets', 'hit.mp3')) 
            killsound.play()

            laserY = pos_y - 80
            check = False
            eposX[i] = random.randint(0, 850)
            eposY[i] = random.randint(10, HEIGHT/2)
            score += 1
        screen.blit(enemyimg[i], (eposX[i], eposY[i]))
    
            
            
    if laserY <= 0:
        laserY = pos_y - 80
        check = False
    if check is True:
        screen.blit(laserrot, ((laserX, laserY)))
        laserY -= 50
    
    

    
    player()
    score_text()
    clock.tick(60)
    pygame.display.update()