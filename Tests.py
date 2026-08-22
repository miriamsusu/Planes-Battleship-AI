import unittest
from Board import *
from Game import *


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_initialization(self):
        """Verify the board is a 10x10 grid of spaces."""
        self.assertEqual(len(self.board._board), 10)
        self.assertEqual(len(self.board._board[0]), 10)
        self.assertEqual(self.board.get_cell(0, 0), " ")

    def test_set_and_get_cell(self):
        self.board.set_cell(2, 5)
        self.assertEqual(self.board._board[5][2], 'x')
        self.assertEqual(self.board.get_cell(5, 2), 'x')

    def test_str_format(self):
        """Check if the string representation contains header and borders."""
        output = str(self.board)
        self.assertIn("1 2 3 4 5 6 7 8 9 10", output)
        self.assertIn("A |", output)
        self.assertIn("J |", output)


class TestBuildPlayerBoard(unittest.TestCase):
    def setUp(self):
        self.p_board = PlayerBoard()
        self.builder = BuildPlayerBoard(self.p_board)

    def test_get_plane_coordinates_up(self):
        """Verify the 'UP' shape generation."""
        coords = self.builder.get_plane_coordinates(0, 5, "UP")
        self.assertEqual(len(coords), 8)
        self.assertIn((0, 5), coords)  # Head
        self.assertIn((3, 6), coords)  # Part of tail

    def test_is_valid_boundary(self):
        """Check that coordinates outside 0-9 are invalid."""
        invalid_coords = [(-1, 0), (0, 0)]
        self.assertFalse(self.builder.is_valid(invalid_coords))

        valid_coords = [(0, 0), (1, 1)]
        self.assertTrue(self.builder.is_valid(valid_coords))

    def test_place_plane(self):
        """Verify plane head symbol matches direction."""
        self.builder.place_plane(2, 2, "UP")
        self.assertEqual(self.p_board.get_cell(2, 2), "^")
        self.assertEqual(self.p_board.get_cell(3, 2), "x")


class TestGameLogic(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.logic = GameLogic(self.board)

    def test_try_coords_hit(self):
        self.board._board[1][1] = "x"
        self.assertEqual(self.logic.try_coords(1, 1), "hit")

    def test_try_coords_down(self):
        self.board._board[1][1] = "v"
        self.assertEqual(self.logic.try_coords(1, 1), "down")

    def test_try_coords_empty(self):
        self.assertEqual(self.logic.try_coords(5, 5), "empty")


class TestPlaneAI(unittest.TestCase):
    def setUp(self):
        self.p_board = PlayerBoard()
        self.ai = PlaneAI(self.p_board)

    def test_process_result_down(self):
        """Verify AI tracks remaining planes correctly."""
        initial_planes = self.ai.planes_remaining
        self.ai.process_result(1, 1, "down")
        self.assertEqual(self.ai.planes_remaining, initial_planes - 1)
        self.assertEqual(self.ai.shots[(1, 1)], "down")

    def test_hunt_logic(self):
        """Ensure hunt returns a valid coordinate and removes it from available."""
        move = self.ai._hunt()
        self.assertIsInstance(move, tuple)
        self.assertEqual(len(move), 2)
        self.assertNotIn(move, self.ai.available)

    def test_possible_heads_inference(self):
        """Complex test: AI should find head if wings are hit."""
        self.ai.process_result(3, 5, "hit")
        heads = self.ai._possible_heads()
        self.assertIn((0, 5), heads)

    def test_adjacent_targeting(self):
        """AI should target +/- 1 cells when it has a body hit."""
        self.ai.process_result(5, 5, "hit")
        adj_move = self.ai.get_move()
        neighbors = [(4, 5), (6, 5), (5, 4), (5, 6)]
        self.assertIn(adj_move, neighbors)


if __name__ == '__main__':
    unittest.main()