import random

from battleship.player import CPUPlayer, HumanPlayer, Player
from battleship.board import Board
from battleship.errors import InvalidMoveError
from battleship.ui_manager import UiManager

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
    def __init__(self, human_player_name: str = None):
        self.human_board = Board()
        self.cpu_board = Board()

        self.human_player = HumanPlayer(self.human_board,
                                        name=human_player_name)
        self.cpu_player = CPUPlayer(self.cpu_board,
                                    "Jack Sparrow")

        self.ui_manager = UiManager(self.cpu_player, self.human_player)

    def start_game(self):
        """Plays Battleship in the terminal by asking for user input"""
        # print the board initially before starting
        self.ui_manager.render()
        while True:
            # Human turn first
            try:
                row, col = self.ui_manager.pick_move()
                self.human_player.validate_move(
                    self.cpu_board, row, col)
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
            # Step 1: Human has moved, but CPU has not
            self.ui_manager.render()
            self.ui_manager.delay(1)

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
            # Step 2: CPU has made move
            self.ui_manager.render()

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
