from abc import ABC
import random
from typing import List, Tuple

from battleship.board import Board, BOARD_NUM_ROWS, BOARD_NUM_COLS
from battleship.errors import InvalidBoardError, InvalidMoveError
from battleship.ship import Ship

_LIST_OF_NAMES = ['Will Turner', 'Elizabeth Swann']


class Player(ABC):
    def __init__(self, board: Board, name: str = None):
        self.name = name or self._generate_name()
        self.board = board
        # keep track of the last succesful hits
        self.last_hits: List[Tuple[int, int]] = []

    def pick_move(self, board: Board) -> Tuple[int, int]:
        pass

    def make_move(self, board: Board, row: int, col: int):
        board_cell = board.game_board[row][col]
        is_hit, is_ship_down = board_cell.fire()
        if is_hit:
            self.last_hits.append((row, col))
        if is_ship_down:
            # once we've taken a ship down, can forget about the last hit
            # you've made. Time to search elsewhere
            self.last_hits = []
        return (is_hit, is_ship_down)

    def all_ships_down(self) -> bool:
        return all([s.is_destroyed() for s in self.ships()])

    def ships(self) -> List[Ship]:
        return self.board.ships

    def __repr__(self):
        return f"{self.name}"

    def _generate_name(self) -> str:
        return random.choice(_LIST_OF_NAMES)


class HumanPlayer(Player):
    def validate_move(self, board: Board,
                      row: int, col: int):
        """Validtes the human move on a board
        Paramters
        ---------
        board : `battleship.board.Board`
          The board to make a move on

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

        is_valid, err = board.is_valid_move(row, col)
        if not is_valid:
            raise InvalidMoveError(err)

    def _ask_user_for_input(self) -> Tuple[int, int]:
        prompt = """
            Where would you like to play?
            Specify as 2 comma separated values for the
            row and column (e.g 1,2):
        """
        val = input(prompt)
        val_as_array = [int(x) for x in val.split(',')]
        return (val_as_array[0], val_as_array[1])


class CPUPlayer(Player):
    def pick_move(self, board: Board) -> Tuple[int, int]:
        """CPU logic to pick a move"""
        # if we are flying blind, just go for anything
        if len(self.last_hits) == 0:
            return self._pick_random_move(board)

        # find all positions surrounding any of our previous hits
        surrounding_positions = board.surrounding_positions(self.last_hits)
        for row, col in surrounding_positions:
            # pick first surrounding position we find that is valid
            # TODO: we can optimize to have it
            # keep searching along a direction
            is_valid, _ = board.is_valid_move(row, col)
            if is_valid:
                return (row, col)

        # no valid surrounding moves, so reset the last hits
        self.last_hits = []
        return self.pick_move(board)

    def _pick_random_move(self, board: Board) -> Tuple[int, int]:
        while True:
            row = random.randint(0, BOARD_NUM_ROWS)
            col = random.randint(0, BOARD_NUM_COLS)
            is_valid, _ = board.is_valid_move(row, col)
            if is_valid:
                break
        return (row, col)

    def __repr__(self):
        return f"{super().__repr__()} (CPU opponent)"
