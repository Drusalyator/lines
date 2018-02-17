"""This file test the logic of program (file: core)"""
import unittest
from core import *


class TestBall(unittest.TestCase):
    """Test the object Ball"""

    def test_init_balls(self):
        """Test '__init__' method"""
        test_ball = Ball()
        self.assertEqual(test_ball.color, 0)
        self.assertEqual(test_ball.selected, False)
        test_ball_2 = Ball(4)
        self.assertEqual(test_ball_2.color, 4)
        self.assertEqual(test_ball_2.selected, False)

    def test_eq_balls(self):
        """Test '__eq__' method"""
        test_ball = Ball(5)
        test_ball_2 = Ball(5)
        test_ball_3 = Ball(2)
        self.assertEqual(test_ball == test_ball_2, True)
        self.assertEqual(test_ball == test_ball_3, False)

    def test_set_color(self):
        """Test 'set_color' method"""
        test_ball = Ball()
        test_ball_2 = Ball(9)
        test_ball.set_color(3)
        test_ball_2.set_color(7)
        self.assertEqual(test_ball.color, 3)
        self.assertEqual(test_ball_2.color, 7)

    def test_set_random_color(self):
        """Test 'set_random_color' method"""
        test_ball = Ball()
        test_ball.set_random_color(5)
        self.assertEqual(test_ball.color != 0, True)
        for i in range(100):
            self.assertEqual(test_ball.color in [1, 2, 3, 4, 5], True)


class TestField(unittest.TestCase):
    """Test the object Field"""

    def test_init_field(self):
        """Test '__init__' method"""
        test_field = Field(9)
        self.assertEqual(test_field.height, 9)
        self.assertEqual(test_field.width, 9)
        self.assertEqual(test_field.balls_in_line, 5)
        self.assertEqual(test_field.number_of_next_ball, 3)
        self.assertEqual(test_field.number_of_color, 7)
        self.assertEqual(test_field.score, 0)
        self.assertEqual(len(test_field.next_balls), 3)
        test_field_2 = Field(3)
        self.assertEqual(test_field_2.field, [[None, None, None], [None, None, None], [None, None, None]])
        test_array = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)]
        self.assertEqual(len(test_array), len(test_field_2.free_cells))
        for coordinates in test_field_2.free_cells:
            self.assertEqual(coordinates in test_array, True)
        for coordinates in test_array:
            self.assertEqual(coordinates in test_field_2.free_cells, True)

    def test_make_next_ball(self):
        """Test 'make_next_ball' method"""
        test_field = Field(9)
        test_field.make_next_balls()
        self.assertEqual(len(test_field.next_balls), 3)
        for ball in test_field.next_balls:
            self.assertEqual(type(ball) == Ball, True)

    def test_get_ball(self):
        """Test 'get_ball' method"""
        test_field = Field(3)
        test_ball = Ball(2)
        test_ball_2 = Ball(7)
        test_field.field[1][2] = test_ball
        test_field.field[0][1] = test_ball_2
        self.assertEqual(test_field.get_ball(2, 1), test_ball)
        self.assertEqual(test_field.get_ball(1, 0), test_ball_2)

    def test_get_color_ball(self):
        """Test 'get_color_ball' method"""
        test_field = Field(3)
        test_ball = Ball(5)
        test_ball_2 = Ball(8)
        test_field.field[2][2] = test_ball
        test_field.field[1][0] = test_ball_2
        self.assertEqual(test_field.get_color_of_ball(2, 2), test_ball.color)
        self.assertEqual(test_field.get_color_of_ball(0, 1), test_ball_2.color)

    def test_set_ball(self):
        """Test 'set_ball' method"""
        test_field = Field(3)
        test_ball = Ball(3)
        test_ball_2 = Ball(1)
        test_field.set_ball(2, 1, test_ball)
        test_field.set_ball(0, 0, test_ball_2)
        self.assertEqual(test_field.field[1][2] == test_ball, True)
        self.assertEqual(test_field.field[0][0] == test_ball_2, True)
        self.assertEqual((2, 1) in test_field.free_cells, False)
        self.assertEqual((0, 0) in test_field.free_cells, False)

    def test_clear_field(self):
        """Test 'clear_field' method"""
        test_field = Field(3)
        test_field.set_ball(1, 1, Ball(7))
        test_field.set_ball(2, 0, Ball(4))
        test_field.set_ball(2, 1, Ball(5))
        test_field.clear_field()
        test_array = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)]
        self.assertEqual(test_field.field, [[None, None, None], [None, None, None], [None, None, None]])
        for coordinates in test_field.free_cells:
            self.assertEqual(coordinates in test_array, True)
        for coordinates in test_array:
            self.assertEqual(coordinates in test_field.free_cells, True)

    def test_refresh_field(self):
        """Test 'refresh_field' method"""
        test_field = Field(3)
        test_field.score = 50
        test_field.refresh_field()
        self.assertEqual(test_field.score, 0)

    def test_delete_ball(self):
        """Test 'delete_ball' method"""
        test_field = Field(3)
        test_field.set_ball(1, 2, Ball(8))
        self.assertEqual(test_field.get_ball(1, 2), Ball(8))
        self.assertEqual((1, 2) in test_field.free_cells, False)
        test_field.delete_ball(1, 2)
        self.assertEqual(test_field.get_ball(1, 2), None)
        self.assertEqual((1, 2) in test_field.free_cells, True)

    def test_make_step(self):
        """Test 'make_step' method"""
        test_field = Field(3)
        test_field.set_ball(2, 1, Ball(5))
        self.assertEqual((0, 0) in test_field.free_cells, True)
        test_field.make_step(2, 1, 1, 2)
        self.assertEqual(test_field.get_ball(1, 2), Ball(5))
        self.assertEqual((1, 2) in test_field.free_cells, False)
        self.assertEqual((2, 1) in test_field.free_cells, True)

    def test_find_full_lines(self):
        """Test 'find_full_lines' method"""
        test_field = Field(5)
        test_field.set_ball(1, 2, Ball(2))
        test_field.set_ball(2, 2, Ball(2))
        test_field.set_ball(3, 2, Ball(2))
        test_array = test_field.find_full_lines(1, 2)
        for coordinate in test_array:
            self.assertEqual(coordinate in [(1, 2), (2, 2), (3, 2)], True)
        test_array = test_field.find_full_lines(2, 2)
        for coordinate in test_array:
            self.assertEqual(coordinate in [(1, 2), (2, 2), (3, 2)], True)
        test_array = test_field.find_full_lines(3, 2)
        for coordinate in test_array:
            self.assertEqual(coordinate in [(1, 2), (2, 2), (3, 2)], True)
        test_field.delete_ball(3, 2)
        test_field.set_ball(3, 2, Ball(4))
        test_array = test_field.find_full_lines(1, 2)
        self.assertEqual(test_array, None)
        test_field.delete_ball(3, 2)
        test_field.set_ball(4, 2, Ball(2))
        test_array = test_field.find_full_lines(1, 2)
        self.assertEqual(test_array, None)
        test_field.clear_field()
        test_field.set_ball(4, 1, Ball(7))
        test_field.set_ball(4, 2, Ball(7))
        test_field.set_ball(4, 3, Ball(7))
        test_array = test_field.find_full_lines(4, 2)
        for coordinate in test_array:
            self.assertEqual(coordinate in [(4, 1), (4, 2), (4, 3)], True)

    def test_delete_full_line(self):
        """Test 'delete_full_line' method"""
        test_field = Field(5)
        test_field.set_ball(1, 2, Ball(2))
        test_field.set_ball(2, 2, Ball(2))
        test_field.set_ball(3, 2, Ball(2))
        test_array = test_field.find_full_lines(2, 2)
        test_field.delete_full_lines(test_array)
        for coordinates in test_array:
            self.assertEqual(test_field.get_ball(coordinates[0], coordinates[1]), None)
        test_field.clear_field()
        test_field.set_ball(1, 2, Ball(2))
        test_field.set_ball(2, 2, Ball(2))
        test_field.set_ball(4, 2, Ball(2))
        test_array = test_field.find_full_lines(2, 2)
        test_field.delete_full_lines(test_array)
        self.assertEqual(test_field.get_ball(1, 2), Ball(2))
        self.assertEqual(test_field.get_ball(2, 2), Ball(2))
        self.assertEqual(test_field.get_ball(4, 2), Ball(2))

    def test_scoring(self):
        """Test 'scoring' method"""
        test_field = Field(5)
        self.assertEqual(test_field.score, 0)
        test_field.scoring(3)
        self.assertEqual(test_field.score, 30)
        test_field.refresh_field()
        test_field.scoring(5)
        self.assertEqual(test_field.score, 150)

    def test_try_move(self):
        """Test 'try_move' method"""
        test_field = Field(5)
        self.assertEqual(test_field.try_move(3, 4, 2, 1), False)
        test_field.set_ball(2, 1, Ball(3))
        test_field.set_ball(3, 4, Ball(7))
        self.assertEqual(test_field.try_move(3, 4, 2, 1), False)
        test_field.clear_field()
        test_field.set_ball(1, 0, Ball(3))
        test_field.set_ball(1, 1, Ball(3))
        test_field.set_ball(0, 1, Ball(3))
        test_field.set_ball(3, 4, Ball(3))
        self.assertEqual(test_field.try_move(3, 4, 0, 0), False)
        test_field.delete_ball(0, 1)
        self.assertEqual(test_field.try_move(3, 4, 0, 0), True)


if __name__ == '__main__':
    unittest.main()
