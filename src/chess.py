"""A game of chess."""


from itertools import cycle

from .board import Board
from .player import Player


class Chess:
    """A chess game."""

    def __init__(self):
        """Start a chess game."""
        self.board = Board()

    #   Cycle players through to run the game.
        self.player = cycle(
            [
                Player("White", "white", self.board),  # input("Enter player name for white: ")
                Player("Black", "black", self.board),  # input("Enter player name for black: ")
            ]
        )
