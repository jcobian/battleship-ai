import random

from battleship.player import Player, CPUPlayer
from battleship.board import Board
from battleship.errors import InvalidMoveError

_HIT_PHRASES = [
    'Nice, you hit a ship!',
    'Great job! You got one!',
]

_MISS_PHRASES = [
    'Nope',
    'Better luck next time',
    'No dice',
]


class Game:
    def __init__(self, human_player_name=None):
        self.human_board = Board()
        self.cpu_board = Board()

        self.human_player = Player(self.human_board,
                                   name=human_player_name)
        self.cpu_player = CPUPlayer(self.cpu_board,
                                    "Jack Sparrow")

    def start_game(self):
        while True:
            action = self._ask_for_action()
            if action == 'q':
                print("Game over!")
                return
            elif action == 'p':
                # Human turn first
                try:
                    row, col = self.human_player.pick_move(self.cpu_board)
                except InvalidMoveError:
                    print("This move is invalid")
                    continue

                is_hit, is_ship_down = self.human_player.make_move(
                    self.cpu_board, row, col)
                if is_hit:
                    print(random.choice(_HIT_PHRASES))
                    if is_ship_down:
                        print("You also took down a ship!")
                        if self.cpu_player.all_ships_down():
                            print("That's Game over!! You win!!")
                            return
                else:
                    print(random.choice(_MISS_PHRASES))

                # Cpu turn
                row, col = self.cpu_player.pick_move(self.human_board)
                cpu_msg = f"{self.cpu_player} made a move at {row},{col}\n"
                is_hit, is_ship_down = self.cpu_player.make_move(
                    self.human_board, row, col)
                if is_hit:
                    cpu_msg += "And it was a hit..\n"
                    if is_ship_down:
                        cpu_msg += "It also took down your ship.."
                        if self.human_player.all_ships_down():
                            cpu_msg += "That's Game over!! You lose...."
                            print(cpu_msg)
                            return
                else:
                    cpu_msg += "And they missed!"
                print(cpu_msg)

            elif action == 's':
                print(f"{self.cpu_player}'s Board:")
                print(self.cpu_board.show())
                print("\n")

                print(f"{self.human_player}'s Board:")
                print(self.human_board.show(censored=False))
                print("\n")

    def _ask_for_action(self):
        prompt = """
        Pick an action:
          (p): Play! Choose this to make a move
          (s): Show the board
          (q): Quit the game
        """
        while True:
            val = input(prompt)
            if val in {'p', 's', 'q'}:
                return val
            else:
                print("Invalid option, try again")
