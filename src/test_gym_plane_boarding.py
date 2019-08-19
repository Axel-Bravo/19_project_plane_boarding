#%% Imports and function declarations
from gym_plane_boarding.envs.plane_boarding_env import *

#%% Testing Development Zone
seat_rows = 32
plane_layout = planes_layouts['b_737']
num_passengers = seat_rows * len(list(compress(plane_layout, plane_layout)))

# Initialize environment
env = PlaneBoardingEnvironment(seat_rows=seat_rows, seat_layout=plane_layout)
env.reset()

# Generate random initial action
random_plane_queue_order = [i for i in range(1, num_passengers + 1)]
random.shuffle(random_plane_queue_order)

# Execute simulation
for _ in range(1):
    observation, reward, done, info = env.step(action=random_plane_queue_order)
    print(observation, reward, done, info)

    if done:
        print("Finished after {} time steps".format(-reward))
        break

print('End of one game!')