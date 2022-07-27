import argparse
from v0.env import parallel_env, aec_env
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
import gym
import supersuit as ss
import numpy as np
from matplotlib import pyplot as plt
from pprint import pprint



def load_env(train=True) -> gym.Env:
    env_kwargs = dict(control=False, render_display=True, frame_rate=0,
    player_speed=20, slowdown_factor=1.0,
    max_steps=60 * 60, observation_type="rgb")
    if train is True:
        env = parallel_env(**env_kwargs)
    else:
        env = aec_env(**env_kwargs)
    # env = ss.color_reduction_v0(env, mode="B")
    env = ss.resize_v0(env, x_size=60, y_size=80)
    env = ss.frame_stack_v1(env, 4)
    if train is True:
        env = ss.pettingzoo_env_to_vec_env_v1(env)
        env = ss.concat_vec_envs_v1(
            env, num_vec_envs=8, num_cpus=0, base_class='stable_baselines3')
    return env


def linear_schedule(initial_value: float):
    def func(progress_remaining: float) -> float:
        return progress_remaining * initial_value

    return func


def show_image(img):
    plt.imshow(img, interpolation="nearest")
    plt.show()

def train(model_name, save_freq=100000):
    env = load_env(train=True)
    model = PPO("CnnPolicy", env, n_steps=128, n_epochs=4, batch_size=256,
                clip_range=linear_schedule(0.1), learning_rate=linear_schedule(2.5e-4),
                # clip_range=0.1, learning_rate=2.5e-4,
                vf_coef=0.5, ent_coef=0.01, verbose=3, tensorboard_log="models/v0/ppo")
    model.learn(total_timesteps=20_000,
                callback=CheckpointCallback(
                    save_freq=max(save_freq // env.num_envs, 1),
                    save_path="models/v0/ppo",
                    verbose=1,
                ))
    model.save(model_name)


def enjoy(model_name):
    env = load_env(train=False)
    model = PPO.load(model_name)
    env.reset()
    for agent in env.agent_iter():
        obs, reward, done, info = env.last()
        # show_image(obs[:, :, 0:3])
        act = model.predict(obs, deterministic=False)[0] if not done else None
        env.step(act)
        env.render()


parser = argparse.ArgumentParser()
parser.add_argument("action", choices=["train", "enjoy"])
# TODO add path arg as well
parser.add_argument("-i", dest="model_name", type=str, default="models/v0/ppo/rl_model_final")
args = parser.parse_args()

if args.action == "train":
    train(args.model_name)
else:
    enjoy(args.model_name)