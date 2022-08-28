"""Test Piece class and subtypes."""
import pytest
from src.pieces import Pawn


def test_check_move():
    pawn = Pawn("black")
    assert pawn.check_movement((1, 0), None)
    assert not pawn.check_movement((0, 1), None)