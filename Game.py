import math
import pygame
import sys
import random
from pygame import mixer

pygame.init()

click = False
# create screen
screen = pygame.display.set_mode((800, 600))

#  Background
backgroundImg = pygame.image.load('background.png')
mixer.music.load('background.wav')
mixer.music.play(-1)

# Top of the window
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('spaceship.png')
playerX = 400
playerY = 480
playerX_change = 0
over_control = 1

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6

# Bullet
# Ready - Can't see bullet on screen
# Fire - Moving on screen
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 5
bullet_state = "ready"

# Score
score_value = 0
title_font = pygame.font.Font('font.TTF', 64)
font = pygame.font.Font('font.TTF', 32)

textX = 10
textY = 10
for i in range(num_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(40)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 30:
        return True


def text(x, y, case):
    if case is "1":  # Game Over
        over_text = title_font.render("Game Over!", True, (255, 255, 255))
        show_score(300, 450)
        screen.blit(over_text, (x, y))

    if case is "2":  # Game Title
        title_text1 = title_font.render("   SPACE", True, (255, 255, 255))
        title_text2 = title_font.render("INVADERS", True, (255, 255, 255))
        screen.blit(title_text1, (x, y))
        screen.blit(title_text2, (x + 78, y + 78))

    if case is "3":  # Resume
        resume_text = font.render("Resume", True, (255, 255, 255))
        screen.blit(resume_text, (x, y))

    if case is "4":  # Quit
        quit_text = font.render("Quit", True, (255, 255, 255))
        screen.blit(quit_text, (x, y))

    if case is "5":  # Play
        play_text = font.render("Play", True, (255, 255, 255))
        screen.blit(play_text, (x, y))


def background():
    screen.blit(backgroundImg, (0, 0))


def pause_menu():
    global click
    while True:
        screen.fill((0, 0, 0))
        # text('main menu', font, (255, 255, 255), screen, 20, 20)
        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect(300, 300, 200, 50)
        button_2 = pygame.Rect(300, 400, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                game()
                pass
        if button_2.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
                pass
        pygame.draw.rect(screen, (100, 100, 255), button_1)
        pygame.draw.rect(screen, (100, 100, 255), button_2)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        text(100, 30, "2")
        show_score(300, 200)
        text(325, 310, "3")
        text(350, 410, "4")
        pygame.display.update()


def main_menu():
    global click
    while True:
        screen.fill((0, 0, 0))
        # text('main menu', font, (255, 255, 255), screen, 20, 20)
        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect(300, 300, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                game()
                pass
        pygame.draw.rect(screen, (100, 100, 255), button_1)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        text(100, 110, "2")
        text(350, 310, "5")
        pygame.display.update()


def game():
    global playerX_change
    global score_value
    global over_control
    global bulletX
    global bulletY
    global bullet_state
    global playerX
    running = True
    while running:
        screen.fill((0, 0, 0))
        background()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_menu()
                    running = False
                if event.key == pygame.K_LEFT:
                    playerX_change = -5
                if event.key == pygame.K_RIGHT:
                    playerX_change = 5
                if event.key == pygame.K_SPACE:
                    if bullet_state is "ready":
                        bullet_sound = mixer.Sound('laser.wav')
                        bullet_sound.play()
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        for i in range(num_enemies):

            # Game Over
            if enemyY[i] > 440:
                for j in range(num_enemies):
                    enemyY[j] = 2000
                screen.fill((0, 0, 0))
                text(100, 150, "2")
                text(150, 350, "1")
                over_control = 0
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 3
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -3
                enemyY[i] += enemyY_change[i]
                # Collision
            collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)
        # if keystroke is pressed check whether its right or left

        # Bullet Movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state is "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change
        if over_control:
            player(playerX, playerY)
            show_score(textX, textY)

        pygame.display.update()


main_menu()