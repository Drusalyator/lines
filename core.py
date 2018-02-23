"""This file implement the logical of the program"""
from random import randint


class Ball:
    """Class implementing a ball object"""

    def __init__(self, color=0):
        """Initialize a ball object"""
        self.color = color
        self.selected = False

    def __eq__(self, other):
        """Define the equality of balls"""
        return self.color == other.color

    def set_color(self, color):
        """Set the color (number) of the ball"""
        self.color = color

    def set_random_color(self, number_of_colors):
        """Determine the color of the ball"""
        self.color = randint(1, number_of_colors)


class Field:
    """Game Field"""

    def __init__(self, amount_cells=9, player="Player"):
        """Initialize game field"""
        self.height = amount_cells
        self.width = amount_cells
        self.player = player
        self._set_number_of_ball_per_line()
        self._set_number_of_next_ball()
        self._set_number_of_color()
        self._init_field()
        self.next_balls = []
        self.make_next_balls()
        self.set_balls = []
        self.score = 0

    def _init_field(self):
        """Initialize field"""
        self.field = []
        self.free_cells = []
        for rows in range(self.height):
            self.field.append([])
            for columns in range(self.width):
                self.field[rows].append(None)
                self.free_cells.append((columns, rows))

    def _set_number_of_color(self):
        """Set number of color"""
        self.number_of_color = self.height // 2 + 3

    def _set_number_of_ball_per_line(self):
        """Set number of a ball per line"""
        self.balls_in_line = self.height // 3 + 2

    def _set_number_of_next_ball(self):
        """Set the number of a ball put on the field"""
        self.number_of_next_ball = self.height // 4 + 1

    def make_next_balls(self):
        """Set the following balls"""
        self.next_balls.clear()
        for index in range(self.number_of_next_ball):
            ball = Ball()
            ball.set_random_color(self.number_of_color)
            self.next_balls.append(ball)

    def clear_field(self):
        """Clear the game field"""
        self.free_cells.clear()
        for rows in range(self.height):
            for columns in range(self.width):
                self.field[rows][columns] = None
                self.free_cells.append((rows, columns))

    def refresh_field(self):
        """Return the field to its initial state"""
        self.clear_field()
        self.score = 0
        self.make_next_balls()
        self.set_next_balls()

    def get_ball(self, x, y):
        """Get a ball by coordinates"""
        return self.field[y][x]

    def get_color_of_ball(self, x, y):
        """Get the color of the ball be coordinates"""
        if self.field[y][x] is not None:
            return self.field[y][x].color

    def set_ball(self, x, y, ball):
        """Set the ball by coordinates"""
        self.field[y][x] = ball
        self.free_cells.remove((x, y))

    def delete_ball(self, x, y):
        """Delete a ball by coordinates"""
        self.field[y][x] = None
        self.free_cells.append((x, y))

    def set_next_balls(self):
        """install the next balls on field"""
        if len(self.free_cells) <= self.number_of_next_ball:
            raise FieldFullException()
        self.set_balls.clear()
        for ball in self.next_balls:
            coordinates = self.free_cells[randint(0, len(self.free_cells)) - 1]
            self.set_ball(coordinates[0], coordinates[1], ball)
            self.set_balls.append((coordinates[0], coordinates[1]))
        self.make_next_balls()

    def try_move(self, start_x, start_y, end_x, end_y):
        """Try move ball in needed coordinate"""
        if self.get_ball(end_x, end_y) is not None or self.get_ball(start_x, start_y) is None:
            return False
        queue = []
        visited_cells = []
        queue.append((start_x, start_y))
        while len(queue) != 0:
            coordinates = queue.pop(0)
            if coordinates[0] < 0 or coordinates[0] >= self.height \
                    or coordinates[1] < 0 or coordinates[1] >= self.width:
                continue
            if (coordinates != (start_x, start_y) and self.get_ball(coordinates[0], coordinates[1]) is not None) \
                    or (coordinates[0], coordinates[1]) in visited_cells:
                continue
            if coordinates[0] == end_x and coordinates[1] == end_y:
                return True
            visited_cells.append((coordinates[0], coordinates[1]))
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dx != 0 and dy != 0:
                        continue
                    else:
                        queue.append((coordinates[0] + dx, coordinates[1] + dy))
        return False

    def make_step(self, start_x, start_y, end_x, end_y):
        """Make step"""
        ball = Ball(self.get_ball(start_x, start_y).color)
        self.set_ball(end_x, end_y, ball)
        self.delete_ball(start_x, start_y)

    def find_full_lines(self, x, y):
        """Find all full lines starting by coordinates of ball"""
        if self.get_ball(x, y) is None:
            return
        current_color = self.get_color_of_ball(x, y)
        ball_for_delete = []
        minus_dx = x
        plus_dx = x + 1
        while minus_dx >= 0 and self.get_color_of_ball(minus_dx, y) == current_color:
            ball_for_delete.append((minus_dx, y))
            minus_dx -= 1
        while plus_dx < self.width and self.get_color_of_ball(plus_dx, y) == current_color:
            ball_for_delete.append((plus_dx, y))
            plus_dx += 1
        if len(ball_for_delete) >= self.balls_in_line:
            return ball_for_delete
        else:
            ball_for_delete.clear()
        minus_dy = y
        plus_dy = y + 1
        while minus_dy >= 0 and self.get_color_of_ball(x, minus_dy) == current_color:
            ball_for_delete.append((x, minus_dy))
            minus_dy -= 1
        while plus_dy < self.height and self.get_color_of_ball(x, plus_dy) == current_color:
            ball_for_delete.append((x, plus_dy))
            plus_dy += 1
        if len(ball_for_delete) >= self.balls_in_line:
            return ball_for_delete
        else:
            ball_for_delete.clear()
        minus_dx = x
        minus_dy = y
        plus_dx = x + 1
        plus_dy = y + 1
        while minus_dx >= 0 and minus_dy >= 0 and self.get_color_of_ball(minus_dx, minus_dy) == current_color:
            ball_for_delete.append((minus_dx, minus_dy))
            minus_dx -= 1
            minus_dy -= 1
        while plus_dx < self.width and plus_dy < self.height and self.get_color_of_ball(plus_dx, plus_dy) == current_color:
            ball_for_delete.append((plus_dx, plus_dy))
            plus_dx += 1
            plus_dy += 1
        if len(ball_for_delete) >= self.balls_in_line:
            return ball_for_delete
        else:
            ball_for_delete.clear()
        minus_dx = x
        plus_dy = y
        while minus_dx >= 0 and plus_dy < self.height and self.get_color_of_ball(minus_dx, plus_dy) == current_color:
            ball_for_delete.append((minus_dx, plus_dy))
            minus_dx -= 1
            plus_dy += 1
        plus_dx = x + 1
        minus_dy = y - 1
        while plus_dx < self.width and minus_dy >= 0 and self.get_color_of_ball(plus_dx, minus_dy) == current_color:
            ball_for_delete.append((plus_dx, minus_dy))
            plus_dx += 1
            minus_dy -= 1
        if len(ball_for_delete) >= self.balls_in_line:
            return ball_for_delete
        else:
            return

    def delete_full_lines(self, array_of_balls_coordinates):
        """Delete full lines"""
        if array_of_balls_coordinates is not None:
            self.scoring(len(array_of_balls_coordinates))
            for coordinate in array_of_balls_coordinates:
                self.delete_ball(coordinate[0], coordinate[1])

    def scoring(self, length_of_remote_line):
        """Scoring by length of remote line"""
        multiplier = length_of_remote_line % self.balls_in_line + 1
        self.score += 10 * length_of_remote_line * multiplier


class FieldFullException(Exception):
    """Field full and no places to set next balls"""
    pass
