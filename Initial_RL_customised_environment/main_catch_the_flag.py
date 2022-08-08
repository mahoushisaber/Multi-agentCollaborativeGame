import gym
import env_catch_the_flag

r = 10
c = 10
env = env_catch_the_flag.CustomEnv(r, c)
for i_episode in range(1):
    observation = env.reset()
    for t in range(1000):
        env.render()
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        print(action, observation)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
env.close()