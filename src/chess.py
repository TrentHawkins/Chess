"""A game of chess."""


from itertools import cycle

from .board import Board
from .player import Player


class Chess:
    """A chess game."""

    def __init__(self):
        """Start a chess game."""
        self.board = Board()

    #   Player piece collections are made agnostic of board position, in case a game is formed from a custom position instead.
        self.player = cycle(
            [
                Player(pieces=set(piece for piece in self.board if piece.orientation == -1)),  # white
                Player(pieces=set(piece for piece in self.board if piece.orientation == +1)),  # black
            ]
        )
