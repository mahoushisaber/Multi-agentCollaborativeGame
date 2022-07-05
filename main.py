import math
import random
from pygame import mixer
import pygame 
import time

WIDTH = HEIGHT = 800
COLOR_WHITE = (255, 255, 255)
speed = 0.2
score = 0
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

playerX = WIDTH * 0.85
playerY = HEIGHT * 0.45
playerX_change = 0
playerY_change = 0
# state for grabbing the ball or not
global grabbable 
grabbable = False
holding = False
pickup_range = 15

grabSound = mixer.Sound("sounds/grab.wav")
grabSound2 = mixer.Sound("sounds/drop.wav")

def player(x, y):
    # blit means draw
    screen.blit(playerImage, (playerX, playerY))


# player2
player2Image = pygame.image.load('graphics/Player2.png')
player2Image = pygame.transform.scale(player2Image, (40, 60)) 

player2X = WIDTH * 0.1
player2Y = HEIGHT * 0.45
player2X_change = 0
player2Y_change = 0

def player2(x, y):
    screen.blit(player2Image, (player2X, player2Y))

# Ball
ballImage = pygame.image.load('graphics/Ball.png').convert_alpha()
ballImage = pygame.transform.scale(ballImage, (40, 45)) 
# ballX = random.randint(30, (WIDTH * 0.9))
# ballY = random.randint(30, (HEIGHT* 0.9))
ballX = 20
ballY = HEIGHT / 2

def ball(x, y):
    screen.blit(ballImage, (ballX, ballY))
    
# Goal
goalImage = pygame.image.load('graphics/Goal.png')
goalImage = pygame.transform.scale(goalImage, (70, 70)) 
goalX = WIDTH - 80
goalY = HEIGHT / 2

def goal(x, y):
    screen.blit(goalImage, (goalX, goalY))
    
    
    
def draw_score():
    pygame.font.init
    font = pygame.font.SysFont(None, 24)
    text = font.render('Score:'+ str(score), True, COLOR_WHITE)
    screen.blit(text, (WIDTH/2, 20))
    
@staticmethod
def get_current_time():
    return int(round(time.time()))

# restting the game 
def reset():
        end_of_game = False
        speed = 0.2
        started_time = get_current_time()
        score = 0
        # TODO: 
        # self.generate_balls()
        # self.generate_players()
        # self.load_map()
        ## debug log for AI traning in future 
        # interval = get_current_time() - self.started_time
        # print("--------------- GAME RESET ---------------")
        # print("Episode ends after:", interval, "(s)")
        # print("Score:", self.score)
        # print("------------------------------------------")
        
        # self.__render()
# Game loop
running = True
while running:
    
    screen.fill((0, 0, 0))
    # draw the area line 
    pygame.draw.line(screen, (255,255,255), ((WIDTH /2), 0), ((WIDTH /2), HEIGHT), 1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed, check the which action of the 4 movements it is
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
                    # set ball's cordinates to the current cordinates of the player 
                    print(ballX, playerX)
                    # range of grabbing the ball: 10 by default 
                    if (playerX - ballX < pickup_range) and (playerY - ballY < pickup_range + 3):
                        grabSound.play()
                        #make ballImage transparent
                        print("Ball Picked")
                        holding = not holding
                        alpha_surf = pygame.Surface(ballImage.get_size(), pygame.SRCALPHA)
                        alpha_surf.fill((255, 255, 255, 0))
                        ballImage.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                # drop
                if grabbable is False:
                    # set ball's cordinates to the current cordinates of the player 
                    if holding is True:
                        grabSound2.play()   
                        ballX = playerX
                        ballY = playerY
                        holding = not holding
                        # alpha_surf = pygame.Surface(ballImage.get_size(), pygame.SRCALPHA)
                        # alpha_surf.fill((255, 255, 255, 255))
                        # ballImage.blit(alpha_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

          
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
    player2X += player2X_change
    player2Y += player2Y_change
  
    
    # Boundary
    if playerX <= 0:
        playerX = 0
    elif playerX >= WIDTH * 0.92:
        playerX = WIDTH * 0.92 
    if playerY <= 0:
        playerY = 0
    elif playerY >= HEIGHT * 0.92:
        playerY = HEIGHT * 0.92
        
    # Boundary check for player2
    if player2X <= 0:
            player2X = 0
    elif player2X >= WIDTH * 0.92:
        player2X = WIDTH * 0.92 
    if player2Y <= 0:
        player2Y = 0
    elif player2Y >= HEIGHT * 0.92:
        player2Y = HEIGHT * 0.92
        
    player(playerX, playerY)
    player2(player2X, player2Y)
    ball(ballX, ballY)
    goal(goalX, goalY)

    draw_score()
    pygame.display.update()