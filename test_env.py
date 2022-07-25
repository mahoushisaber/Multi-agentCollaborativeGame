from v0.env import aec_env, parallel_env
from pettingzoo.utils import random_demo
from pettingzoo.test import parallel_api_test, performance_benchmark, test_save_obs

env_kwargs = dict(control=True, render_display=True, frame_rate=0, max_steps=60 * 10, observation_type="rgb", player_speed=10)
env = parallel_env(**env_kwargs)
parallel_api_test(env)
env = aec_env(**env_kwargs)
performance_benchmark(env)
env.reset()
test_save_obs(env)
random_demo(env)