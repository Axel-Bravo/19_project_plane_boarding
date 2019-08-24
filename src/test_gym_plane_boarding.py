#%% Imports and function declarations
# pip install -e 19_project_onboarding/
import gym
import random

#%% Testing Development Zone
# Initialize environment
env = gym.make('gym_plane_boarding:b737-v0')  # Available: "b737-v0", "b747-v0", "a380-v0"
env.reset()

# Generate random initial action
random_plane_queue_order = [i for i in range(1, env.observation_space.shape[0] + 1)]
random.shuffle(random_plane_queue_order)

# Execute simulation
for _ in range(1):
    observation, reward, done, info = env.step(action=random_plane_queue_order)
    print(observation, reward, done, info)

    if done:
        print("Finished after {} time steps".format(-reward))
        break

print('End of one game!')
