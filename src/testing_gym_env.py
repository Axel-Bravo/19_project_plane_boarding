#%% Imports and function declarations
from src.gym_env import *

#%% Testing Development Zone

# Initialize environment
env = OnBoardingEnvironment(seat_rows=seat_rows, seat_layout=seat_layout)
env.reset()

# Generate random initial action
random_plane_queue_order = [i for i in range(1, num_passengers + 1)]
random.shuffle(random_plane_queue_order)

# Execute simulation
for _ in range(1):
    observation, reward, done, info = env.step(action=random_plane_queue_order)
    print(observation, reward, done, info)

    if done:
        print("Finished after {} timesteps".format(t + 1))
        break

print('End of one game!')