import os
import time
import random
from itertools import compress, product

planes_layouts = {
    'b_747': (1, 1, 0, 1, 1, 1, 1, 0, 1, 1),
    'a_380': (1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1)
}


class Plane(object):

    def __init__(self, seat_rows: int, seat_layout: tuple):
        """
        Plane initialization
        :param seat_rows: number of rows from the airplane
        :param seat_layout: seat columns structure; e.g. (0, 0, 0, 1, 0, 0, 0);  0 - seat, 1 - aisle
        """
        self.seat_rows = seat_rows
        self.seat_layout = seat_layout
        self.passengers = []
        self.layout = [[[] for _ in range(len(self.seat_layout))] for _ in range(self.seat_rows)]
        self.next_layout = [[[] for _ in range(len(self.seat_layout))] for _ in range(self.seat_rows)]

    def update_layout(self):
        """
        Updates the plane current layout with next state
        """
        self.layout = self.next_layout
        self.next_layout = [[[] for _ in range(len(self.seat_layout))] for _ in range(self.seat_rows)]

    def all_seated(self):
        """
        Checks if all passengers are currently seated
        """
        for agent in self.passengers:
            if agent.current_mov != 'sit':
                return False
        return True

    def is_empty(self, row: int, col:int) -> bool:
        """
        Checks if a seat is and/or will be empty
        :param row: seat's row
        :param col: set's column
        :return: seat and will be empty
        """
        return len(self.layout[row][col]) == 0 and len(self.next_layout[row][col]) == 0


class Passenger(object):

    def __init__(self, seat: (int, int), plane: Plane):
        """
        Passenger initialization
        :param seat: seat assigned to passenger; (seat, column)
        :param plane:
        """
        # Static
        self.seat = list(seat)
        self.baggage = random.randint(0, 20)
        self.plane = plane
        # Dynamic
        self.pos = [-1, -1]
        self.current_mov = ''
        self.move_count = -1

    def choose_move(self):
        if self.seat == self.pos:
            self.current_mov = 'sit'
            return

        if self.seat[0] > self.pos[0]:
            self.current_mov = 'up'
            return

        if self.seat[0] == self.pos[0]:
            if self.baggage > 0:
                self.current_mov = 'baggage'
                return
            if self.seat[1] > self.pos[1]:
                self.current_mov = 'right'
                return
            else:
                self.current_mov = 'left'
                return
        print("error! Unknown step")

    def move(self):
        if self.current_mov == '':
            self.choose_move()
        if self.current_mov == 'sit':
            self.sit()
        if self.current_mov == 'up':
            self.move_up()
        if self.current_mov == 'baggage':
            self.set_baggage()
        if self.current_mov == 'right':
            self.move_right()
        if self.current_mov == 'left':
            self.move_left()
        if self.current_mov == 'standLeft':
            self.stand_left()
        if self.current_mov == 'standRight':
            self.stand_right()

    def move_right(self):
        clear = True
        for seat in range(self.pos[1] + 1, self.seat[1]):
            if not self.plane.is_empty(self.pos[0], seat):
                clear = False
                for agent in self.plane.layout[self.pos[0]][seat]:
                    if agent.seat[1] < self.seat[1] and not agent in self.plane.next_layout[self.pos[0]][self.pos[1]]:
                        agent.current_mov = 'standLeft'
        if not clear:
            self.plane.next_layout[self.pos[0]][self.pos[1]].append(self)
            return
        if clear:
            my_turn = True
            for agent in self.plane.layout[self.pos[0]][self.pos[1]]:
                if agent == self:
                    continue

                if agent.seat[1] > self.seat[1] and agent.current_mov == self.current_mov:
                    my_turn = False
            if not my_turn:
                self.plane.next_layout[self.pos[0]][self.pos[1]].append(self)
                return
            self.pos[1] += 1
            self.plane.next_layout[self.pos[0]][self.pos[1]].append(self)
            if self.pos[1] == self.seat[1]:
                self.current_mov = ''

    def move_left(self):
        clear = True
        for seat in range(self.seat[1], self.pos[1]):
            if not self.plane.is_empty(self.pos[0], seat):
                clear = False
                for agent in self.plane.layout[self.pos[0]][seat]:
                    if agent.seat[1] > self.seat[1] and not agent in self.plane.next_layout[self.pos[0]][self.pos[1]]:
                        agent.current_mov = 'standRight'
        if not clear:
            self.plane.next_layout[self.pos[0]][self.pos[1]].append(self)
            return
        if clear:
            my_turn = True
            for agent in self.plane.layout[self.pos[0]][self.pos[1]]:
                if agent == self:
                    continue
                if agent.seat[1] < self.seat[1] and agent.current_mov == self.current_mov:
                    my_turn = False
            if not my_turn:
                self.plane.next_layout[self.pos[0]][self.pos[1]].append(self)
                return
            self.pos[1] -= 1
            self.plane.next_layout[self.pos[0]][self.pos[1]].append(self)
            if self.pos[1] == self.seat[1]:
                self.current_mov = ''

    def move_up(self):
        if self.plane.is_empty(self.pos[0] + 1, self.pos[1]) and len(self.plane.layout[self.pos[0]][self.pos[1]]) == 1:
            self.pos[0] += 1
            self.current_mov = ''
        self.plane.next_layout[self.pos[0]][self.pos[1]].append(self)

    def set_baggage(self):
        self.plane.next_layout[self.pos[0]][self.pos[1]].append(self)
        self.baggage -= 1
        if self.baggage == 0:
            self.current_mov = ''

    def stand_left(self):
        if self.plane.is_empty(self.pos[0], self.pos[1] - 1) or self.plane.seat_layout[self.pos[1] - 1] == 0:
            self.pos[1] -= 1
        if self.plane.seat_layout[self.pos[1]] == 0:
            self.current_mov = 'right'
        self.plane.next_layout[self.pos[0]][self.pos[1]].append(self)

    def stand_right(self):
        if self.plane.is_empty(self.pos[0], self.pos[1] + 1) or self.plane.seat_layout[self.pos[1] + 1] == 0:
            self.pos[1] += 1
        if self.plane.seat_layout[self.pos[1]] == 0:
            self.current_mov = 'left'
        self.plane.next_layout[self.pos[0]][self.pos[1]].append(self)

    def sit(self):
        self.plane.next_layout[self.pos[0]][self.pos[1]].append(self)


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
