from v0.env import aec_env, parallel_env
from pettingzoo.utils import random_demo
from pettingzoo.test import parallel_api_test, performance_benchmark, test_save_obs

env_kwargs = dict(control=True, render_display=True, frame_rate=60, max_steps=0, observation_type="rgb", player_speed=10, slowdown_factor = 2.0, random_pos = True)
#change
env = aec_env(**env_kwargs)
env.reset()
done = False
while not done:
    env.step(None)
    env.render()
    # print(env.score)
    if not env:
        done = True
# env = parallel_env(**env_kwargs)
# parallel_api_test(env)
# env = aec_env(**env_kwargs)

# performance_benchmark(env)
# env.reset()
# test_save_obs(env)
# random_demo(env)