import random
from typing import List

from battleship.board import Board, BOARD_NUM_ROWS, BOARD_NUM_COLS
from battleship.errors import InvalidBoardError, InvalidMoveError
from battleship.ship import Ship

_LIST_OF_NAMES = ['Will Turner', 'Elizabeth Swann']


class Player:
    def __init__(self, board: Board, name: str = None):
        self.name = name or self._generate_name()
        self.board = board

    def pick_move(self, board: Board) -> (int, int):
        """Prompts the player to make a move to execute on a given board
        Paramters
        ---------
        board : `battleship.board.Board`
          The board to make a move on

        Returns
        -------
        (int, int) : the row and column on the board to make a move on

        Raises
        ------
        `battleship.errors.InvalidBoardError`
            If the board is the player's board.
            This must be run on a board that is not yours.
        `battleship.errors.InvalidMoveError`
            If the move is invalid
            Moves can be invalid because they are out of bounds or
            because they've already been attempted
        """
        if board == self.board:
            raise InvalidBoardError("Cannot make a move on your own board")

        row, col = self._ask_user_for_input()
        is_valid, err = board.is_valid_move(row, col)
        if is_valid:
            return (row, col)
        else:
            raise InvalidMoveError(err)

    def make_move(self, board: Board, row: int, col: int):
        board_cell = board.game_board[row][col]
        is_hit, is_ship_down = board_cell.fire()
        return (is_hit, is_ship_down)

    def all_ships_down(self) -> bool:
        return all([s.is_destroyed() for s in self.ships()])

    def ships(self) -> List[Ship]:
        return self.board.ships

    def _ask_user_for_input(self) -> (int, int):
        prompt = """
            Where would you like to play?
            Specify as 2 comma separated values for the
            row and column (e.g 1,2):
        """
        val = input(prompt)
        val_as_array = [int(x) for x in val.split(',')]
        return (val_as_array[0], val_as_array[1])

    def __repr__(self):
        return f"{self.name}"

    def _generate_name(self) -> str:
        return random.choice(_LIST_OF_NAMES)


class CPUPlayer(Player):
    def pick_move(self, board: Board) -> (int, int):
        """CPU logic to pick a move"""
        # TODO: For now, just random. Next steps is to make it smart
        while True:
            row = random.randint(0, BOARD_NUM_ROWS)
            col = random.randint(0, BOARD_NUM_COLS)
            is_valid, _ = board.is_valid_move(row, col)
            if is_valid:
                break
        return (row, col)

    def __repr__(self):
        return f"{super().__repr__()} (CPU opponent)"
