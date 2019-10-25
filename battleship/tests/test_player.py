import pytest

from unittest import mock

from battleship import player, errors


@pytest.fixture
def player_obj():
    mock_board = mock.MagicMock()
    mock_board.ships = [mock.MagicMock(), mock.MagicMock()]
    return player.Player(mock_board, "Jeff Probst")


def test_player_constructor():
    mock_board = mock.MagicMock()
    p = player.Player(mock_board, "Jeff Probst")
    assert p.name == "Jeff Probst"
    assert p.board == mock_board


def test_player_repr(player_obj):
    assert str(player_obj) == "Jeff Probst"


@mock.patch.object(player.Player, '_ask_user_for_input')
def test_player_pick_move(mock_ask_user, player_obj):
    mock_ask_user.return_value = (1, 2)
    other_board = mock.MagicMock()
    other_board.is_valid_move.return_value = (True, None)
    assert player_obj.pick_move(other_board) == (1, 2)


@mock.patch.object(player.Player, '_ask_user_for_input')
def test_player_pick_move_if_move_invalid(mock_ask_user, player_obj):
    mock_ask_user.return_value = (1, 2)
    other_board = mock.MagicMock()
    other_board.is_valid_move.return_value = (False, 'some error')
    with pytest.raises(errors.InvalidMoveError) as excinfo:
        player_obj.pick_move(other_board)
        assert 'some error' in str(excinfo.value)


def test_player_pick_move_if_board_invalid(player_obj):
    with pytest.raises(errors.InvalidBoardError):
        player_obj.pick_move(player_obj.board)


def test_cpu_player_repr():
    mock_board = mock.MagicMock()
    p = player.CPUPlayer(mock_board, "Jack Sparrow")
    assert str(p) == "Jack Sparrow (CPU opponent)"
