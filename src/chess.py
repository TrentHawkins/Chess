"""A game of chess."""

from datetime import datetime
from itertools import compress, tee, zip_longest
from types import MethodType
from typing import Iterable

from .board import Board
from .move import Move
from .piece import Piece
from .pieces.melee import King
from .pieces.pawn import Pawn
from .pieces.ranged import Rook
from .player import Player
from .square import Square


class Chess:
    """A chess game.

    Attributes:
        board: The board to play the game on.
        current: The player whose turn it is.
        opponent: The other player.
    """

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
        print("\033[H\033[J")  # Clear entire screen before procceding.
        print(f"CHESS {datetime.today().replace(microsecond=0)}")
        print("═════════════════════════")

        self.board: Board = board or Board()

    #   White usually starts first, but this player will always be the current one.
        self.current: Player = Player("Foo", "white", self.board)  # input("Enter player name for white: ")
        self.opponent: Player = Player("Bar", "black", self.board)  # input("Enter player name for black: ")

    #   Keep track of who is black and white:
        self.white: Player = self.current
        self.black: Player = self.opponent

    #   Round counter:
        self.round_index: int = 0

    #   Each piece has moved in a custom position, except for pawn whose immovability can be discerned by their movement entropy.
        if board is not None:
            for piece in self.board:
                if type(piece) is not Pawn:
                    piece.has_moved = True

        #   Switch to blacks turn in a custom position starting with black.
            if black:
                self.board.flipped = True
                self.current, self.opponent = self.opponent, self.current

    def update(self):
        """Define game-context-sensitive rules for evaluating piece legal moves.

        This affects current player who needs opponent info to make decisions about movement legallity.
        """

        def king_safe(source_piece: Piece, target: Square):
            """Check if king of current player is safe.

            Check for king's safety after proposed move.
            This will be used for probiding extra context to both deployability and capturability conditions.
            """
            source = source_piece.square

        #   Check if current king is in danger after the move. If it is not, then the move is legit.
            target_piece, self.board[target], self.board[source] = self.board[target], source_piece, None  # type: ignore
            king_safe = self.current.king.square not in self.opponent.squares
            self.board[source], self.board[target] = source_piece, target_piece  # type: ignore

            return king_safe

        def piece_deployable(source_piece: Piece, target: Square):
            source_piece.deployable.__doc__
            target_piece = self.board[target]

            is_empty = target_piece is None or type(target_piece) is Piece

            return Piece.deployable(source_piece, target) and is_empty and \
                king_safe(source_piece, target)

        def piece_capturable(source_piece: Piece, target: Square):
            source_piece.capturable.__doc__
            target_piece = self.board[target]

            is_not_empty = target_piece is not None and type(target_piece) is not Piece \
                and source_piece.orientation != target_piece.orientation

            return Piece.capturable(source_piece, target) and is_not_empty and \
                king_safe(source_piece, target)

        def pawn_capturable(source_piece: Pawn, target: Square):
            source_piece.capturable.__doc__
            target_piece = self.board[target]

            is_not_empty = target_piece is not None \
                and source_piece.orientation != target_piece.orientation

            return Pawn.capturable(source_piece, target) and is_not_empty and \
                king_safe(source_piece, target)

        def king_castleable(player_king: King, target: Square):
            player_king.castleable.__doc__
            castle = target - player_king.square
            middle = player_king.square + castle // 2  # type: ignore

        #   Escorting rook:
            rook = self.board[player_king.square + player_king.castles[castle]]  # type: ignore

        #   Mind that king cannot escape check with a castle, as it usually can by moving otherwise.
            return King.castleable(player_king, target) and self.current.king.square not in self.opponent.squares \
                and type(rook) is Rook and Rook.castleable(rook, middle)

    #   Update all pieces in the current player's collection.
        for piece in self.current.pieces:
            piece.deployable = MethodType(piece_deployable, piece)

            if type(piece) is Pawn:
                piece.capturable = MethodType(pawn_capturable, piece)

            else:
                piece.capturable = MethodType(piece_capturable, piece)

    #   Defining both castleabilities does not create an infinite recursion.
        self.current.king.castleable = MethodType(king_castleable, self.current.king)

    #   Set opponent's basic rules too:
        self.opponent.update()

    def turn(self):
        """Advance a turn."""
        print("\033[H\033[2B")  # Reset printing head.

    #   Print the current game state:
        print(self.board)  # Lets see the board!
        print()

        self.update()  # Update players first with game-context!
        move = self.current.read()  # Make a move tough guy!

    #   Print current history of moves:
        print()
        print(f" ###   {self.white.name:7s}   {self.black.name:7s} ")
        print("─────╥─────────┬─────────")

        for round, (white, black) in enumerate(zip_longest(self.white.history, self.black.history)):
            print(f" {round+1:03d} ║ {str(white):18s} │ {str(black) if black is not None else '':18s} ")

        self.current(move)

    #   Age pieces by one turn (included freshly created ghosts).
        for piece in self.board:
            piece.life += 1

        #   Eliminate any out-lived ghost pieces (2 turns).
            if type(piece) is Piece and piece.life > 1:
                del self.board[piece.square]  # type: ignore

    #   Prepare for the next turn:
    #   self.board.flipped = not self.board.flipped

    #   Flip player identities, making the next turn invokation proper!
        self.current, self.opponent = self.opponent, self.current

    def round(self):
        """Advance a round, which is two turns, one for black and one for white."""
        self.round_index += 1

        self.turn()
        self.turn()
