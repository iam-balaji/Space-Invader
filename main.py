import pygame
import random
import math
from pygame import mixer
# initialise pygame
pygame.init()

# Creates the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('SpaceInvader/background.png')

# Background Music
mixer.music.load('SpaceInvader/background.wav')
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('SpaceInvader/ufo.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('SpaceInvader/spaceship.png')
playerX = 360
PlayerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6

for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load('SpaceInvader/enemy.png'))
    enemyX .append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)


# Bullet
bulletImg = pygame.image.load('SpaceInvader/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = 'ready'

# score
score = 0   
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY=10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf',64)

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y,i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x, y))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX, 2) +
                         math.pow(enemyY-bulletY, 2))
    if distance < 28:
        return True
    else:
        return False

def show_Score(x,y):
    scoreValue = font.render('Score :'+ str(score) , True ,(255,255,255))
    screen.blit(scoreValue,(x,y))

def gameover():
    over_text = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,250))

# Gaming window running loop
running = True
while running:

    # Background Change
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Checking for keystroke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = - 5

            if event.key == pygame.K_RIGHT:
                playerX_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('SpaceInvader/laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

# Updating the new x-axis and checking for boundary
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

# Enemy Movement
    for i in range(no_of_enemies):
        if  enemyY[i] > 440:
            for j in range(no_of_enemies):
                enemyY[j] = 2000
                gameover()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
            
# Collision Detection
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('SpaceInvader/explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            score += 1
        enemy(enemyX[i], enemyY[i] , i)
# For Refiring the bullet
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"


# Bullet Movement
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    

    player(playerX, PlayerY)
    show_Score(textX,textY)
    pygame.display.update()
