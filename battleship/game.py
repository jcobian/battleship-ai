import random

from battleship.player import (
    Player,
    CPUPlayerRandom,
)
from battleship.cpu_player_reinforcement import CPUPlayerReinforcment
from battleship.board import Board
from battleship.errors import InvalidMoveError

_HIT_PHRASES = [
    'Aye, you hit a ship!',
    'Great job! You got one!',
]

_MISS_PHRASES = [
    'You misssed..',
    'Nada. Better luck next time',
    'No dice mate :(',
]


class Game:
    def __init__(self, human_player_name: str = None,
                 cpu_strategy: str = None):
        self.human_board = Board()
        self.cpu_board = Board()

        self.human_player = Player(self.human_board,
                                   name=human_player_name)

        cpu_player = None
        cpu_player_name = "Jack Sparrow"
        if cpu_strategy == 'random':
            cpu_player = CPUPlayerRandom(self.cpu_board,
                                         cpu_player_name)
        elif cpu_strategy == 'reinforcement_learning':
            cpu_player = CPUPlayerReinforcment(self.cpu_board,
                                               cpu_player_name)
            cpu_player.train()
        self.cpu_player = cpu_player

    def start_game(self):
        """Plays Battleship in the terminal by asking for user input"""
        # print the board initially before starting
        self._print_boards()
        while True:
            action = self._ask_for_action()
            if action == 'q':
                print("Game over!")
                return
            elif action == 'h':
                self._print_help()
            elif action == 'p':
                # Human turn first
                try:
                    row, col = self.human_player.pick_move(self.cpu_board)
                except InvalidMoveError as exc:
                    print(f"This move is invalid: {exc}")
                    continue

                print("\n")
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

                print("\n\n")
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
                self._print_boards()
            elif action == 'i':
                self._print_status(self.cpu_player)
                self._print_status(self.human_player)

    def _print_status(self, player: Player):
        """Prints status for a given player"""
        print(f"{player}'s ship status:")
        for ship in player.ships():
            if ship.is_destroyed():
                print(f"\t{ship}: Destroyed!")
            else:
                print(f"\t{ship}: Alive!")

    def _ask_for_action(self):
        prompt = """
        Pick an action:
          (p): Play! Choose this to make a move
          (s): Show the board
          (i): Show the status of you and your opponent's ships
          (h): Print out a help screen explaining the board
          (q): Quit the game
        """
        while True:
            val = input(prompt)
            if val in {'p', 's', 'q', 'h', 'i'}:
                return val
            else:
                print("Invalid option, try again")

    def _print_help(self):
        msg = """
        You and your opponent each have 5 ships. They are:
            CARRIER (C)
            BATTLESHIP (B)
            FRIGATE (F)
            SUBMARINE (S)
            DESTROYER (D)

        If looking at your own board:
            - A period is shown meaning the cell is empty (no ship there)
            - O if the cell was fired at by your opponent and it does not
            have a piece of a ship
            - X if the cell was fired at by your opponent and it did contain
            a piece of a ship
            - If the cell contains a ship and they haven't fired at it,
            it contains a letter representing the ship type (see above)

        If looking at your opponent's board:
            - A period is shown if the cell is empty and
            you haven't fired there
            - O if you fired at it and there was not a piece of a ship there
            - X if you fired at it and there was a piece of a ship there
        """
        print(msg)

    def _print_boards(self):
        print(f"{self.cpu_player}'s Board:")
        print(self.cpu_board.show())
        print("\n")

        print(f"{self.human_player}'s Board:")
        print(self.human_board.show(censored=False))
        print("\n")
