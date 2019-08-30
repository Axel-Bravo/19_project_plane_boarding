#%% Imports and function declarations
# pip install -e 19_project_onboarding/
import gym
import random
from src.utils import ReplayBuffer


#%% Environment Initialization
env = gym.make('gym_plane_boarding:b737-v0')
buffer = ReplayBuffer()

# Initial experiences on ReplayBuffer
for _ in range(2500):
    env.reset()
    passengers_queue = env.queue

    # Generate random action
    random_plane_queue_order = [i for i in range(1, env.observation_space.shape[0] + 1)]
    random.shuffle(random_plane_queue_order)

    observation, reward, done, info = env.step(action=random_plane_queue_order)
    buffer.add(state=passengers_queue, action=random_plane_queue_order, reward=reward)

# Agent learning
    # TODO: implement initial DRL agent algorithm

