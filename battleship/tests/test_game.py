from battleship import game


def test_game_constructor():
    g = game.Game()
    assert g.human_board is not None
    assert g.cpu_board is not None
    assert g.human_player is not None
    assert g.cpu_player is not None
    # make sure the boards are assigned correctly
    assert g.human_player.board == g.human_board
    assert g.human_player.board != g.cpu_board
    assert g.cpu_player.board == g.cpu_board
