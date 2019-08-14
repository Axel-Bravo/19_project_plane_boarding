import random


class Passenger(object):

    def __init__(self, seat: (int, int), plane):
        """
        Passenger initialization
        :param seat: seat assigned to passenger; (seat, aisle)
        :param plane:
        """
        # Static
        self.seat = seat
        self.baggage = random.randint(0, 20)
        self.plane = plane

        # Dynamic
        self.pos = [-1, -1]
        self.move = ''
        self.move_count = -1

    def choose_move(self):
        if self.seat == self.pos:
            self.move = 'sit'
            return

        if self.seat[0] > self.pos[0]:
            self.move = 'up'
            return

        if self.seat[0] == self.pos[0]:
            if self.baggage > 0:
                self.move = 'baggage'
                return
            if self.seat[1] > self.pos[1]:
                self.move = 'right'
                return
            else:
                self.move = 'left'
                return
        print("error! Unknows step")

    def move(self):
        if self.move == '':
            self.choose_move()
        if self.move == 'sit':
            self.sit()
        if self.move == 'up':
            self.moveUp()
        if self.move == 'baggage':
            self.setBaggage()
        if self.move == 'right':
            self.moveRight()
        if self.move == 'left':
            self.moveLeft()
        if self.move == 'standLeft':
            self.standLeft()
        if self.move == 'standRight':
            self.standRight()

    def moveRight(self):
        clear = True
        for seat in range(self.pos[1] + 1, self.seat[1]):
            if not self.plane.is_empty(self.pos[0], seat):
                clear = False
                for agent in self.plane.squares[self.pos[0]][seat]:
                    if agent.seat[1] < self.seat[1] and not agent in self.plane.nextSquares[self.pos[0]][self.pos[1]]:
                        agent.curMove = 'standLeft'
        if not clear:
            self.plane.nextSquares[self.pos[0]][self.pos[1]].append(self)
            return
        if clear:
            myTurn = True
            for agent in self.plane.squares[self.pos[0]][self.pos[1]]:
                if agent == self:
                    continue
                if agent.seat[1] > self.seat[1] and agent.curMove == self.move:
                    myTurn = False
            if not myTurn:
                self.plane.nextSquares[self.pos[0]][self.pos[1]].append(self)
                return
            self.pos[1] += 1
            self.plane.nextSquares[self.pos[0]][self.pos[1]].append(self)
            if self.pos[1] == self.seat[1]:
                self.move = ''
            return

    def moveLeft(self):
        clear = True
        for seat in range(self.seat[1], self.pos[1]):
            if not self.plane.is_empty(self.pos[0], seat):
                clear = False
                for agent in self.plane.squares[self.pos[0]][seat]:
                    if agent.seat[1] > self.seat[1] and not agent in self.plane.nextSquares[self.pos[0]][self.pos[1]]:
                        agent.curMove = 'standRight'
        if not clear:
            self.plane.nextSquares[self.pos[0]][self.pos[1]].append(self)
            return
        if clear:
            myTurn = True
            for agent in self.plane.squares[self.pos[0]][self.pos[1]]:
                if agent == self:
                    continue
                if agent.seat[1] < self.seat[1] and agent.curMove == self.move:
                    myTurn = False
            if not myTurn:
                self.plane.nextSquares[self.pos[0]][self.pos[1]].append(self)
                return
            self.pos[1] -= 1
            self.plane.nextSquares[self.pos[0]][self.pos[1]].append(self)
            if self.pos[1] == self.seat[1]:
                self.move = ''
            return

    def moveUp(self):
        if self.plane.is_empty(self.pos[0] + 1, self.pos[1]) and len(self.plane.squares[self.pos[0]][self.pos[1]]) == 1:
            self.pos[0] += 1
            self.move = ''
        self.plane.nextSquares[self.pos[0]][self.pos[1]].append(self)
        return

    def setBaggage(self):
        self.plane.nextSquares[self.pos[0]][self.pos[1]].append(self)
        self.baggage -= 1
        if self.baggage == 0:
            self.move = ''
        return

    def standLeft(self):
        if self.plane.is_empty(self.pos[0], self.pos[1] - 1) or self.plane.layout[self.pos[1] - 1] == 1:
            self.pos[1] -= 1
        if self.plane.layout[self.pos[1]] == 1:
            self.move = 'right'
        self.plane.nextSquares[self.pos[0]][self.pos[1]].append(self)
        return

    def standRight(self):
        if self.plane.is_empty(self.pos[0], self.pos[1] + 1) or self.plane.layout[self.pos[1] + 1] == 1:
            self.pos[1] += 1
        if self.plane.layout[self.pos[1]] == 1:
            self.move = 'left'
        self.plane.nextSquares[self.pos[0]][self.pos[1]].append(self)
        return

    def sit(self):
        self.plane.nextSquares[self.pos[0]][self.pos[1]].append(self)
        return


class Plane(object):

    def __init__(self, seat_rows: int, seat_layout: tuple):
        """
        Plane initialization
        :param seat_rows: number of rows from the airplane
        :param seat_layout: seat columns structure; e.g. (1, 1, 1, 0, 1, 1, 1);  1 - seat, 0 - aisle
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
            if agent.curMove != 'sit':
                return False
        return True

    def is_empty(self, row: int, col: int) -> bool:
        """
        Checks if a seat is and/or will be empty
        :param row: seat's row
        :param col: set's column
        :return: seat and will be empty
        """
        return len(self.layout[row][col]) == 0 and len(self.next_layout[row][col]) == 0
