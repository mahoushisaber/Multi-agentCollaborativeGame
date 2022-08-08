import gym
import numpy as np
from gym import spaces
ENV_ACTION_N = 4
ENV_SPACE_LEN = 10
#                      y, x , yeah...I messed up
ENV_INIT_PLAYER_POS = [8, 6]
ENV_INIT_FLAG_POS = [0, 1]
ENV_LEFT_ACTION = 0
ENV_RIGHT_ACTION = 1
ENV_UP_ACTION = 2
ENV_DOWN_ACTION = 3

PLAYER_REPR = "P"
FLAG_REPR = "~"



class CustomEnv(gym.Env):
    """
    _~________ 
    __________
    __________
    __________
    __________
    __________
    __________
    _____ ____
    ____ p ___
    _____ ____
    
    spaces around p are available moves

    """
    
    def __init__(self, row, col):
        super(CustomEnv, self).__init__()
        self.row = row
        self.col = col
         
        self.action_space = spaces.Discrete(
            ENV_ACTION_N)  # one for left 
                            #        right
                            #        up
                            #        down
        # Example for using image as input:
        self.observation_space = spaces.Box(
            low=0, high=row, shape=(2,), dtype=np.uint8)

    def step(self, action):
        done = False
        self._take_action(action)
        reward = 0
        # plus a reward when reached the flag
        if (self.player[0] == self.flag[0] and self.player[1] == self.flag[1]):
            reward += 100
            done = True
        # the smaller the manh-dist, the greater the reward
        reward += -((ENV_SPACE_LEN * ENV_SPACE_LEN)  - 
                    (abs(self.flag[0] - self.player[0]) +
                    abs(self.flag[1] - self.player[1]))
                    ) 
    
        obs = self._next_observation()
        return obs, reward, done, {}

    def reset(self):
        self.player = ENV_INIT_PLAYER_POS
        self.flag = ENV_INIT_FLAG_POS
        
        return self._next_observation()

    def render(self):
        for r in range(self.row):
            print("|",  end = " ")
            for c in range(self.col):
                if r == self.player[0] and c == self.player[1]:
                    print(PLAYER_REPR, end = " ")
                elif r == self.flag[0] and c == self.flag[1]:
                    print(FLAG_REPR, end = " ") 
                else:
                    print("-", end = " ")
            print("|", end="\n")

    def _take_action(self, action):
        if action == ENV_LEFT_ACTION:
            if self.player[1] > 0:
                self.player[1] -= 1
        elif action == ENV_RIGHT_ACTION:
            if self.player[1] < self.col - 1:
                self.player[1] += 1
        elif action == ENV_UP_ACTION:
            if self.player[0] > 0:
                self.player[0] -= 1
        elif action == ENV_DOWN_ACTION:
            if self.player[0] < self.row - 1:
                self.player[0] += 1

    def _next_observation(self):
        # observe the 
        return np.array([self.player, self.flag])
