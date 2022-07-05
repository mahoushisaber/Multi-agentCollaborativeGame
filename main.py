import math
import random
from pygame import mixer
import pygame 

WIDTH = HEIGHT = 800

pygame.init()
# create teh screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Title
pygame.display.set_caption = "Collaborative Game"
icon = pygame.image.load('graphics/Player.png')
# icon = pygame.transform.scale(icon, (50, 100)) 
pygame.display.set_icon(icon)


# Player
playerImage = pygame.image.load('graphics/Player.png')
playerImage = pygame.transform.scale(playerImage, (40, 60)) 
player_up = playerImage

playerX = WIDTH * 0.9
playerY = HEIGHT * 0.45
playerX_change = 0
playerY_change = 0
global grabbable 
grabbable = True
grabSound = mixer.Sound("sounds/grab.wav")
grabSound2 = mixer.Sound("sounds/drop.wav")

def player():
    # blit means draw
    screen.blit(playerImage, (playerX, playerY))


# Enemy
enemyImage = pygame.image.load('graphics/Enemy2.png')
enemyImage = pygame.transform.scale(enemyImage, (40, 60)) 

enemyX = WIDTH * 0.1
enemyY = HEIGHT * 0.45

def enemy():
    # blit means draw
    screen.blit(enemyImage, (enemyX, enemyY))


# Game loop
running = True
while running:
    
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed, check the which action of the 4 movements it is
        speed = 0.2
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -speed
                playerImage = pygame.transform.rotate(player_up, 90)
            if event.key == pygame.K_RIGHT:
                playerX_change = speed
                playerImage = pygame.transform.rotate(player_up, -90)
            if event.key == pygame.K_UP:
                playerY_change = -speed
                playerImage = pygame.transform.rotate(player_up, 0)
            if event.key == pygame.K_DOWN:
                playerY_change = speed
                playerImage = pygame.transform.rotate(player_up, 180)
                
            if event.key == pygame.K_SPACE:
                # grab item
                grabbable = not grabbable
                if grabbable is True:
                    grabSound.play()
                    # set ball's cordinates to the current cordinates of the player 
                    ballX = playerX
                    ballY = playerY
                           
                # drop
                if grabbable is False:
                    grabSound2.play()
                    # set ball's cordinates to the current cordinates of the player 
                    ballX = playerX
                    ballY = playerY
                    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0
            # TODO: check if item is around to pick up, if not, state does not change
            pass

    # player movement with inputs
    playerX += playerX_change
    playerY += playerY_change
    
    # Boundary
    if playerX <= 0:
        playerX = 0
    elif playerX >= WIDTH * 0.95:
        playerX = WIDTH * 0.95 
    if playerY <= 0:
        playerY = 0
    elif playerY >= HEIGHT * 0.92:
        playerY = HEIGHT * 0.92
        
    player()
    enemy()
    pygame.display.update()