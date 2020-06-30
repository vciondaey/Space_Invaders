import pygame
import random
import math
from pygame import mixer

# Initialise pygame;
pygame.init()

# backgroundsound
mixer.music.load("background.wav")
mixer.music.play(-1)

screen = pygame.display.set_mode((800, 600))

# Title and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon((icon))
# Game loop
playerimg = pygame.image.load("spaceship(1).png")
playerX = 370
playerX_change = 0
playerY = 480

enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6

bulletimg = pygame.image.load("bullet.png")
bulletX = -80
bulletY = 0

backgroung = pygame.image.load("2352.jpg")


explosionimg = pygame.image.load("explosion.png")
explosionX = []
explosionY = []
explosiontime = 10
curexplosiontime = []

for i in range(no_of_enemies):
    enemyimg.append(pygame.image.load("ufo.png"))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(0, 100))
    enemyX_change.append(2)
    enemyY_change.append(25)
    curexplosiontime.append(explosiontime+1)
    explosionX.append(enemyX)
    explosionY.append(enemyY)

def explosion(x, y):
    screen.blit(explosionimg, (x, y))


def bullet(x, y):
    screen.blit(bulletimg, (x, y))


def player():
    screen.blit(playerimg, (playerX, playerY))


def enemy(i):
    screen.blit(enemyimg[i], (enemyX[i], enemyY[i]))


def iscollision(i):
    distance = math.sqrt(math.pow(enemyX[i] - bulletX, 2) + math.pow(enemyY[i] - bulletY, 2))
    if distance < 27:
        return True
    return False
score = 0
shot = False
running = True
font = pygame.font.Font('freesansbold.ttf',30)
over_font = pygame.font.Font('freesansbold.ttf',80)
textX = 10
textY = 10

def show_score():
    dis_score = font.render("Score :" + str(score), True, (255,255,255))
    screen.blit(dis_score,(textX,textY))

def game_over():
    over_text = over_font.render("Game Over",True,(255,0,0))
    screen.blit(over_text,(170,250))

while running:

    # screen.fill((150, 16, 0))
    screen.blit(backgroung, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #     if keyword is pressed checck for r or l
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                # if not shot:
                shot = True
                bullet_sound = mixer.Sound("laser.wav")
                bullet_sound.play()
                bulletX = playerX + 16
                bulletY = playerY
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerX += playerX_change
    if playerX < 0:
        playerX = 1
    if playerX > 737:
        playerX = 736

    for i in range(no_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] > 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]

        # collision occured
        if iscollision(i):
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 0
            shot = False
            score += 1
            print(score)
            # enemyY = random.randint(0,100)
            # enemyX = random.randint(0,800)
            explosionX[i] = enemyX[i]
            explosionY[i] = enemyY[i]
            # enemyX[i] = 7000
            # enemyY[i] = -900
            curexplosiontime[i] = 0
        if curexplosiontime[i] < explosiontime:
            explosion(explosionX[i],explosionY[i])
            curexplosiontime[i] += 1
        if curexplosiontime[i] == explosiontime:
            curexplosiontime[i] += 1
            enemyY[i] = random.randint(0,100)
            enemyX[i] = random.randint(0,800)
        if enemyY[i] >= 420:
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            game_over()
            break
        enemy(i)
    if bulletY < 0:
        shot = False
        bulletY = playerY
    if shot:
        bulletY -= 5
        bullet(bulletX, bulletY)
    player()
    show_score()
    pygame.display.update()
