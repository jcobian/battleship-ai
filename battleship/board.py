from collections import defaultdict
import random
from typing import List, Optional, Set, Tuple

from battleship.errors import AlreadyFiredError
from battleship.ship import Ship, ShipPiece, ShipType

BOARD_NUM_ROWS = 8
BOARD_NUM_COLS = 8


class BoardCell:
    def __init__(self):
        """Creates an empty cell on the board"""
        self.attempted_hit: bool = False
        self.ship_piece: ShipPiece = None
        self.ship: Ship = None

    def set_ship(self, ship_piece: ShipPiece, ship: Ship):
        self.ship_piece = ship_piece
        self.ship = ship

    def fire(self) -> Tuple[int, int]:
        if self.has_been_attempted():
            raise AlreadyFiredError
        self.attempted_hit = True

        is_hit = False
        is_ship_down = False

        if self.has_ship():
            self.ship_piece.hit = True
            is_hit = True
            is_ship_down = self.ship.is_destroyed()

        return (is_hit, is_ship_down)

    def has_been_attempted(self) -> bool:
        return self.attempted_hit

    def empty(self) -> bool:
        return self.ship_piece is None

    def has_ship(self) -> bool:
        return not self.empty()

    def show(self, censored=True):
        """Shows the cell

        If looking at your own board (censored = False):
            . if the cell is empty
            O if the cell was fired at and it does not have a piece of a ship
            X if the cell was fired at and it did contain a piece of a ship
            If the cell contains a ship and they haven't fired at it,
            it contains a letter representing the ship type

        If looking at your opponent's board (censored = True):
            . if the cell is empty and you haven't fired at it
            O if you fired at it and there was not a piece of a ship there
            X if you fired at it and there was a piece of a ship there
        """
        if self.has_been_attempted() and self.empty():
            # miss
            return "⚪"
        if self.empty():
            return "."

        if self.has_been_attempted() and self.has_ship():
            # TODO: if this is your own ship, then return
            # 2 characters with ship label + some sort of X
            return "🔴"

        if not self.has_been_attempted() and self.has_ship():
            if censored:
                return "."
            else:
                return str(self.ship_piece)


class Board:
    def __init__(self):
        self.ships = [
            Ship(ShipType.CARRIER),
            Ship(ShipType.BATTLESHIP),
            Ship(ShipType.FRIGATE),
            Ship(ShipType.SUBMARINE),
            Ship(ShipType.DESTROYER),
        ]
        self.game_board = self._generate_game_board(self.ships)

    def show(self, cursor_row, cursor_col,
             censored: bool = True, show_cursor: bool = False) -> str:
        """Show the board

        Parameters
        ----------
        censored : bool, optional
            Whether or not to show the locations of the ships

        Returns
        -------
        str
            A string representing the board
        """
        out = "\t"
        for col in range(BOARD_NUM_COLS):
            out += f"{col}\t"
        out += "\n"
        for row_index in range(BOARD_NUM_ROWS):
            out += f"{row_index}\t"
            row_array = self.game_board[row_index]
            output_array = []
            for col_index, board_cell in enumerate(row_array):
                # show plane icon if it is the opponent board and
                # the position is where cursor is at
                if (show_cursor is True and row_index == cursor_row and
                        col_index == cursor_col):
                    # show plane
                    output_array.append("✈️")
                else:
                    output_array.append(board_cell.show(censored=censored))
            out += '\t'.join(output_array)
            out += "\n\n"
        return out

    def is_in_bound(self, row: int, col: int) -> bool:
        return 0 <= row < BOARD_NUM_ROWS and 0 <= col < BOARD_NUM_COLS

    def is_valid_move(self, row: int, col: int) -> Tuple[bool, Optional[str]]:
        # first check if is out of bounds
        if row >= BOARD_NUM_ROWS:
            return (False, f"{row} is too big, must be "
                           f"less than {BOARD_NUM_ROWS}")
        if col >= BOARD_NUM_COLS:
            return (False, f"{col} is too big, must be "
                           f"less than {BOARD_NUM_COLS}")
        if row < 0:
            return (False, f"{row} must be greater than or equal to 0")
        if col < 0:
            return (False, f"{col} must be greater than or equal to 0")

        # now make sure cell hasn't been fired at already
        board_cell = self.game_board[row][col]
        is_valid = False if board_cell.has_been_attempted() else True
        err = None if is_valid else 'cell has already been fired at'
        return (is_valid, err)

    def surrounding_positions(
            self, positions: List[Tuple[int, int]]) -> Set[Tuple[int, int]]:
        """Returns a list of positions that surround a given a list of positions

        Notes
        -----
        Will only return valid moves that are above, below, to the left,
        or to the right
        """
        # return a set to we don't return the same spot twice
        result = set()
        spots_to_check = []
        for row, col in positions:
            # spot above
            spots_to_check.append((row - 1, col))
            # spot below
            spots_to_check.append((row + 1, col))
            # spot to left
            spots_to_check.append((row, col - 1))
            # spot to right
            spots_to_check.append((row, col + 1))
        # now for each spot, make sure it is valid
        # if so, return as a surrounding position
        for row, col in spots_to_check:
            in_bounds = self.is_in_bound(row, col)
            if in_bounds:
                result.add((row, col))
        return result

    # Start methods to generate a random game board with ships on it
    def _generate_game_board(self, ships: List[Ship]) -> List[List[BoardCell]]:
        # first initialize an empty board
        board: List[List[BoardCell]] = []
        for row in range(BOARD_NUM_ROWS):
            board.append([])
            for _ in range(BOARD_NUM_COLS):
                board_cell = BoardCell()
                board[row].append(board_cell)

        # now place all the ships on the board randomly
        self._place_ships_on_game_board(board, ships)
        return board

    def _place_ships_on_game_board(self, board: List[List[BoardCell]],
                                   ships: List[Ship]):
        def place_ship_on_game_board(board, ship):
            # key: tuple of (row, col, position)
            # value: bool on if we've attempted to place this ship here
            attempted = defaultdict(bool)
            while True:
                row = random.randint(0, BOARD_NUM_ROWS - 1)
                col = random.randint(0, BOARD_NUM_COLS - 1)
                position = random.choice(['vertical', 'horizontal'])

                # optimization so we don't retry the same place twice
                if attempted[(row, col, position)] is True:
                    continue

                if self._can_place_ship_at_position(board, ship,
                                                    row, col, position):
                    self._place_ship_at_position(board, ship,
                                                 row, col, position)
                    break
                else:
                    attempted[(row, col, position)] = True

        for ship in ships:
            place_ship_on_game_board(board, ship)

    def _place_ship_at_position(self, board: List[List[BoardCell]], ship: Ship,
                                row: int, col: int, position: str):
        if position == 'horizontal':
            row_to_fill = board[row][col: col + ship.size]
            for next_piece_index, board_cell in enumerate(row_to_fill):
                shipPiece = ship.pieces[next_piece_index]
                board_cell.set_ship(shipPiece, ship)
        else:
            column_to_fill = []
            for i in range(row, row + ship.size):
                column_to_fill.append(board[i][col])
            for next_piece_index, board_cell in enumerate(column_to_fill):
                shipPiece = ship.pieces[next_piece_index]
                board_cell.set_ship(shipPiece, ship)

    def _can_place_ship_at_position(self, board: List[List[BoardCell]],
                                    ship: Ship, row: int, col: int,
                                    position: str):
        if position == 'horizontal':
            # ship is too big to fit here horizontally
            if col + ship.size > BOARD_NUM_COLS:
                return False
            row_to_try = board[row][col:col+ship.size]

            return all([board_cell.empty() for board_cell in row_to_try])
        else:
            # ship is too big to fit here vertically
            if row + ship.size > BOARD_NUM_ROWS:
                return False
            col_to_try = []
            for i in range(row, row + ship.size):
                col_to_try.append(board[i][col])
            return all([board_cell.empty() for board_cell in col_to_try])
    # End methods to generate a random game board with ships on it
