#%% Imports and function declarations
# pip install -e gym_plane_boarding/
import gym
import random
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from src.utils import ReplayBuffer, QAproximator

from tensorflow.nn import log_softmax
from tensorflow import convert_to_tensor, cast, float32

# DRL Agent parameters
min_num_experiences = 1000
num_experiences = int(3e4)

learn_every = 100
learn_consecutively = 5


#%% DQN Execution
env = gym.make('gym_plane_boarding:b737-v0')
buffer = ReplayBuffer()

rewards = []
rewards_mean = deque(maxlen=100)

q_network = QAproximator()
q_target = QAproximator()
q_target.copy_weights(network_to_copy=q_target)

for i_exp in range(num_experiences):
    env.reset()
    passengers_queue = env.queue

    # Select Action
    if i_exp < min_num_experiences:
        # Generate random action
        plane_queue_order = [i for i in range(1, env.observation_space.shape[0] + 1)]
        plane_queue_order = np.array(log_softmax(cast(convert_to_tensor(plane_queue_order), float32)))
        random.shuffle(plane_queue_order)
    else:
        pass
        # TODO: to implement the E-greedy algorithm or plain greedy

    observation, reward, done, info = env.step(action=plane_queue_order)  # Run simulation
    buffer.add(state=passengers_queue, action=plane_queue_order, reward=reward)  # Save experience

    rewards.append(reward)  # Save reward
    rewards_mean.append(reward)  # Save reward mean

    if i_exp < min_num_experiences:  # Agent average performance information
        print("Agent average performance is: {}".format(round(np.array(rewards_mean).mean(), 2)))

    if (i_exp < min_num_experiences) and (i_exp % learn_every == 0):  # Update Q-target Network
        pass
        # TODO: implementation of the Q-network learning and update procedures

plt.plot(rewards)
