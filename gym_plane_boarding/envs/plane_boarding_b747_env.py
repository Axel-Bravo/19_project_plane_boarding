import gym
from gym import spaces
from src.utils import *


class PlaneBoardingB747Environment(gym.Env):
    """
    A plan on-boarding simulator environment for OpenAI gym; based on a Lufthansa's Boeing 747-400 (744)
    V1 configuration (393 seats). Adapted to the current unique seat layout configuration.

    This environment has the particularity that it just has an initial action, the sorting of the queue.
    After this has been performed, the full simulation runs and returns the number of steps taken as the
    negative reward. Having 50 seat rows; 393 seats / 8 seats per row = 49,125

    """
    metadata = {'render.modes': ['human']}

    def __init__(self):
        """
        On-boarding OpenAI gym's environment initialization
        """
        super(PlaneBoardingB747Environment, self).__init__()

        self.seat_rows = 50
        self.seat_layout = (1, 1, 0, 1, 1, 1, 1, 0, 1, 1)
        self.num_passengers = self.seat_rows * len(list(compress(self.seat_layout, self.seat_layout)))

        # Reward is negative,; the less time the simulation spends the better
        # As simulation is deterministic, the time spent is attributable to the queue ordering ability
        # The selected number -10000 is just a number with margin, actual simulations take 1500 steps
        self.reward_range = (-10000, 0)

        # The action space is basically an ordering for the passengers queue
        # Having:
        #        (number of passengers order possibilities)  * number of passengers
        # In combination with the state space, it indicates which is the entering order, a passenger should have
        self.action_space = spaces.MultiDiscrete([self.num_passengers for _ in range(self.num_passengers)])

        # State space  is [(row, column, baggage) * num_passengers]
        #  Rows: seat_rows
        #  Columns: (0, len(seat_layout)-1) -> len(seat_layout); although aisles are not "usable"
        #  Baggage: (0, 20) -> 21 values; current implementation
        self.passenger_space = [self.seat_rows, len(self.seat_layout), 21]
        self.observation_space = spaces.MultiDiscrete([self.passenger_space for _ in range(self.num_passengers)])

        # Simulation required attributes
        self.plane = None
        self.queue = None
        self.aisle_columns = None
        self.rounds = 0

    def _next_observation(self) -> list:
        """
        Translates a plane status, i.e. the passengers information, into a format processable by the agent
        :return: Observation space properly formatted
        """
        observation_space = []

        for passenger in self.queue:
            observation_space.append(passenger.seat + [passenger.baggage])

        return observation_space

    def step(self, action: list) -> tuple:
        """
        Given an ordering sequence, arranges the queue in consequence and runs the simulation
        :param action: ordering sequence for the passenger's queue
        :return: result of the simulation
        """
        # Reorder queue, based on algorithm order
        self.queue = [i_queue for _, i_queue in sorted(zip(action, self.queue))]

        # Run simulation
        while True:
            if len(self.queue) == 0 and self.plane.all_seated():
                return None, -self.rounds, True, None  # Corresponding to observation, reward, done, info

            for agent in self.plane.passengers:  # update agents
                agent.move()

            if len(self.queue) > 0:  # Dequeue passengers
                best_aisle = None
                best_dist = -1
                for aisle in self.aisle_columns:  # Select passenger's starting aisle
                    dist = abs(aisle - self.queue[0].seat[1])
                    if best_dist == -1 or dist < best_dist:
                        best_dist = dist
                        best_aisle = aisle
                if self.plane.is_empty(0, best_aisle):
                    entering_passenger = self.queue.pop(0)
                    entering_passenger.pos = [0, best_aisle]
                    self.plane.next_layout[0][best_aisle].append(entering_passenger)
                    self.plane.passengers.append(entering_passenger)

            self.plane.update_layout()
            self.rounds += 1

    def reset(self) -> list:
        """
        Resets the environment by initializing the simulation required parameters
        :return:
        """
        self.plane = Plane(seat_rows=self.seat_rows, seat_layout=self.seat_layout)
        self.queue = generate_queue(plane=self.plane)
        random.shuffle(self.queue)
        self.aisle_columns = [i_col if col == 0 else 0 for i_col, col in enumerate(self.plane.seat_layout)]
        self.aisle_columns = list(compress(self.aisle_columns, self.aisle_columns))
        self.rounds = 0

        return self._next_observation()

    def render(self, mode='human'):
        """
        No rendering mode available, as the simulation runds
        :param mode:
        :return:
        """
        pass
