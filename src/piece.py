"""Implements the chess pieces that are placed in a chessboard.

Chess has 6 types of pieces with predifined rules of movement and worth in-game:
    Pawn: Moves one step forward, unless first move, where it may move two squares forward.
        Captures diagonally. Can en-pasant. Can be promoted to a higher value piece at the end of a player's board. Worth 1.
    Bishop: Moves along diagonals. Worth 3. WOrth 3+ when in pairs of two or in an open game.
    Knights: Moves 2 squares in one directions and 1 in a vertical to that direction).
        Can jump over other pieces. Worth 3. Worth 3+ in closed games.
    Rook: Moves along ranks and files. Worth 5.
    Queen: Moves both like a rook and bishop. Worth 9.
    King: Moves one square in any direction. Worth N/A (you loose the king it's game over).

Naming the pieces
    This section contains chess piece figurines.
    Without proper rendering support, you may see question marks, boxes, or other symbols.
    Each piece type (other than pawns) is identified by an uppercase letter.
    English-speaking players use the letters:
    -   K for king,
    -   Q for queen,
    -   R for rook,
    -   B for bishop, and
    -   N for knight (since K is already used and is a silent letter in knight).

    In both standard algebraic notation and FAN, pawns are not identified by a letter or symbol, but rather by the absence of one.

    Different initial letters are used by other languages.
    In chess literature, especially that intended for an international audience,
    the language-specific letters are often replaced by universally recognized piece symbols; for example, ♞c6 in place of Nc6.
    This style is known as Figurine Algebraic Notation (FAN).
    The Unicode Miscellaneous Symbols set includes all the symbols necessary for FAN.

    In both standard algebraic notation and FAN, pawns are not identified by a letter or symbol,but rather by the absence of one.
"""


from dataclasses import dataclass
from enum import IntEnum
from itertools import combinations
from typing import ClassVar

from .square import Square, Vector


class Orientation(IntEnum):
    """Annotate direction on the board with the corresponding color."""

    white = -1  # Array indexing goes down the board, but white goes up.
    black = +1  # Array indexing goes down the board, and so does black.

    def __pos__(self):
        return self

    def __neg__(self):
        return self.__class__["white"] if self.name == "black" else self.__class__["black"]


@dataclass(init=False, repr=False)
class Piece:
    """A generic chess piece.

    Class Attributes:
        value: How much a piece is worth:
            1: Pawn
            3: Knight/Bishop
            5: Rook
            9: Queen
            ∞: King
        steps: Default move patterns characteristic for each piece.

    Attributes:
        orientation: One of two colors, black or white. Holds direction respective to the board.
        square: Where on (any) board is it (as far as rules go).

    A few generic rules applied to all pieces:
        Pinning: If moving a piece will discover a check on your king, the piece is pinned and cannot move.
        If your king is checked, no other piece can move except for the ones and with only the moves that resolve the check.

    Straight steps:
        ↑ north
        ← west
        ↓ south
        → east

    Diagonal steps (via combinations of straight steps):
        → + ← = · center (removed)
        → + ↑ = ↗ north-east
        → + ↓ = ↘ south-east
        ← + ↑ = ↖ north-west
        ← + ↓ = ↙ south-west
        ↑ + ↓ = · center (removed)
    """

#   Piece letter range:
    piece_range: ClassVar[str] = "BKNQR"

#   Piece value is None:
    value: ClassVar[int] = 0

#   Piece Notation:
    symbol: ClassVar[str] = "🨅"  # This will be ghosted so that empty space has the right width.

#   Straight steps:
    straights: ClassVar[set[Vector]] = {
        Vector(-1, 0),
        Vector(0, -1),
        Vector(+1, 0),
        Vector(0, +1),
    }

#   Diagonal steps:
    diagonals: ClassVar[set[Vector]] = \
        {straight0 + straight1 for straight0, straight1 in combinations(straights, 2)} - {Vector(0, 0)}

    steps: ClassVar[set[Vector]] = set()

    def __init__(self, orientation: Orientation | str, square: Square | str | None = None):
        f"""Give a {self.__class__.__name__} a color and a square.

        Args:
            orientation: Either "white" or "black"
            square: Location on a board (which board is irrelevant).
        """
        self.orientation: Orientation = Orientation[orientation] if isinstance(orientation, str) else orientation
        self.square: Square | None = Square(square) if square is not None else None

        self.life: int = 0  # The lifetime of a piece on the board in terms of game turns.
        self.has_moved: bool = False  # Has not moved upon creation.

    def __repr__(self) -> str:
        f"""Represent a {self.__class__.__name__}.

        Returns:
            The representation of a {self.__class__.__name__}.
        """
        return f"\033[8m{self.symbol}\033[0m"  # An unspecified piece is a ghost piece.

    def __hash__(self):
        """Make each piece distinct based on its type square alone.

        That means that pieces outside the board will still be distinct by type.
        That is no issue as the only thing we need of pieces outside the board is to count them by type.

        NOTE: Do not mix pieces that are on different boards.

        Returns:
            The square the piece is designated to.
        """

        return hash((self.__class__.__name__, self.square))

    def __call__(self, target: Square | str):
        """Move the piece to a target square.

        Simply updates the piece's square and movement flag.

        Args:
            target: The square in notation the piece wants to go to.

        Returns:
            The piece moved.

        NOTE: A `Move` class will be made to encapsulate moves, this will be moved there.
        """
        if target is not None:  # If target square is given
            target = Square(target)

        self.square = target  # Update the piece's square.
        self.has_moved = True  # The pawns at their start and kings and rooks for castling use this flag.

        return self

    def king_saved(self, square: Square) -> bool:
        """Check if king of current player is safe.

        Check for king's safety after proposed move.
        This will be used for probiding extra context to both deployability and capturability conditions.
        This method will require simulating the proposed move to check if it passes for king safety.

        Args:
            square: The source square is `self.square` (not necessary).

        Returns:
            Whether king of current player is safe.
        """
        return True  # The king is apriory safe.

    def deployable(self, square: Square) -> bool:
        """Check if current piece is placeable on target square.

        This method will be updated by both player and game context (whenever opponent info is needed),
        to account for king safety and obstacles (friendly pieces).

        Args:
            square: The source square is `self.square` (not necessary).

        Returns:
            Whether piece is placeable on target square.
        """
        return self.square is not None and square is not None  # Make sure piece and square are on a board.

    def capturable(self, square: Square) -> bool:
        """Check if piece on target square is capturable by current piece.

        This method will be updated by both player and game context (whenever opponent info is needed),
        to account for king safety and opponent pieces (targets).

        Args:
            square: The source square is `self.square` (necessary for cross-checking color).

        Returns:
            Whether piece on target square is capturable by current piece.
        """
        return self.square is not None and square is not None  # Make sure piece and square are on a board.

    def squares(self) -> set[Square]:
        f"""Generate all legal moves a {self.__class__.__name__} can apriori make.

        Args:
            square: Square on which piece is placed.
                Default is no square, in which case displacements are not resolved into squares and generators not unfold.
            condition: A condition that depends on a square, usually a target square.

        Returns:
            squares: any empty potential square the piece can move to
            targets: any potential square in squares that the piece can target another piece
        """
        return set()  # A ghost piece cannot move or capture.
