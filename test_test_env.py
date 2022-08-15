import unittest
import pygame

# from v0 import Env
from pettingzoo import ParallelEnv
from pettingzoo.utils import parallel_to_aec
from v0.sprite.dest import DestSprite
from v0.sprite.ground import GroundSprite
from v0.sprite import player
from v0.sprite.player import PlayerSprite
from v0.sprite.ball import BallSprite
from v0.sprite.score import ScoreSprite
class TestMain(unittest.TestCase):
    # Test the function env.py
    def test_GroundSprite(self):
        ground = GroundSprite(pygame.Color(0, 0, 0),
                             (0, 0, 20, 20))
        self.assertEqual(ground.rect, (0, 0, 20, 20))  
    
    def test_UpdateSpeed(self):
        ground = GroundSprite(pygame.Color(0, 0, 0),
                             (0, 0, 20, 20))
        
        obs = pygame.sprite.Group()
        player = PlayerSprite("1",pygame.Color(0, 0, 0), (0, 0), 10, 10, ground, obs, 6)
        players = pygame.sprite.Group()
        
        ground.update(player.speed)
        players.add(player)
        self.assertEqual(ground.speed_map.__contains__(10), False)  

    def test_PlayerSprite(self):
        obs = pygame.sprite.Group()
        ground = GroundSprite(pygame.Color(0, 0, 0),
                             (0, 0, 20, 20))
        player = PlayerSprite("1",pygame.Color(0, 0, 0), (0, 0), 0, 0, ground, obs, 5)
        player2 = PlayerSprite("2",pygame.Color(255, 255, 255), (200, 200), 0, 0, ground, obs, 5)
        players = pygame.sprite.Group()
        players.add(player)
        players.add(player2)
        self.assertEqual(len(players), 2)
        self.assertEqual(player.rect, (0, 0, 0, 0))  
        
    def test_DestSprite(self):
        # color, pos, width, height
        dest = DestSprite(pygame.Color(0, 0, 0),
                                (0, 0), 20, 20)
        self.assertEqual(dest.rect, (0, 0, 20, 20))  
    
    def test_BallSprite(self):
        obs = pygame.sprite.Group()
        # color, pos, width, height
        ball = BallSprite(pygame.Color(0, 0, 0),
                                (0, 0), 20, 20) 
        self.assertEqual(ball.rect, (0, 0, 20, 20))  
        
    def test_BallCarriedBy(self):
        obs = pygame.sprite.Group()
        ground = GroundSprite(pygame.Color(0, 0, 0),
                             (0, 0, 20, 20))
        ball = BallSprite(pygame.Color(0, 0, 0),
                                (0, 0), 20, 20) 
        player = PlayerSprite("1",pygame.Color(0, 0, 0), (0, 0), 0, 0, ground, obs, 5)
        player2 = PlayerSprite("2",pygame.Color(0, 0, 0), (0, 0), 0, 0, ground, obs, 10)
        # First carried by player 2, then 1
        ball.carry_by(player2)
        self.assertEqual(ball.carrier, player2)  
        ball.carry_by(player)
        self.assertEqual(ball.carrier, player)
    
    def test_ScoreSprite(self):
        pygame.font.init()
        obs = pygame.sprite.Group()
        # pos
        score = ScoreSprite((0, 0))
        obs.add(score)
        self.assertEqual(score.value, 0)  
    
    def test_ScoreUpdate(self):
        pygame.font.init()
        # update score to 2
        score = ScoreSprite((0, 0))
        score.value = 2
        score.update()
        self.assertEqual(score.value, 2)  
        
    # expected move to certain positions...
    def test_PlayerAction(self):
        obs = pygame.sprite.Group()
        ground = GroundSprite(pygame.Color(0, 0, 0),
                             (0, 0, 20, 20))
        player = PlayerSprite("1", pygame.Color(0, 0, 0), (0, 0), 1, 0, ground, obs, 5)
        rect = player.image.get_rect()
        player.step(0)
        players = pygame.sprite.Group()
        players.add(player)
        self.assertEqual(rect, (0, 0, 1, 0))
    
    def test_PlayerCollision(self):
        obs = pygame.sprite.Group()
        ground = GroundSprite(pygame.Color(0, 0, 0),
                             (0, 0, 20, 20))
        player = PlayerSprite("1", pygame.Color(0, 0, 0), (0, 0), 3, 1, ground, obs, 10)
        player2 = PlayerSprite("2", pygame.Color(0, 0, 0), (2, 2), 3, 1, ground, obs, 10)
        player3 = PlayerSprite("3", pygame.Color(0, 0, 0), (0, 0), 3, 1, ground, obs, 10)
    
        collision_with_player2 = player.obstacle_collide(player, player2)
        collision_with_player3 = player.obstacle_collide(player, player3)
        # Only player 3 is at the same location. Collision should occur
        self.assertEqual(collision_with_player2, False)
        self.assertEqual(collision_with_player3, True)


if __name__ == '__main__':
    unittest.main()