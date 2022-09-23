"""A game of chess."""


from types import MethodType

from .board import Board
from .piece import Piece
from .player import Player
from .square import Square


class Chess:
    """A chess game."""

    def __init__(self, board: Board = Board()):
        """Start a chess game."""
        self.board = board

    #   White starts first, but this player will alwyas be the current one.
        self.current = Player("White", "white", self.board)  # input("Enter player name for white: ")
        self.opponent = Player("Black", "black", self.board)  # input("Enter player name for black: ")

        def king_deployable(source_piece: Piece, target: Square):
            source_piece.deployable.__doc__
            target_piece = self.board[target]

        #   NOTE: Applying method directly to `source_piece` causes infinite recursion.
        #   A more explicit resolution is required.
        #   However, since method is updated for all pieces on the board,
        #   and since each one of them is a strict `Piece` subclass,
        #   we need the actual class name to resolve the redefinition.

            return source_piece.__class__.deployable(source_piece, target) \
                and target_piece is None \
                and target not in self.opponent.checks

        def king_capturable(source_piece: Piece, target: Square):
            source_piece.capturable.__doc__
            target_piece = self.board[target]

        #   NOTE: Applying method directly to `source_piece` causes infinite recursion.
        #   A more explicit resolution is required.
        #   However, since method is updated for all pieces on the board,
        #   and since each one of them is a strict `Piece` subclass,
        #   we need the actual class name to resolve the redefinition.

            if target_piece is not None:
                return source_piece.__class__.capturable(source_piece, target) \
                    and source_piece.orientation != target_piece.orientation \
                    and target not in self.opponent.checks

            return False

    #   This update is only necessary for the kings:
        self.current.king.deployable = MethodType(king_deployable, self.current.king)
        self.current.king.capturable = MethodType(king_capturable, self.current.king)

    def turn(self):
        """Advance the turn."""
        self.board.flip()

        self.current, self.opponent = self.opponent, self.current
