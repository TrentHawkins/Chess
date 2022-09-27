"""Implement moves as object to tie them to their chess notation and provide with usefull properties.

Notation for moves
    Each move of a piece is indicated by the piece's uppercase letter, plus the coordinate of the destination square.
    For example, Be5 (bishop moves to e5), Nf3 (knight moves to f3).
    For pawn moves, a letter indicating pawn is not used, only the destination square is given.
    For example, c5 (pawn moves to c5).

Captures
    When a piece makes a capture, the multiplication sign "×" is inserted immediately before the destination square.
    For example, Bxe5 (bishop captures the piece on e5).
    When a pawn makes a capture, the file from which the pawn departed is used to identify the pawn.
    For example, exd5 (pawn on the e-file captures the piece on d5).

    En passant captures are indicated by specifying:
    -   the capturing pawn's file of departure,
    -   the "×", and
    -   the destination square (not the square of the captured pawn)

    Some texts, such as the Encyclopaedia of Chess Openings, omit any indication that a capture has been made.
    (For example, Be5 instead of Bxe5; ed6 instead of exd6 or exd6 e.p.)
    When it is unambiguous to do so, a pawn capture is sometimes described by specifying only the files involved (exd or even ed).
    These shortened forms are sometimes called minimal or abbreviated algebraic notation.

Disambiguating moves
    When two (or more) identical pieces can move to the same square,
    the moving piece is uniquely identified by specifying the piece's letter, followed by (in descending order of preference):
    -   the file of departure (if they differ); or
    -   the rank of departure (if the files are the same but the ranks differ); or
    -   both the file and rank of departure (if neither alone is sufficient to identify the piece

    As above, an "x" can be inserted to indicate a capture.

Pawn promotion
    When a pawn promotes, the piece promoted to is indicated at the end of the move notation,
    for example: e8Q (promoting to queen). In standard FIDE notation, no punctuation is used;
    in Portable Game Notation (PGN) and many publications, pawn promotion is indicated by the equals sign (e8=Q).

Castling
    Castling is indicated by the special notations 0-0 (for kingside castling) and 0-0-0 (queenside castling).
    While the FIDE standard [6] is to use the digit zero (0-0 and 0-0-0), PGN uses the uppercase letter O (O-O and O-O-O).

Check
    A move that places the opponent's king in check usually has the symbol "†" appended.

Checkmate
    Checkmate at the completion of moves is represented by the symbol "‡" .

Long algebraic notation
    In long algebraic notation, both the starting and ending squares are specified, for example: e2e4.
    Sometimes these are separated by a hyphen, e.g. Nb1-c3, while captures are indicated by an "×", e.g. Rd3×d7.
    Long algebraic notation takes more space and is no longer commonly used in print; however, it has the advantage of clarity.
    Some books using primarily short algebraic notation use the long notation instead of the short disambiguation forms.

    A form of long algebraic notation (without piece names) is also used by the Universal Chess Interface (UCI) standard,
    which is a common way for graphical chess programs to communicate with chess engines (e.g., for AI).
"""

from dataclasses import dataclass

from .piece import Piece
from .pieces.melee import King
from .pieces.ranged import Rook
from .square import Square


@dataclass(repr=False)
class Move:
    """Encapsulate all the data needed for a move in chess.

    Each move of a piece is indicated by the piece's uppercase letter, plus the coordinate of the destination square.
    For example, Be5 (bishop moves to e5), Nf3 (knight moves to f3).
    For pawn moves, a letter indicating pawn is not used, only the destination square is given.
    For example, c5 (pawn moves to c5).

    In long algebraic notation, both the starting and ending squares are specified, for example: e2e4.
    Sometimes these are separated by a hyphen, e.g. Nb1-c3, while captures are indicated by an "×", e.g. Rd3×d7.

    Subclasses will specialize the kind of move to be made:
    -   Capture: The most dominant subtype of `Move`, which has a different alebraic notation.
    -   EnPassant: The special pawn rule on capturing evading enemy pawns.
    -   Promotion: The special pawn rule on promoting terminating pawns to other pieces.
    -   Castle: The castling of king and rook.
    -   Check: The king being checked.
    -   Checkmate: The king being checkmated.

    Attributes:
        piece: The piece to be moved.
        square: The square to move said piece.

    Methods:
        is_legal: Check if move is legal based on piece and square context.
    """

    piece: Piece
    square: Square

    def __post_init__(self):
        """Recode square in notation to a `Square` object."""
        self.square = Square(self.square)

    def __repr__(self):
        """Each move of a piece is indicated by the piece's uppercase letter, plus the coordinate of the destination square.

        For example, Be5 (bishop moves to e5), Nf3 (knight moves to f3).
        For pawn moves, a letter indicating pawn is not used, only the destination square is given.
        For example, c5 (pawn moves to c5).

        NOTE: This needs contextual resolve at `Board` or `Player` level. For now use long algebraic notation.
        """
        return self.piece._repr + repr(self.piece.square) + "-" + repr(self.square)

    def is_legal(self):
        """Check if move is legal based on piece and square context."""
        return self.piece.deployable(self.square)  # type: ignore


@dataclass(repr=False)
class Capture(Move):
    """Encapsulate all the data needed for a capture in chess.

    When a piece makes a capture, the multiplication sign "×" is inserted immediately before the destination square.
    For example, Bxe5 (bishop captures the piece on e5).
    When a pawn makes a capture, the file from which the pawn departed is used to identify the pawn.
    For example, exd5 (pawn on the e-file captures the piece on d5).

    En passant captures are indicated by specifying:
    -   the capturing pawn's file of departure,
    -   the "×", and
    -   the destination square (not the square of the captured pawn)

    In long algebraic notation, both the starting and ending squares are specified, for example: e2e4.
    Sometimes these are separated by a hyphen, e.g. Nb1-c3, while captures are indicated by an "×", e.g. Rd3×d7.
    """

    def __repr__(self):
        """Each move of a piece is indicated by the piece's uppercase letter, plus the coordinate of the destination square.

        For example, Be5 (bishop moves to e5), Nf3 (knight moves to f3).
        For pawn moves, a letter indicating pawn is not used, only the destination square is given.
        For example, c5 (pawn moves to c5).

        NOTE: This needs contextual resolve at `Board` or `Player` level. For now use long algebraic notation.
        """
        return super().__repr__().replace("-", "×")

    def is_legal(self):
        """Check if move is legal based on piece and square context."""
        return self.piece.capturable(self.square)  # type: ignore
