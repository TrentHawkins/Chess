"""Implements a player.

A game of chess always has two players, but this class will be able to keep track of each player stats in a meaningful way.
"""

from collections import Counter
from dataclasses import dataclass

from .piece import Piece


class Player:
    """A player.

    Attributes:
        pieces: A collection of the player's pieces.
        captured: A collection of captured pieces hashed by piece type.
            NOTE: All captured pieces are expected to have `square == None` making them distinct only by type.
    """

    def __init__(self, pieces: set[Piece] = set(), captured: Counter[Piece] = Counter()):
        """Create collections for player.

        Args:
            pieces:  A collection of the player's pieces.
            captured: A collection of captured pieces hashed by piece type.
        """
        self.pieces = pieces
        self.captured = captured
