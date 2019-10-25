from collections import defaultdict
import random

from battleship.ship import Ship

BOARD_NUM_ROWS = 8
BOARD_NUM_COLS = 8


class Board:
    def __init__(self):
        self.ships = [
            Ship("Carrier", 5),
            Ship("Battleship", 4),
            Ship("Frigate", 3),
            Ship("Submarine", 3),
            Ship("Destroyer", 2),
        ]
        self.game_board = self._generate_game_board(self.ships)

    def show(self, censored=True):
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
        for row in range(BOARD_NUM_ROWS):
            out += f"{row}\t"
            out += '\t'.join([board_cell.show(censored=censored)
                             for board_cell in self.game_board[row]])
            out += "\n\n"
        return out

    def is_valid_move(self, row, col):
        if row >= BOARD_NUM_ROWS or col >= BOARD_NUM_COLS:
            return False
        if row < 0 or col < 0:
            return False

        # return false if it has already been attempted
        return not self.game_board[row][col].attemptedHit

    def _generate_game_board(self, ships):
        # first initialize an empty board
        board = []
        for row in range(BOARD_NUM_ROWS):
            board.append([])
            for _ in range(BOARD_NUM_COLS):
                board_cell = BoardCell()
                board[row].append(board_cell)

        self._place_ships_on_game_board(board, ships)
        return board

    def _place_ships_on_game_board(self, board, ships):
        def place_ship_on_game_board(board, ship):
            # key: tuple of (row, col, position)
            # value: bool on if we've attempted to place this ship here
            attempted = defaultdict(bool)
            while True:
                row = random.randint(0, BOARD_NUM_ROWS - 1)
                col = random.randint(0, BOARD_NUM_COLS - 1)
                position = random.choice(['vertical', 'horizontal'])

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

    def _place_ship_at_position(self, board, ship, row, col, position):
        if position == 'horizontal':
            row_to_fill = board[row][col: col + ship.size]
            for next_piece_index, board_cell in enumerate(row_to_fill):
                shipPiece = ship.pieces[next_piece_index]
                board_cell.placeShipPieceHere(shipPiece, ship)
        else:
            column_to_fill = []
            for i in range(row, row + ship.size):
                column_to_fill.append(board[i][col])
            for next_piece_index, board_cell in enumerate(column_to_fill):
                shipPiece = ship.pieces[next_piece_index]
                board_cell.placeShipPieceHere(shipPiece, ship)

    def _can_place_ship_at_position(self, board, ship, row, col, position):
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


class BoardCell:
    def __init__(self, value=None):
        """Creates a cell on the board

        Parameters
        ----------
        value : `battleship.ship.ShipPiece`, optional
            If not supplied, this is an empty piece on the board
            If ShipPiece, a piece of a ship is located here
        """

        self.attemptedHit = False
        self.value = value
        self.ship = None

    def placeShipPieceHere(self, shipPiece, ship):
        self.value = shipPiece
        self.ship = ship

    def fire(self):
        self.attemptedHit = True
        is_hit = False
        is_ship_down = False

        if not self.empty():
            ship_piece = self.value
            ship_piece.hit = True
            is_hit = True
            is_ship_down = self.ship.is_destroyed()

        return (is_hit, is_ship_down)

    def empty(self):
        return self.value is None

    # opponent
    # . if empty and i haven't tried
    # O if i've tried and it is empty
    # X if i've tried and it was a hit
    # my board
    # . if empty
    # O if they tried that place and it was empty
    # X if they 've tried and it was a hit
    # PieceName if they haven't tried and a piece is there
    def show(self, censored=True):
        if self.attemptedHit and self.empty():
            return "O"
        if self.empty():
            return "."

        if self.attemptedHit and not self.empty():
            return "X"

        if not self.attemptedHit and not self.empty():
            if censored:
                return "."
            else:
                return str(self.value)
