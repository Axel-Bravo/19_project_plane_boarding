import os
import time
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
    seats = product(list(range(plane.seat_rows)), seat_columns)

    for seat in seats:
        queue.append(Passenger(seat=seat, plane=plane))

    return queue


def print_simulation(plane: Plane, queue: list, aisle_columns: list, num_simulations: int):
    """
    Print the simulation by the  python's terminal console
    :param plane: plane used in the simulation
    :param queue: queue of passengers of the on-boarding process
    :param aisle_columns: aisle'columns plane layout
    :param num_simulations: number of simulations to execute
    """
    os.system('clear')
    for _ in range(len(plane.seat_layout) + 1):  # Print separator
        print("", end='')

    for _ in range(len(queue)):  # Print remaining queue
        print('<', end='')
    print('\n')

    for i in range(plane.seat_rows):  # Print current plane layout status
        for j in range(len(plane.seat_layout)):
            if len(plane.layout[i][j]) != 0:
                if len(plane.layout[i][j]) > 1:
                    print(len(plane.layout[i][j]), end='')
                elif plane.layout[i][j][0].current_mov == 'standRight' or plane.layout[i][j][
                    0].current_mov == 'right':
                    print('>', end='')
                elif plane.layout[i][j][0].current_mov == 'standLeft' or plane.layout[i][j][0].current_mov == 'left':
                    print('<', end='')
                elif plane.layout[i][j][0].current_mov == 'up':
                    print('V', end='')
                elif plane.layout[i][j][0].current_mov == 'baggage':
                    print('B', end='')
                elif plane.layout[i][j][0].current_mov == 'sit':
                    print('S', end='')
                else:
                    print('?', end='')
            elif j in aisle_columns:
                print('|', end='')
            else:
                print('_', end='')
        print('')

    print('\nCurrent round: {}'.format(num_simulations))
    time.sleep(0.04)


def simulation(rows: int, layout: tuple, num_simulations: int, show_simulation: bool = False) -> float:
    """
    Simulates the on-boarding process of an airplane
    :param rows: number of rows from the airplane
    :param layout: columns layout of the airplane
    :param num_simulations: number of launched simulations
    :param show_simulation: parameter to decide if we want to see the on-boarding simulation
    :return: number of rounds taken to seat all passengers
    """
    plane = Plane(seat_rows=rows, seat_layout=layout)
    queue = generate_queue(plane=plane)
    random.shuffle(queue)
    aisle_columns = [i_col if col == 0 else 0 for i_col, col in enumerate(plane.seat_layout)]
    aisle_columns = list(compress(aisle_columns, aisle_columns))
    rounds = 0

    while True:
        if len(queue) == 0 and plane.all_seated():
            return rounds

        for agent in plane.passengers:  # update agents
            agent.move()

        if len(queue) > 0:  # Dequeue passengers
            best_aisle = None
            best_dist = -1
            for aisle in aisle_columns:  # Select passenger's starting aisle
                dist = abs(aisle - queue[0].seat[1])
                if best_dist == -1 or dist < best_dist:
                    best_dist = dist
                    best_aisle = aisle
            if plane.is_empty(0, best_aisle):
                entering_passenger = queue.pop(0)
                entering_passenger.pos = [0, best_aisle]
                plane.next_layout[0][best_aisle].append(entering_passenger)
                plane.passengers.append(entering_passenger)

        plane.update_layout()
        if show_simulation:
            print_simulation(plane=plane, queue=queue, aisle_columns=aisle_columns, num_simulations=num_simulations)
        rounds += 1


def main():
    num_simulations = 250
    num_rows = 32
    random_avg = 0

    for i_sim in range(num_simulations):
        random_avg += simulation(rows=num_rows, layout=planes_layouts['b_737'], num_simulations=i_sim,
                                 show_simulation=False)
    random_avg = random_avg / float(num_simulations)

    print("Random Average: {}".format(random_avg))


if __name__ == "__main__":
    main()
