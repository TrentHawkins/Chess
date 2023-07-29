"""A game of chess."""


from datetime import datetime
from itertools import cycle, zip_longest
from shutil import get_terminal_size
from types import MethodType
from typing import TextIO

from .board import Board
from .piece import Piece
from .pieces.melee import King
from .pieces.pawn import Pawn
from .pieces.ranged import Rook
from .player import Player, post_game_prompt
from .square import Square


class Chess:
    """A chess game.

    Attributes:
        board: The board to play the game on.
        current: The player whose turn it is.
        opponent: The other player.
    """

    def __init__(
        self,
        game_file: str | None = None,
        white: str | None = None,
        black: str | None = None,
        board: Board | None = None,
        reversed: bool = False
    ):
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
        self.game: TextIO | None = open(game_file) if game_file is not None else None

    #   A custom or default board for the game.
        self.board: Board = board or Board()

    #   White usually starts first, but this player will always be the current one.
        self.current: Player = Player("white", self.board, name=white)
        self.opponent: Player = Player("black", self.board, name=black)

    #   Keep track of who is black and white:
        self.white: Player = self.current
        self.black: Player = self.opponent

    #   Game termination flags:
        self.agreement: bool = False
        self.draw: bool = False
        self.termination: bool = False

    #   Each piece has moved in a custom position, except for pawn whose immovability can be discerned by their movement entropy.
        if board is not None:
            for piece in self.board:
                if type(piece) is not Pawn:
                    piece.has_moved = True

        #   Switch to blacks turn in a custom position starting with black.
            if reversed:
                self.board.flipped = True
                self.current, self.opponent = self.opponent, self.current

    #   Three dots graphic:
        self.dots = cycle("." * times for times in range(19))

    #   Clear entire screen after procceding.
        print("\033[H\033[J")

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

        representation += f" CHESS {datetime.today().replace(microsecond=0)} \n"
        representation += f"{self.board}\033[s\n"  # Lets see the board!

    #   Check winning conditions before draw conditions, as some as subset to winning conditions.
    #   For example, stalemate is always true for checkmate, so it must be checked last.
        if self.termination:
            if self.draw:
                representation += " Game drawn"

                if self.agreement:
                    representation += " by agreement!"

                elif self.current.stalemate:
                    representation += " by stalemate!"

            else:
                representation += f" {self.current.name} won"

                if self.opponent.resignation:
                    representation += f" by resignation!"

                elif self.current.checkmate:
                    representation += f" by checkmate!"

    #   else:
    #       representation += f" Loading{next(self.dots)}"

    #   Clear the line in case there are player move prompt left-overs:
        representation += f"\033[K\n"
        representation += "┌─────────┬───────────────┐\n"

    #   Get material differences:
        self.white.material_difference = self.white.material - self.black.material
        self.black.material_difference = self.black.material - self.white.material

    #   Print captures pieces and material differences for both players:
        representation += f"{self.white}\n"
        representation += f"{self.black}\n"

        representation += "└─────────┴───────────────┘\n"
        representation += f"  ###   {self.white.name:7s}   {self.black.name:7s}  \n"
        representation += "┌─────╥─────────┬─────────┐\n"

    #   History display buffer: shows 32 last moves, meaning it forgets the past.
        buffer: int = get_terminal_size().lines - 26
        offset = max(len(self.white.history) - buffer, 0)

    #   Running move history starts here:
        for round, (white, black) in enumerate(
            list(
                zip_longest(
                    self.white.history,
                    self.black.history,
                )
            )[-buffer:]
        ):
            if black is not None:
                representation += f"│ {round + offset + 1:03d} ║ {str(white):18s} │ {str(black):18s} │\n"

            else:
                representation += f"│ {round + offset + 1:03d} ║ {str(white):18s} │         │\n"

    #   The end:
        representation += "└─────╨─────────┴─────────┘\n\033[u"

        return representation

    def update(self):
        """Define game-context-sensitive rules for evaluating piece legal moves.

        This affects current player who needs opponent info to make decisions about movement legallity.
        """

        def piece_king_saved(source_piece: Piece, target: Square):
            """Check if king of current player is safe.

            Check for king's safety after proposed move.
            This will be used for probiding extra context to both deployability and capturability conditions.
            """
            source = source_piece.square

        #   Check if current king is in danger after the move. If it is not, then the move is legit.
            if source is not None:
                self.board[source], self.board[target], target_piece = None, source_piece, self.board[target]
                king_safe = self.current.king.square not in self.opponent.squares()
                self.board[target], self.board[source] = target_piece, source_piece

        #   King is not threatened by captured pieces.
            else:
                king_safe = True

            return king_safe

        def piece_deployable(source_piece: Piece, target: Square):
            f"""{source_piece.deployable.__doc__}"""
            target_piece = self.board[target] if target is not None else None

            is_empty = target_piece is None or type(target_piece) is Piece

            return source_piece.__class__.deployable(source_piece, target) and is_empty

        def piece_capturable(source_piece: Piece, target: Square):
            f"""{source_piece.capturable.__doc__}"""
            target_piece = self.board[target] if target is not None else None

            is_not_empty = target_piece is not None and type(target_piece) is not Piece \
                and source_piece.orientation != target_piece.orientation

            return source_piece.__class__.capturable(source_piece, target) and is_not_empty

        def pawn_capturable(source_piece: Pawn, target: Square):
            f"""{source_piece.capturable.__doc__}"""
            target_piece = self.board[target] if target is not None else None

            is_not_empty = target_piece is not None \
                and source_piece.orientation != target_piece.orientation

            return source_piece.__class__.capturable(source_piece, target) and is_not_empty

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
            piece.king_saved = MethodType(piece_king_saved, piece)
            piece.deployable = MethodType(piece_deployable, piece)

            if type(piece) is Pawn:
                piece.capturable = MethodType(pawn_capturable, piece)

            else:
                piece.capturable = MethodType(piece_capturable, piece)

    #   Defining both castleabilities does not create an infinite recursion.
        self.current.king.castleable = MethodType(king_castleable, self.current.king)

    #   Set opponent's basic rules too:
        self.opponent.update()

    def terminate(self) -> bool:
        """Terminate game based on its state and each of the player states:

        Draw by:
        -   mutual agreement
        -   three-fold movement repetition
            FIXME: For now players have to mutually agree to a draw if this happens.
        -   stalemate

        Termination by:
        -   reisgnation
        -   checkmate

        Returns:
            Global game termination condition.
        """
        self.current.king.in_check = self.current.king.square in self.opponent.squares()

    #   Reset draw offers only for current player (to give the chance to opponent player to respond).
        self.agreement = self.current.draw and self.opponent.draw
        self.current.draw = False

    #   Set stalemate and checkmate conditions in one place as the relate and need to sync-up.
        self.current.stalemate = self.current.squares() == set()
        self.current.checkmate = self.current.stalemate and self.current.king.in_check

    #   HACK: Edit last move as a check move, if no other modifier is added.
        if self.current.king.in_check and not (self.current.draw or self.opponent.resignation):
            self.opponent.history[-1].representation += "†"

    #   The final game termination decision compliled:
        self.draw = (self.current.stalemate and not self.current.checkmate) or self.agreement
        self.termination = self.current.checkmate or self.opponent.resignation or self.draw

    #   HACK: Edit last move as a checkmate move, if it was annotated as a check move first, else leave as is.
        if self.current.checkmate:
            self.opponent.history[-1].representation = self.opponent.history[-1].representation.replace("†", "‡")

        return self.termination

    def turn(self):
        """Advance a turn.

        Stages of a turn are:
        -   Update context for both players:
            -   Augment current player's context with king safety,
            -   Strip opponent player of king safety controls
        -   Check termination conditions:
            -   Draw,
                -   Mutual agreement,
                -   Stalemate.
            -   Resignation,
            -   Checkmate.
        -   Print:
            -   Board state,
            -   Both player states:
                -   Captured pieces,
                -   Material difference.
            -   Game movement history (buffered).
        -   Eliminate all outlived ghost pieces (en-passant).
        -   Flip roles, current player becomes opponent and vice versa.
        """
        self.update()
        self.terminate()

        print(self)

    #   Attempt to terminate game, before any more moves are input:
        if self.termination:
            post_game_prompt()
            return

    #   Make a move tough guy!
        move = self.current.read(self.game)

    #   If move terminates game, exit the game:
        if move is None:
            self.termination = True
            return

    #   Make the move!
        self.current(move)

    #   Age pieces by one turn (included freshly created ghosts).
        for piece in self.board:
            piece.life += 1

        #   Eliminate any out-lived ghost pieces (2 turns).
            if type(piece) is Piece and piece.square is not None and piece.life > 1:
                del self.board[piece.square]

    #   Prepare for the next turn:
    #   self.board.flipped = not self.board.flipped

    #   Flip player identities, making the next turn invokation proper!
        self.current, self.opponent = self.opponent, self.current
