"""Implements a player.

A game of chess always has two players, but this class will be able to keep track of each player stats in a meaningful way.
"""

from collections import Counter
from dataclasses import dataclass

from .board import Board
from .piece import Orientation


@dataclass(init=False, repr=False)
class Player:
    """A player.

    Attributes:
        board: The board this player is playing on.
        orientation: The allegiance of the player, defining the correspponding orientation of the board.
        pieces: A collection of the player's pieces on the board.
        captured: A collection of captured pieces hashed by piece type.
            NOTE: All captured pieces are expected to have `square == None` making them distinct only by type.
    """

    def __init__(self, board: Board, color: str):
        """Create collections for player.

        Args:
            board: The board this player is playing on.
            orientation: The allegiance of the player, defining the correspponding orientation of the board.
        """
        self.board: Board = board  # The board this player is playing on.
        self.orientation: Orientation = Orientation[color]  # The allegiance of the player.

    #   Assign pieces to player agnostically, so that custom position can also be loaded.
        self.pieces = set(piece for piece in self.board if piece.orientation == self.orientation)
        self.captured = Counter()  # In custom positions, captured material is immaterial.
