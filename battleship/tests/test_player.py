import pytest

from unittest import mock

from battleship import player, errors


@pytest.fixture
def player_obj():
    mock_board = mock.MagicMock()
    mock_board.ships = [mock.MagicMock(), mock.MagicMock()]
    return player.HumanPlayer(mock_board, "Jeff Probst")


def test_player_constructor():
    mock_board = mock.MagicMock()
    p = player.HumanPlayer(mock_board, "Jeff Probst")
    assert p.name == "Jeff Probst"
    assert p.board == mock_board


def test_player_repr(player_obj):
    assert str(player_obj) == "Jeff Probst"


def test_cpu_player_repr():
    mock_board = mock.MagicMock()
    p = player.CPUPlayer(mock_board, "Jack Sparrow")
    assert str(p) == "Jack Sparrow (CPU opponent)"


def test_player_make_move(player_obj):
    other_board = mock.MagicMock()
    cells = [mock.MagicMock() for i in range(4)]
    other_board.game_board = [[cells[0], cells[1]], [cells[2], cells[3]]]

    cell_to_fire = cells[3]
    cell_to_fire.fire.return_value = (True, False)
    assert player_obj.make_move(other_board, 1, 1) == (True, False)
    assert (1, 1) in player_obj.last_hits

    cell_to_fire = cells[2]
    cell_to_fire.fire.return_value = (False, False)
    assert player_obj.make_move(other_board, 1, 0) == (False, False)
    assert (1, 0) not in player_obj.last_hits

    cell_to_fire = cells[1]
    cell_to_fire.fire.return_value = (True, True)
    assert player_obj.make_move(other_board, 0, 1) == (True, True)
    assert len(player_obj.last_hits) == 0


def test_player_all_ships_down(player_obj):
    mock_ship_1 = mock.MagicMock()
    mock_ship_2 = mock.MagicMock()
    player_obj.board.ships = [mock_ship_1, mock_ship_2]

    mock_ship_1.is_destroyed.return_value = False
    mock_ship_2.is_destroyed.return_value = False
    assert player_obj.all_ships_down() is False

    mock_ship_2.is_destroyed.return_value = True
    assert player_obj.all_ships_down() is False

    mock_ship_1.is_destroyed.return_value = True
    assert player_obj.all_ships_down() is True
