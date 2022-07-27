import pygame
from dataclasses import dataclass
import sys
import numpy as np
from gym import spaces
from gym.utils import EzPickle
from pettingzoo import ParallelEnv
from pettingzoo.utils import parallel_to_aec
from v0.sprite.dest import DestSprite
from v0.sprite.ground import GroundSprite
from v0.sprite import player
from v0.sprite.player import PlayerSprite
from v0.sprite.ball import BallSprite


def parallel_env(**kwargs):
    env = raw_env(**kwargs)
    return env

def aec_env(**kwargs):
    return parallel_to_aec(raw_env(**kwargs))

@dataclass(init=True, repr=True)
class CoopGame(ParallelEnv):
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

    def __post_init__(self):
        self.screen_width = self.map_width * self.tile_size
        self.screen_height = self.map_height * self.tile_size
        self.__init_pygame()
        self.__init_game_logic()
        self.__init_petting_zoo()

        self.reset()

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

    def __init_petting_zoo(self):
        self.possible_agents = [self.player1.name, self.player2.name]
        self.agent_name_mapping = {
            self.player1.name: self.player1,
            self.player2.name: self.player2,
        }

        self._action_spaces = {
            agent: spaces.Discrete(player.NUM_ACTIONS)
            for agent in self.possible_agents
        }
        if self.observation_type == "rgb":
            self.observation_shape = (self.screen_width, self.screen_height, 3)
            self.current_frame = np.zeros(
                self.observation_shape, dtype=np.uint8)
            self._observation_spaces = {
                agent: spaces.Box(
                    low=0,
                    high=255,
                    shape=self.observation_shape,
                    dtype=np.uint8
                )
                for agent in self.possible_agents
            }
        else:
            raise NotImplementedError(
                "observation_type %s is not supported" % self.observation_type)

    def observation_space(self, agent):
        return self._observation_spaces[agent]

    def action_space(self, agent):
        return self._action_spaces[agent]

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
        """
        Reset needs to initialize the `agents` attribute and must set up the
        environment so that render(), and step() can be called without issues.

        Here it initializes the `num_moves` variable which counts the number of
        hands that are played.

        Returns the observations for each agent
        """
        self.agents = self.possible_agents[:]
        self.steps = 0
        for player in self.players:
            player.reset()
        for ball in self.balls:
            ball.respawn()
        self.__update_screen()
        observations = {agent: self.observe(agent) for agent in self.agents}
        return observations

    def step(self, actions):
        """
        step(action) takes in an action for the current agent (specified by
        agent_selection) and needs to update
        - rewards
        - _cumulative_rewards (accumulating the rewards)
        - dones
        - infos
        - agent_selection (to the next agent)
        And any internal state used by observe() or render()
        """
        # If a user passes in actions with no agents, then just return empty observations, etc.
        if not actions:
            self.agents = []
            self.__tick()
            return {}, {}, {}, {}
        self.steps += 1
        self.rewards = {agent: 0 for agent in self.agents}
        for agent in actions:
            self.__handle_action(agent, actions[agent])

        self.__tick()

        env_done = self.is_terminal()
        dones = {agent: env_done for agent in self.agents}

        observations = {
            agent: self.observe(agent) for agent in self.agents
        }

        infos = {agent: {} for agent in self.agents}

        if env_done:
            self.agents = []

        return observations, self.rewards, dones, infos

    def render(self, mode='human'):
        if self.render_display:
            pygame.display.update()
        if self.frame_rate != 0:
            pygame.time.Clock().tick(self.frame_rate)

    def observe(self, agent):
        if self.observation_type == "rgb":
            return self.current_frame

    def is_terminal(self):
        return self.steps >= self.max_steps

    def close(self):
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    def __capture_screen(self):
        pygame.pixelcopy.surface_to_array(self.current_frame, self.screen)
        return self.current_frame

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
            if self.observation_type == "rgb":
                self.__capture_screen()

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
        self.player1 = PlayerSprite("red_player", pygame.Color(
            255, 0, 0), (0, self.screen_height // 2), self.tile_size, self.tile_size,
            self.main_ground, self.player1_grounds, self.obstacles, self.player_speed)
        self.players.add(self.player1)
        self.obstacles.add(self.player1)

        self.player2 = PlayerSprite("green_player", pygame.Color(
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
                        self.rewards[agent] += 10
                    if ball.ball_find_carrier(ball, self.player1):  
                        self.rewards[self.player1.name] += 1                
                        self.rewards[self.player2.name] -= 1    
                    if ball.ball_find_carrier(ball, self.player2):  
                        self.rewards[self.player2.name] += 1                
                        self.rewards[self.player1.name] -= 1             
                    self.ball.respawn()
            else:
                player = pygame.sprite.spritecollideany(ball, self.players)
                if player is not None:
                    ball.carry_by(player)

class raw_env(CoopGame, EzPickle):

    def __init__(self, **kwargs):
        EzPickle.__init__(self, **kwargs)
        CoopGame.__init__(self, **kwargs)