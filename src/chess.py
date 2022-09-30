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

    def __init__(self, board: Board | None = None, black: bool = False):
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
        self.board = board or Board()

    #   Make room for the boarf before the game starts:
        for _ in range(15):
            print()  # empty line

    #   White usually starts first, but this player will always be the current one.
        self.current = Player("Foo", "white", self.board)  # input("Enter player name for white: ")
        self.opponent = Player("Bar", "black", self.board)  # input("Enter player name for black: ")

    #   Each piece has moved in a custom position, except for pawn whose immovability can be discerned by their movement entropy.
        if board is not None:
            for piece in self.board:
                if type(piece) is not Pawn:
                    piece.has_moved = True

        #   Switch to blacks turn in  acustom position starting with black.
            if black:
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

        def king_castleable(king: King, target: Square):
            king.castleable.__doc__
            castle = target - king.square
            middle = king.square + castle // 2  # type: ignore

        #   Escorting rook:
            rook = self.board[king.square + king.castles[castle]]  # type: ignore

        #   Mind that king cannot escape check with a castle, as it usually can by moving otherwise.
            return type(rook) is Rook and rook.castleable(middle) \
                and self.current.king.square not in self.opponent.squares and king.__class__.castleable(king, target)

        self.current.king.castleable = MethodType(king_castleable, self.current.king)

    def turn(self):
        """Advance a turn."""
        print(self.board)  # Lets see the board!
        print()  # empty line

        self.current(self.current.read())  # Make a move tough guy!

    #   Age pieces by one turn (included freshly created ghosts).
        for piece in self.board:
            piece.life += 1

        #   Eliminate any out-lived ghost pieces (2 turns).
            if type(piece) is Piece and piece.life > 1:
                del self.board[piece.square]  # type: ignore

        self.current, self.opponent = self.opponent, self.current

    def round(self):
        """Advance a round, which is two turns, one for black and one for white."""
        self.turn()
        self.turn()
