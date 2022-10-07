"""A game of chess."""

from datetime import datetime
from itertools import zip_longest
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

        self.board: Board = board or Board()

    #   White usually starts first, but this player will always be the current one.
        self.current: Player = Player("Foo", "white", self.board)  # input("Enter player name for white: ")
        self.opponent: Player = Player("Bar", "black", self.board)  # input("Enter player name for black: ")

    #   Keep track of who is black and white:
        self.white: Player = self.current
        self.black: Player = self.opponent

    #   Game termination flags:
        self.agreement: bool = False
        self.draw: bool = False
        self.gameover: bool = False

    #   Each piece has moved in a custom position, except for pawn whose immovability can be discerned by their movement entropy.
        if board is not None:
            for piece in self.board:
                if type(piece) is not Pawn:
                    piece.has_moved = True

        #   Switch to blacks turn in a custom position starting with black.
            if black:
                self.board.flipped = True
                self.current, self.opponent = self.opponent, self.current

    def __repr__(self):
        """ Representation of a game.

        Includes:
        -   a game header (with a running datetime),
        -   the board (state),
        -   the prompt for current player to input a move
        -   a run down of captured material for both players
        -   a side-by-side running move history of both players
        """
        representation = "\033[H"  # Reset printing head.

        representation += f"CHESS {datetime.today().replace(microsecond=0)}\n"
        representation += "═════════════════════════\n"
        representation += f"{self.board}\n"  # Lets see the board!
        representation += "═════════════════════════\n"

        if self.gameover:
            if self.draw:
                representation += " Game draw"

                if self.agreement:
                    representation += " by agreement"

                representation += "!\033[K"

        #   Checks verify a losing player therefore, but then roles are flipped at the end of the turn.
            elif self.current.victory:
                representation += f" {self.current.name} won"

                if self.opponent.resignation:
                    representation += f" by resignation"

                representation += f"!\033[K"

        representation += "\n"
        representation += "─────────┬───────────────\n"

    #   Get material differences:
        self.white.material -= self.black.material
        self.black.material -= self.white.material - self.black.material

        representation += f"{self.white}\n"
        representation += f"{self.black}\n"

        representation += "─────────┴───────────────\n"
        representation += f" ###   {self.white.name:7s}   {self.black.name:7s} \n"
        representation += "─────╥─────────┬─────────\n"

        for round, (white, black) in enumerate(zip_longest(self.white.history, self.black.history)):
            representation += f" {round+1:03d} ║ {str(white):18s} │ {str(black) if black is not None else '':18s} \n"

        return representation

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
            self.board[source], self.board[target], target_piece = None, source_piece, self.board[target]  # type: ignore
            king_safe = self.current.king.square not in self.opponent.squares()
            self.board[target], self.board[source] = target_piece, source_piece  # type: ignore

            return king_safe

        def piece_deployable(source_piece: Piece, target: Square):
            f"""{source_piece.deployable.__doc__}"""
            target_piece = self.board[target] if target is not None else None

            is_empty = target_piece is None or type(target_piece) is Piece

            return source_piece.__class__.deployable(source_piece, target) and is_empty and \
                king_safe(source_piece, target)

        def piece_capturable(source_piece: Piece, target: Square):
            f"""{source_piece.capturable.__doc__}"""
            target_piece = self.board[target] if target is not None else None

            is_not_empty = target_piece is not None and type(target_piece) is not Piece \
                and source_piece.orientation != target_piece.orientation

            return source_piece.__class__.capturable(source_piece, target) and is_not_empty and \
                king_safe(source_piece, target)

        def pawn_capturable(source_piece: Pawn, target: Square):
            f"""{source_piece.capturable.__doc__}"""
            target_piece = self.board[target] if target is not None else None

            is_not_empty = target_piece is not None \
                and source_piece.orientation != target_piece.orientation

            return source_piece.__class__.capturable(source_piece, target) and is_not_empty and \
                king_safe(source_piece, target)

        def king_castleable(current_king: King, target: Square):
            f"""{current_king.castleable.__doc__}"""

        #   Cascade the checks to save power:
            if current_king.__class__.castleable(current_king, target):  # Check basics first to save power
                castle = target - current_king.square  # Target square is assumed legit
                middle = current_king.square + castle // 2  # type: ignore
                current_rook = self.board[current_king.square + current_king.castles[castle]]  # type: ignore

                if type(current_rook) is Rook and current_rook.__class__.castleable(current_rook, middle):
                    return self.current.king.square not in self.opponent.squares()  # The king is safe.

            else:
                return False

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
        self.update()

    #   Reset draw offers only for current player (to give the chance to opponent player to respond).
        self.current.draw = False

    #   Update players first with game-context before printing!
        print(self)

    #   Make a move tough guy!
        move = self.current.read()
        self.current(move)

    #   Age pieces by one turn (included freshly created ghosts).
        for piece in self.board:
            piece.life += 1

        #   Eliminate any out-lived ghost pieces (2 turns).
            if type(piece) is Piece and piece.life > 1:
                del self.board[piece.square]  # type: ignore

    #   Prepare for the next turn:
    #   self.board.flipped = not self.board.flipped

    #   Set draw flags:
        self.agreement = self.current.draw and self.opponent.draw
        self.draw = self.agreement

    #   Set termination flags:
        self.current.resignation = move.resign
        self.opponent.victory = self.current.resignation
        self.gameover = self.draw or self.opponent.victory

    #   Flip player identities, making the next turn invokation proper!
        self.current, self.opponent = self.opponent, self.current
