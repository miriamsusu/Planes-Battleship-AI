class Board:
    def __init__(self):
        self._board = [[" " for _ in range(10)] for _ in range(10)]

    def get_cell(self, row, column):
        cell = self._board[row][column]
        return cell

    def set_cell(self, row, column):
        self._board[column][row] = 'x'

    def __str__(self):
        header = "    " + " ".join(str(i) for i in range(1,11)) + "\n"
        separator = "  +" + "-" * 21 + "+\n"

        output = header + separator

        for i, row in enumerate(self._board):
            letter = chr(ord('A') + i)
            row_str = f"{letter} | " + " ".join(row) + " |\n"
            output += row_str

        output += separator
        return output


class PlayerBoard(Board):
    def __init__(self):
        super().__init__()

class ComputerBoard(Board):
    def __init__(self):
        super().__init__()