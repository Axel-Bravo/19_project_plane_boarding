#%% Imports and functions declarations
from itertools import compress, product
from src.utils import *


def generate_queue(plane: Plane) -> list:
    """
    Generates a queue of passengers
    :param plane: a plane in order to know seats availability
    :return: passenger's queue
    """
    queue = []
    seat_columns = compress(range(len(plane.seat_layout)), plane.seat_layout)
    seats = product(seat_columns, list(range(plane.seat_rows)))

    for seat in seats:
        queue.append(Passenger(seat=seat, plane=plane))

    return queue


def simulation(rows: int, layout: tuple):
    """
    Simulates the on-boarding process of an airplane
    :param rows: number of rows from the airplane
    :param layout: columns layout of the airplane
    :return: number of rounds taken to seat all passengers
    """
    plane = Plane(seat_rows=rows, seat_layout=layout)
    queue = generate_queue(plane=plane)
    queue = random.shuffle(queue)
    aisle_columns = [0 if column == 1 else 1 for column in plane.seat_layout]
    rounds = 0

    while True:
        if len(queue) == 0 and plane.all_seated():
            return rounds

        for passenger in plane.passengers:  # update agents
            passenger.move()

        if len(queue) > 0:  # Move from queue
            best_aisle = None
            best_dist = -1
            for aisle in aisle_columns:  # Select starting aisle
                dist = abs(aisle - queue[0].seat[1])
                if best_dist == -1 or dist < best_dist:
                    best_dist = dist
                    best_aisle = aisle
            if plane.is_empty(0, best_aisle):
                next_passenger = queue.pop(0)
                next_passenger.pos = [0, best_aisle]
                plane.next_layout[0][best_aisle].append(next_passenger)
                plane.passengers.append(next_passenger)

        plane.update_layout()
        rounds += 1

        return rounds


g_737 = (1, 1, 1, 0, 1, 1, 1)
g_747 = (1, 1, 0, 1, 1, 1, 1, 0, 1, 1)
g_a380 = (1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1)


if __name__ == "__main__":
    g_737 = (1, 1, 1, 0, 1, 1, 1)
    g_747 = (1, 1, 0, 1, 1, 1, 1, 0, 1, 1)
    g_a380 = (1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1)

    num_simulations = 10
    num_rows = 32
    plane_layout = g_747
    randomAvg = 0

    for _ in range(num_simulations):
        randomAvg += simulation(rows=num_rows, layout=plane_layout)

    randomAvg /= num_simulations

    print(randomAvg)
