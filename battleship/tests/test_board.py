from unittest import mock

from battleship import board


def test_board_is_valid_move():
    b = board.Board()
    # test when the row is out of bounds
    with mock.patch('battleship.board.BOARD_NUM_ROWS', 8):
        assert b.is_valid_move(8, 0)[0] is False
        assert b.is_valid_move(9, 0)[0] is False
        assert b.is_valid_move(100, 0)[0] is False
    assert b.is_valid_move(-1, 0)[0] is False

    # test when the col is out of bounds
    with mock.patch('battleship.board.BOARD_NUM_COLS', 8):
        assert b.is_valid_move(0, 8)[0] is False
        assert b.is_valid_move(0, 9)[0] is False
        assert b.is_valid_move(0, 100)[0] is False
    assert b.is_valid_move(0, -1)[0] is False

    # test when it is valid
    with mock.patch('battleship.board.BOARD_NUM_COLS', 8):
        with mock.patch('battleship.board.BOARD_NUM_COLS', 8):
            assert b.is_valid_move(2, 3)[0] is True
            assert b.is_valid_move(0, 0)[0] is True
