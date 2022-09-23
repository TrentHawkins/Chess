"""A game of chess."""


from types import MethodType

from .board import Board
from .piece import Piece
from .player import Player
from .square import Square


class Chess:
    """A chess game."""

    def __init__(self, board: Board = Board(), black: bool = False):
        """Start a chess game.

        Args:
            board: A custom position if desired. If so, you must specify whose move it is.

        Also defines chessboard-context-sensitive rules for evaluating piece legal moves.
        Because king safety constrains movement of other pieces, king moves are defined seperately.
            The king may not come under check willfully.
            At the same time, pieces may not expose the king to a check willfully.
            Finally if king does come under check, no piece moves are allowed other than the ones protecting the king.
        """
        self.board = board

    #   White usually starts first, but this player will alwyas be the current one.
        self.current = Player("White", "white", self.board)  # input("Enter player name for white: ")
        self.opponent = Player("Black", "black", self.board)  # input("Enter player name for black: ")

    #   Switch to blacks turn in  acustom position starting with black.
        if board != Board() and black:
            self.turn()

        def king_safe(source_piece: Piece, target: Square):
            """Check if king of current player is safe.

            Check for kings safety after proposed move too.
            This will be used for probiding extra context to both deployability and capturability conditions.

            NOTE: A player's checks rely on the player's pieces' moves, which are affected by what is happening here.
            """
            source = source_piece.square

        #   Check first if king is in danger presently. If it is, there is hope for this move yet, keep reading.
            king_safe = self.current.king.square not in self.opponent.checks

        #   Check if king is still in danger, after the move. If it is not, then the move is legit.
            target_piece, self.board[target], self.board[source] = self.board[target], self.board[source], None  # type: ignore

            king_safe = king_safe and self.current.king.square not in self.opponent.checks

            self.board[source], self.board[target] = self.board[target], target_piece  # type: ignore

            return king_safe

        def piece_deployable(source_piece: Piece, target: Square):
            source_piece.deployable.__doc__
            target_piece = self.board[target]

        #   Avoid ckecking for king safety in unecessary scenarios.
            if source_piece.__class__.deployable(source_piece, target) and target_piece is None:
                return king_safe(source_piece, target)

            return False

        def piece_capturable(source_piece: Piece, target: Square):
            source_piece.capturable.__doc__
            target_piece = self.board[target]

        #   Avoid ckecking for king safety in unecessary scenarios.
            if source_piece.__class__.capturable(source_piece, target) and target_piece is not None \
                    and source_piece.orientation != target_piece.orientation:
                return king_safe(source_piece, target)

            return False

        for piece in self.current.pieces:
            piece.deployable = MethodType(piece_deployable, piece)
            piece.capturable = MethodType(piece_capturable, piece)

    def turn(self):
        """Advance the turn."""
        self.current, self.opponent = self.opponent, self.current
