"""A game of chess."""


from re import Pattern, compile
from types import MethodType

from .board import Board
from .move import Capture, Move
from .moves.castle import Castle
from .moves.pawn import Jump, Promotion
from .piece import Piece
from .pieces.melee import King, Knight
from .pieces.pawn import Pawn
from .pieces.ranged import Bishop, Queen, Rook
from .player import Player
from .square import Square


class Chess:
    """A chess game."""

    def __init__(self, board: Board = Board(), black: bool = False):
        """Start a chess game.

        Args:
            board: A custom position if desired. If so, you must specify whose move it is.
            black: Whether it's blacks move for a custom position. Ignored for default games.

        Also defines chessboard-context-sensitive rules for evaluating piece legal moves.
        Because king safety constrains movement of other pieces, king moves are defined seperately.
            The king may not come under check willfully.
            At the same time, pieces may not expose the king to a check willfully.
            Finally if king does come under check, no piece moves are allowed other than the ones protecting the king.
        """
        self.board = board

    #   White usually starts first, but this player will alwyas be the current one.
        self.current = Player("Foo", "white", self.board)  # input("Enter player name for white: ")
        self.opponent = Player("Bar", "black", self.board)  # input("Enter player name for black: ")

    #   Switch to blacks turn in  acustom position starting with black.
        if board != Board() and black:
            self.current, self.opponent = self.opponent, self.current

        def king_safe(source_piece: Piece, target: Square):
            """Check if king of current player is safe.

            Check for kings safety after proposed move too.
            This will be used for probiding extra context to both deployability and capturability conditions.

            NOTE: A player's checks rely on the player's pieces' moves, which are affected by what is happening here.
            """
            source = source_piece.square

        #   Check if king is still in danger after the move. If it is not, then the move is legit.
            target_piece, self.board[target], self.board[source] = self.board[target], source_piece, None  # type: ignore
            king_safe = self.current.king.square not in self.opponent.squares
            self.board[source], self.board[target] = source_piece, target_piece  # type: ignore

            return king_safe

        def piece_deployable(source_piece: Piece, target: Square):
            source_piece.deployable.__doc__
            target_piece = self.board[target]

            return source_piece.__class__.deployable(source_piece, target) and target_piece is None \
                and king_safe(source_piece, target)

        def piece_capturable(source_piece: Piece, target: Square):
            source_piece.capturable.__doc__
            target_piece = self.board[target]

            return source_piece.__class__.capturable(source_piece, target) and target_piece is not None \
                and source_piece.orientation != target_piece.orientation \
                and king_safe(source_piece, target)

    #   Update all pieces in the current player's collection.
        for piece in self.current.pieces:
            piece.deployable = MethodType(piece_deployable, piece)
            piece.capturable = MethodType(piece_capturable, piece)

        def castle_is_legal(castle: Castle):
            castle.is_legal.__doc__
            return castle.__class__.is_legal(castle) \
                and castle.middle not in self.opponent.squares \
                and castle.square not in self.opponent.squares

    #   Update current player's castles with check constraints.
        for castle in self.current.castlings:
            castle.is_legal = MethodType(castle_is_legal, castle)

    def turn(self):
        """Advance a turn."""
        print(self.board)  # Lets see the board!
        self.current(self.current.read())  # Make a move tough guy!
        self.current, self.opponent = self.opponent, self.current

    def round(self):
        """Advance a round, which is two turns, one for black and one for white."""
        self.turn()
        self.turn()

    #   Eliminate any ghost pieces after one full round to eliminate any missed en-passants.
        for piece in self.board:
            if type(piece) is Piece:
                del piece
