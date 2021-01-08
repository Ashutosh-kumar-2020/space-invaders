import math
import random
import os 
import pygame
from pygame import mixer
import time
import sys

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('assets/background.png')
intro = pygame.image.load('assets/intro.jpg').convert_alpha()    

# Sound
mixer.music.load("assets/background.wav")


# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('assets/ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('assets/player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('assets/enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150)) 
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('assets/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score 


if(not os.path.exists("assets/hiscore.txt")):
        with open("assets/hiscore.txt", "w") as f:
            f.write("0") 

with open('assets/hiscore.txt', 'r') as f:
    hiscore_value = f.read() 

score_value = 0 
font = pygame.font.Font('freesansbold.ttf', 32) 

textX = 10
testY = 20

hiscoreX = 200
hiscoreY = 20

high_brokeX = 400
high_brokeY = 20 

startButtonX = 240
startButtonY = 270 

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255)) 
    screen.blit(score, (x, y)) 

def show_hiscore(x, y):
    hiscore = font.render(f"hiscore : {str(hiscore_value)}", True, (237, 28, 178))   
    screen.blit(hiscore, (x, y)) 

def highscore_broke_text(x, y):
    hiscore_broke_text = "You broke the highscore"  
    hiscore_text = font.render(hiscore_broke_text, True, (36, 242, 71))   
    screen.blit(hiscore_text, (x, y)) 

    pygame.display.update() 




def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255)) 
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10)) 


def isCollision(enemyX, enemyY, bulletX, bulletY):
    global score_value
    global hiscore_value 
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2))) 
    if int(score_value) > int(hiscore_value): 
        with open('hiscore.txt', 'w') as f:
            f.write(str(score_value)) 
        highscore_broke_text(high_brokeX, high_brokeY) 

        
        
    if distance < 27:
        return True
    else:
        return False 

    


def StartMenu(x, y):
    menu = True 
    while menu: 
        # screen.fill((237, 28, 178))  
        startmenu_text = "press enter to start." 
        startmenu_text_blit = font.render(startmenu_text, True, (255, 255, 255))  
        screen.blit(startmenu_text_blit,(x, y))  
        screen.blit(intro, (250,50)) 
        pygame.display.update() 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() 
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu = False
                    start() 




def start():
    mixer.music.play(-1)    
    global playerX_change
    global playerX  
    global bulletX
    global bulletY
    global bullet_state 
    global score_value 
    global hiscore_value

    running = True
    while running: 
        # RGB = Red, Green, Blue
        screen.fill((0, 0, 0))
        # Background Image
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

            # if keystroke is pressed check whether its right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    playerX_change = -5
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d: 
                    playerX_change = 5
                if event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
                    if bullet_state is "ready":
                        bulletSound = mixer.Sound("assets/laser.wav") 
                        bulletSound.play()
                        # Get the current x cordinate of the spaceship 
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        # 5 = 5 + -0.1 -> 5 = 5 - 0.1
        # 5 = 5 + 0.1



        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy Movement
        for i in range(num_of_enemies):

            # Game Over
            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[i]

            # Collision
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosionSound = mixer.Sound("assets/explosion.wav") 
                explosionSound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        # Bullet Movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state is "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, testY) 
        show_hiscore(hiscoreX,hiscoreY) 
        pygame.display.update()


if __name__ == "__main__":
    StartMenu(startButtonX, startButtonY) 
