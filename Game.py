import random
class PlaneBuilder:
    """Base class containing what both boards need"""
    def __init__(self, board_obj):
        self._board_obj = board_obj

    def get_plane_coordinates(self, r, c, direction):
        """
        :param r: the row for the front of the plane
        :param c: the column for the front of the plane
        :param direction: up/down/right/left
        :return: returns the coordinates for all the components of a plane
        """
        direction = direction.upper()
        coords = [(r, c)]

        if direction == "UP":
            coords += [(r + 1, c - 1), (r + 1, c), (r + 1, c + 1)]
            coords += [(r + 2, c)]
            coords += [(r + 3, c - 1), (r + 3, c), (r + 3, c + 1)]
        elif direction == "DOWN":
            coords += [(r - 1, c - 1), (r - 1, c), (r - 1, c + 1)]
            coords += [(r - 2, c)]
            coords += [(r - 3, c - 1), (r - 3, c), (r - 3, c + 1)]
        elif direction == "LEFT":
            coords += [(r - 1, c + 1), (r, c + 1), (r + 1, c + 1)]
            coords += [(r, c + 2)]
            coords += [(r - 1, c + 3), (r, c + 3), (r + 1, c + 3)]
        elif direction == "RIGHT":
            coords += [(r - 1, c - 1), (r, c - 1), (r + 1, c - 1)]
            coords += [(r, c - 2)]
            coords += [(r - 1, c - 3), (r, c - 3), (r + 1, c - 3)]

        return coords

    def is_valid(self, coords):
        """

        :param coords: will contain a list of tubles with all the coordinates for a plane
        :return: True -> if we can place the plane on the board, False -> if we can't place the plane on the board
        """
        for r, c in coords:
            if not (0 <= r <= 9 and 0 <= c <= 9):
                return False
            cell_value = self._board_obj.get_cell(r, c)
            if cell_value != " ":
                return False
        return True

class BuildPlayerBoard(PlaneBuilder):
    def __init__(self, playerboard):
        super().__init__(playerboard)

    def place_plane(self, r, c, direction):
        """

        :param r: input parameter for the row
        :param c: input parameter for the column
        :param direction: chosen direction
        :return: places the plane on the board
        """
        coords = self.get_plane_coordinates(r, c, direction)
        if self.is_valid(coords):
            for i, (pr, pc) in enumerate(coords):
                if i == 0:
                    heads = {"UP": "^", "DOWN": "v", "LEFT": "<", "RIGHT": ">"}
                    self._board_obj._board[pr][pc] = heads[direction.upper()]
                else:
                    self._board_obj._board[pr][pc] = "x"
            return True
        else:
            return False

class BuildComputerBoard(PlaneBuilder):
    def __init__(self, computerboard):
        super().__init__(computerboard)

    def generate_random_coordinates(self):
        """
        :return: will generate random coordinates for the computer planes and choose a direction
        """
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        return random.randint(0, 9), random.randint(0, 9), random.choice(directions)

    def place_planes(self):
        """
        :return: places the planes on the board if valid
        """
        planes_placed = 0
        while planes_placed != 3:
            r, c, direction = self.generate_random_coordinates()
            coords = self.get_plane_coordinates(r, c, direction)
            if self.is_valid(coords):
                for i, (pr, pc) in enumerate(coords):
                    if i == 0:
                        heads = {"UP": "^", "DOWN": "v", "LEFT": "<", "RIGHT": ">"}
                        self._board_obj._board[pr][pc] = heads[direction.upper()]
                    else:
                        self._board_obj._board[pr][pc] = "x"
                planes_placed += 1
class GameLogic:
    def __init__(self,board):
        self._game_board = board

    def try_coords(self, r, c):
        """

        :param r: rwo coordinate we are checking
        :param c: cell coordinate we are checking
        :return: if a plane was hit/downed or if the cell is empty
        """
        cell_value = self._game_board.get_cell(r,c)
        if cell_value != " ":
            if cell_value == "x":
                return "hit"
            else:
                return "down"
        else:
            return "empty"

class PlaneAI(GameLogic):
    BOARD_SIZE = 10

    PLANE_SHAPES = {
        "UP": [(0, 0), (1, -1), (1, 0), (1, 1), (2, 0), (3, -1), (3, 0), (3, 1)],
        "DOWN": [(0, 0), (-1, -1), (-1, 0), (-1, 1), (-2, 0), (-3, -1), (-3, 0), (-3, 1)],
        "LEFT": [(0, 0), (-1, 1), (0, 1), (1, 1), (0, 2), (-1, 3), (0, 3), (1, 3)],
        "RIGHT": [(0, 0), (-1, -1), (0, -1), (1, -1), (0, -2), (-1, -3), (0, -3), (1, -3)],
    }

    def __init__(self, player_board):
        super().__init__(player_board)
        self.shots = {}
        self.available = {(r, c) for r in range(10) for c in range(10)}
        self.planes_remaining = 3

    def get_move(self):
        """
        This is organized taking into consideration the importance of the move:
        1. if the computer can win in one move(most important)
        2. if the computer finds possible heafs(2nd most important)
        3. if there are no head possibilities but here are hits, it checks the proximity of the hits(3rd most important)
        4. if there are no cluse it generates a random unused move(least important)
        :return: returns the best move
        """
        win = self._forced_head()
        if win:
            self.available.remove(win)
            return win
        kill = self._best_destroy()
        if kill:
            self.available.remove(kill)
            return kill
        adj = self._get_adjacent_targets()
        if adj:
            move = random.choice(adj)
            self.available.remove(move)
            return move
        return self._hunt()

    def process_result(self, r, c, result):
        """

        :param r: row coordinate
        :param c: column coordinate
        :param result: empty/hit/down
        :return: if result is down it means that the computer downed a plane and the number of remaining planes decreases
        """
        self.shots[(r, c)] = result
        if result == "down":
            self.planes_remaining -= 1

    def _forced_head(self):
        """
        :return: if there is one plan e left and one head possibility then we try it in order to win in one move
        """
        if self.planes_remaining != 1:
            return None
        heads = self._possible_heads()
        if len(heads) == 1:
            h = next(iter(heads))
            if h in self.available:
                return h
        return None

    def _best_destroy(self):
        """
        :return: coordinates for a possible move in order to hit a head
        """
        heads = self._possible_heads()
        for h in heads:
            if h in self.available:
                return h
        return None

    def _get_adjacent_targets(self):
        """Finds valid adjacent coordinates +/- 1 from body hits."""
        hits = {p for p, r in self.shots.items() if r == "hit"}
        adj_targets = set()
        for r, c in hits:
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if (nr, nc) in self.available:
                    adj_targets.add((nr, nc))
        return list(adj_targets)

    def _possible_heads(self):
        """
        This function checks if the cells can be heads taking into consideration the shape of the plane(direction and
        coordinates). If there are no hits in the structure of the proposed plane or if there are misses in
        the structure of the proposed plane, we will not add the "head" to the possible heads
        :return: all possible heads for a plane
        """
        hits = {p for p, r in self.shots.items() if r in ("hit", "down")}
        misses = {p for p, r in self.shots.items() if r == "empty"}
        heads = set()

        for r in range(10):
            for c in range(10):
                for shape in self.PLANE_SHAPES.values():
                    cells = set()
                    valid = True
                    for dr, dc in shape:
                        nr, nc = r + dr, c + dc
                        if not (0 <= nr < 10 and 0 <= nc < 10):
                            valid = False
                            break
                        cells.add((nr, nc))

                    if not valid:
                        continue

                    if not hits.isdisjoint(cells):
                        if not any(m in cells for m in misses):
                            heads.add((r, c))
        return heads

    def _hunt(self):
        """
        :return: random move if the computer has no hints to hit a plane
        """
        choices = [p for p in self.available if (p[0] + p[1]) % 2 == 0]
        if not choices:
            choices = list(self.available)
        move = random.choice(choices)
        self.available.remove(move)
        return move