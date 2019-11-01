from os import system
import time

from battleship.player import Player


class UiManager:
    def __init__(self, player_top: Player, player_bottom: Player):
        self.player_top = player_top
        self.player_bottom = player_bottom
        self.board_top = player_top.board
        self.board_bottom = player_bottom.board
        # TODO: pick a random position where there is not a ship
        self.cursor_row = 0
        self.cursor_col = 0

    def pick_move(self):
        # TODO: check for out of bounds
        user_input = None
        while True:
            user_input = input()
            if user_input in {'j', 'k', 'h', 'l'}:
                self._handle_cursor_move(user_input)
                self.render()
            elif user_input == 'f':
                fire_row = self.cursor_row
                fire_col = self.cursor_col
                # now move the cursor so they can see what happened
                surrounding_positions = self.board_top.surrounding_positions(
                    [(fire_row, fire_col)])
                for row, col in surrounding_positions:
                    board_cell = self.board_top.game_board[row][col]
                    if not board_cell.has_been_attempted():
                        self.cursor_row = row
                        self.cursor_col = col
                        break

                # if we didn't find an empty surrounding spot,
                # just move anywhere
                if self.cursor_row == fire_row and self.cursor_col == fire_col:
                    first_surrounding_pos = list(surrounding_positions)[0]
                    row, col = first_surrounding_pos
                    self.cursor_row = row
                    self.cursor_col = col

                return (fire_row, fire_col)

    def _handle_cursor_move(self, user_input):
        if user_input == "j":
            # move down
            self.cursor_row += 1
        elif user_input == "k":
            # move up
            self.cursor_row -= 1
        elif user_input == "h":
            # move left
            self.cursor_col -= 1
        elif user_input == "l":
            # move right
            self.cursor_col += 1

    def render(self):
        system('clear')
        self._show_boards()

    def delay(self, num_seconds):
        time.sleep(num_seconds)

    def _show_boards(self):
        print(f"{self.player_top}'s Board:")
        print(self.board_top.show(self.cursor_row,
                                  self.cursor_col, show_cursor=True))
        print("\n")

        print(f"{self.player_bottom}'s Board:")
        print(self.board_bottom.show(
            self.cursor_row, self.cursor_col,
            show_cursor=False, censored=False))
        print("\n")
