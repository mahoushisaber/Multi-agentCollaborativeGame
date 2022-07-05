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

playerX = WIDTH * 0.9
playerY = HEIGHT * 0.45

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
    
    player()
    enemy()
    pygame.display.update()