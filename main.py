from battleship.game import Game


def main():
    name = input("What is your name? ")
    game = Game(human_player_name=name)
    game.start_game()


if __name__ == "__main__":
    main()
