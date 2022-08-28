"""Test board class."""
import pytest
from src.board import Board
from src.pieces import Pawn


@pytest.fixture
def board_start():
    return Board()


def test_movement(board_start:Board):
    cur_square = "a7"
    goto_square = "a6"
    assert isinstance(board_start["a7"], Pawn)
    assert board_start.movement(cur_square, goto_square)
    assert isinstance(board_start["a6"], Pawn)


def test_movement_nope(board_start:Board):
    cur_square = "a2"
    goto_square = "a4"
    assert not board_start.movement(cur_square, goto_square)
