from asyncore import loop
import pygame
from pygame import mixer
import random
import math
pygame.init()


# Create Screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("./assets/background.jpg")


# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("./assets/ufo.png")
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load("./assets/space-invaders.png")
player_x = 370
player_y = 480
player_x_change = 0


def player(x, y):
    screen.blit(player_img, (x, y))


# Enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
number_of_enemies = 6
for i in range(number_of_enemies):
    enemy_img.append(pygame.image.load("./assets/alien.png"))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(0.4)
    enemy_y_change.append(40)


def enemy(x, y,i):
    screen.blit(enemy_img[i], (x, y))


# Bullet
bullet_img = pygame.image.load("./assets/bullet.png")
bullet_x = 0
bullet_y = 480
bullet_x_change = 0.1
bullet_y_change = -1
bullet_state = "ready"  # Ready you cant see bullet fire bullet is firing


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x+16, y+10))


def collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((enemy_x-bullet_x)**2 + (enemy_y-bullet_y)**2)
    if distance < 27:
        return True
    return False


# Score
score = 0
font=pygame.font.Font("freesansbold.ttf",32)
text_x=10
text_y=10
def show_score(x,y):
    score_display=font.render("Score: "+str(score),True,(255,255,255))
    screen.blit(score_display,(x,y))

#High_Score
high_score=0
with open("./hight_score.txt") as high_score_file:
    high_score=high_score_file.read()
    high_x=560
    high_y=10
def show_high_score(x,y):
        hiscore_display=font.render("High Score: "+str(high_score),True,(255,255,255))
        screen.blit(hiscore_display,(x,y))

# Game Over Text
over_font=pygame.font.Font("freesansbold.ttf",64)
def game_over_text():
    over_text=over_font.render("Game Over",True,(255,255,255))
    screen.blit(over_text,(200,250))


# Game loop
run = True
while run:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # if keystroke is pressed whether right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -0.3
            if event.key == pygame.K_RIGHT:
                player_x_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound=mixer.Sound("./assets/audio/laser.wav")
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Player Movement
    player_x += player_x_change
    if player_x < 0:
        player_x = 0
    if player_x > 736:
        player_x = 736

    # Enemy Movement
    for i in range(number_of_enemies):
        # Game Over
        if enemy_y[i]>420:
            for j in range(number_of_enemies):
                enemy_y[j]=2000
            game_over_text()
            break
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] < 0:
            enemy_x_change[i] = 0.4
            enemy_y[i] += enemy_y_change[i]
        if enemy_x[i] > 736:
            enemy_x_change[i] = -0.4
            enemy_y[i] += enemy_y_change[i]
         # Collision
        if collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
            collision_sound=mixer.Sound("./assets/audio/explosion.wav")
            collision_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score +=1
            with open("./hight_score.txt",mode="w+") as high_score_file:
                if int(high_score)<score:
                    high_score_file.write(str(score))
                    high_score=score
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)
        enemy(enemy_x[i], enemy_y[i],i)

    # Bullet Movement
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y += bullet_y_change
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    player(player_x, player_y)
    show_score(text_x,text_y)
    show_high_score(high_x,high_y)

    pygame.display.update()