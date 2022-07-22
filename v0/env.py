import pygame
from dataclasses import dataclass
import sys
import numpy as np
from gym import spaces
from v0.sprite.dest import DestSprite
from v0.sprite.ground import GroundSprite
from v0.sprite import player
from v0.sprite.player import PlayerSprite
from v0.sprite.ball import BallSprite

@dataclass(init=True, repr=True)
class CoopGame():
    player_speed: int = 5
    tile_size: int = 40
    map_width: int = 20
    map_height: int = 15
    control: bool = False
    frame_rate: int = 60
    render_display: bool = True
    ball_spawn = (0, 260)
    dest_pos = (760, 260)
    slowdown_factor: float = 3.0
    max_steps: int = 60 * 60
    observation_type: str = "rgb"

    metadata = {"render_modes": ["human"], "name": "coop_par"}

    def __init_game_logic(self):
        self.main_ground = pygame.Rect(
            (0, 0), (self.screen_width, self.screen_height))
        self.players = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.balls = pygame.sprite.Group()
        self.dests = pygame.sprite.Group()
        self.player1_grounds = pygame.sprite.Group()
        self.player2_grounds = pygame.sprite.Group()
        self.__init_players()
        self.__init_grounds()
        self.__spawn_ball()
        self.__init_dest()
        
    def __init_pygame(self):
        pygame.init()
        if self.render_display:
            pygame.display.set_caption("CoopGame")
            self.screen = pygame.display.set_mode(
                (self.screen_width, self.screen_height))
        else:
            self.screen = pygame.Surface(
                (self.screen_width, self.screen_height))

    def reset(self, seed=None):
        self.steps = 0
        for player in self.players:
            player.reset()
        for ball in self.balls:
            ball.respawn()
        self.__update_screen()

    def render(self, mode='human'):
        if self.render_display:
            pygame.display.update()
        if self.frame_rate != 0:
            pygame.time.Clock().tick(self.frame_rate)

    def __tick(self):
        self.__handle_events()
        self.players.update()
        self.balls.update()
        self.__ball_update()
        self.__update_screen()
        if self.render_display:
            pygame.display.update()

    def __update_screen(self):
        if self.render_display or self.observation_type == "rgb":
            # all update is done, update the screen
            self.player1_grounds.draw(self.screen)
            self.player2_grounds.draw(self.screen)
            self.players.draw(self.screen)
            self.dests.draw(self.screen)
            self.balls.draw(self.screen)

    def __handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
        if self.control:
            self.__handle_key_press()

    def __handle_key_press(self):
        keys = pygame.key.get_pressed()
        # WASD to control movement of player 1
        if keys[pygame.K_w] != 0:
            self.player1.step(player.ACTION_UP)
        elif keys[pygame.K_d] != 0:
            self.player1.step(player.ACTION_RIGHT)
        elif keys[pygame.K_s] != 0:
            self.player1.step(player.ACTION_DOWN)
        elif keys[pygame.K_a] != 0:
            self.player1.step(player.ACTION_LEFT)
        # ↑↓←→ to control movement of player 2
        if keys[pygame.K_UP] != 0:
            self.player2.step(player.ACTION_UP)
        elif keys[pygame.K_RIGHT] != 0:
            self.player2.step(player.ACTION_RIGHT)
        elif keys[pygame.K_DOWN] != 0:
            self.player2.step(player.ACTION_DOWN)
        elif keys[pygame.K_LEFT] != 0:
            self.player2.step(player.ACTION_LEFT)

    def __handle_action(self, player_name, action):
        p = self.agent_name_mapping[player_name]
        p.step(action)

    def __init_grounds(self):
        ground = GroundSprite(pygame.Color(0, 0, 0),
                              (0, 0, self.screen_width // 2, self.screen_height))
        ground.update_speed(self.player1, 1.0)
        ground.update_speed(self.player2, self.slowdown_factor)
        self.player1_grounds.add(ground)
        self.player2_grounds.add(ground)

        ground = GroundSprite(pygame.Color(128, 128, 128),
                              (self.screen_width // 2, 0, self.screen_width, self.screen_height))
        ground.update_speed(self.player1, self.slowdown_factor)
        ground.update_speed(self.player2, 1.0)
        self.player1_grounds.add(ground)
        self.player2_grounds.add(ground)

    def __init_players(self):
        self.player1 = PlayerSprite(pygame.Color(
            255, 0, 0), (0, self.screen_height // 2), self.tile_size, self.tile_size,
            self.main_ground, self.player1_grounds, self.obstacles, self.player_speed)
        self.players.add(self.player1)
        self.obstacles.add(self.player1)

        self.player2 = PlayerSprite(pygame.Color(
            0, 255, 0), (self.screen_width - self.tile_size, self.screen_height // 2), self.tile_size, self.tile_size,
            self.main_ground, self.player2_grounds, self.obstacles, self.player_speed)
        self.players.add(self.player2)
        self.obstacles.add(self.player2)

    def __spawn_ball(self):
        self.ball = BallSprite(pygame.Color(0, 0, 255),
                               self.ball_spawn,
                               self.tile_size // 2, self.tile_size // 2)
        self.balls.add(self.ball)

    def __init_dest(self):
        self.dest = DestSprite(pygame.Color(128, 0, 255),
                               self.dest_pos,
                               self.tile_size, self.tile_size)
        self.dests.add(self.dest)

    def __ball_update(self):
        for ball in self.balls:
            if ball.carrier:
                score_dest = pygame.sprite.spritecollideany(ball, self.dests)
                if score_dest:
                    for agent in self.rewards:
                        self.rewards[agent] += 1
                    self.ball.respawn()
            else:
                player = pygame.sprite.spritecollideany(ball, self.players)
                if player is not None:
                    ball.carry_by(player)
