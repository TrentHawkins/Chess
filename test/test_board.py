"""Test board class."""
import pytest
from src.board import Board, difference
from src.pieces import Pawn, Rook


@pytest.fixture
def board_start():
    return Board()


def test_movement_single_pawn(board_start:Board):
    cur_square = "a7"
    goto_square = "a6"
    cur = board_start._indices(cur_square)
    goto = board_start._indices(goto_square)
    move = difference(cur, goto)
    assert not board_start.check_move_blocked(cur, move)
    assert isinstance(board_start["a7"], Pawn)
    assert board_start.movement(cur_square, goto_square)
    assert isinstance(board_start["a6"], Pawn)


def test_movement_pawn_mvoes_only_one_square(board_start:Board):
    cur_square = "a2"
    goto_square = "a4"
    assert not board_start.movement(cur_square, goto_square)


def test_movement_rook_is_blocked_by_pawn(board_start:Board):
    cur_square = "a1" # rook is here
    goto_square = "a2" # pawn is here
    cur = board_start._indices(cur_square)
    goto = board_start._indices(goto_square)
    move = difference(cur, goto)
    assert isinstance(board_start[cur_square], Rook)
    assert board_start.check_move_blocked(cur, move)


def test_movement_rook_after_moving_blocking_pawn(board_start:Board):
    cur = "a1" # rook is here
    goto_rook = "a2" # pawn is here
    goto_pawn = "a3" # empty
    assert board_start.movement(goto_rook, goto_pawn)
    assert board_start.movement(cur, goto_rook)


def test_movement_rook_captures_pawn(board_start:Board):
    cur = "a1" # rook is here
    goto_rook = "a7" # pawn is here
    board_start["a2"] = None # remove friendly pawn so rook can move
    assert board_start.movement(cur, goto_rook)


def test_movement_rook_blocked_by_enemy_pawn(board_start:Board):
    cur = "a1" # rook is here
    goto_rook = "a8" # pawn is here
    board_start["a2"] = None # remove friendly pawn so rook can move
    assert not board_start.movement(cur, goto_rook)
