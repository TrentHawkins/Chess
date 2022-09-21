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
"""

from dataclasses import dataclass
from enum import IntEnum
from itertools import combinations
from typing import ClassVar, Optional

from .square import Square, Vector


class Orientation(IntEnum):
    """Annotate direction on the board with the corresponding color."""

    white = -1
    black = +1


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

    def __init__(self, color: str, square: Optional[Square] = None):
        f"""Give a {self.__class__.__name__} a color and a square.

        Args:
            color_name: Either "white" or "black"
            square: Location on a board (which board is irrelevant).
        """
        self.orientation = Orientation[color]
        self.square = square

    def __repr__(self) -> str:
        f"""Represent a {self.__class__.__name__}.

        Returns:
            The representation of a {self.__class__.__name__}.
        """
        return "\033[8m🨅\033[0m"  # An unspecified piece is a ghost piece.

    def has_friend(self, other):
        """Check weather `other` is a friend of `self`.

        Returns:
            True if `self` and `other` are of the same color.
        """
        return self.orientation == other.orientation if self and other else False

    def has_foe(self, other):
        """Check weather `other` is a foe of `self`.

        Returns:
            True if `self` and `other` are of different color.
        """
        return self.orientation != other.orientation if self and other else False

    def deployable(self, target: Square) -> bool:
        """Check if current piece is placeable on target square.

        This method is to be lazily-defined in board, access to current piece data makes it appropriate to sign it in here.
        If this check fails, the capturability check will kick in as a next step.

        Args:
            target: The source square is `self.square` (not necessary).

        Returns:
            Whether piece is placeable on target square.
        """
        return self.square is not None and target is not None  # Make sure you check a piece that is on a board.

    def capturable(self, target: Square) -> bool:
        """Check if piece on target square is capturable by current piece.

        This method is to be lazily-defined in board, access to current piece data makes it appropriate to sign it in here.
        If this check fails... NOTE: Implement special checks.

        Args:
            target: The source square is `self.square` (necessary for cross-checking color).

        Returns:
            Whether piece on target square is capturable by current piece.
        """
        return self.square is not None and target is not None  # Make sure you check a piece that is on a board.

#   NOTE: The king might be prove to be problematic, as it has an extra condition of blocked movement, squares that are checked.
    @property
    def moves(self) -> set[Square]:
        f"""Generate all legal moves a {self.__class__.__name__} can apriori make.

        Args:
            square: Square on which piece is placed.
                Default is no square, in which case displacements are not resolved into squares and generators not unfold.
            condition: A condition that depends on a square, usually a target square.

        Returns:
            2 sets of moves:
                squares: any empty potential square the piece can move to
                targets: any potential square in squares that the piece can target another piece
        """
        return set()  # A ghost piece cannot move or capture.
