"""Implements the chess pieces that are placed in a chessboard.

Of the 6 type of chess pieces the following are melee units:
    Knights: Moves 2 squares in one directions and 1 in a vertical to that direction).
        Can jump over other pieces. Worth 3. Worth 3+ in closed games.
    King: Moves one square in any direction. Worth N/A (you loose the king it's game over).

Remember pawns are kind of special.
"""

from dataclasses import dataclass
from itertools import product
from pickletools import long1
from typing import ClassVar

from ..piece import Piece
from ..square import Square, Vector
from .ranged import Rook


@dataclass(init=False, repr=False, eq=False)
class Meleed(Piece):
    """A close ranged piece:
        - King
        - Knight (has reach)

    For a meeled piece (pawns are special) all squares are target squares.
    """

    @property
    def squares(self) -> set[Square]:
        f"""{super().squares.__doc__}"""
        squares = super().squares

        if self.square is not None:  # If meleed piece is on a board,
            for step in self.steps:  # For all target squares,
                square = self.square + step  # Get target,

                if self.deployable(square) or self.capturable(square):  # If said target is inside board limits,
                    squares.add(square)  # Add said target to meleed piece.

        return squares


@dataclass(init=False, repr=False, eq=False)
class King(Meleed):
    """A King.

    Moves one square in any direction that is not blocked by same side piece or targeted by enemy piece.

    King steps:
        ↑ north
        ← west
        ↓ south
        → east
        ↗ north-east
        ↘ south-east
        ↖ north-west
        ↙ south-west
    """

#   King main attributes:
    _repr: ClassVar[str] = "♚"

#   King moves:
    steps: ClassVar[set[Vector]] = Piece.straights | Piece.diagonals

#   Castles (key: king move, value: corresponding rook relative position):
    castles: ClassVar[dict[Vector, Vector]] = {
        Vector(0, +2): Vector(0, +3),
        Vector(0, -2): Vector(0, -4),
    }

    in_check: bool = False

    def castleable(self, square: Square) -> bool:
        """Check if current king is castlable on either side.

        This method is to be lazily-defined in board, access to current piece data makes it appropriate to sign it in here.
        If this check fails, the capturability check will kick in as a next step.

        This method assumes that the proper squares are checked. This is done in `squares` below, so its safe.
        For now, check that:
        -   the king has not moved
        -   the king can move to the castling square (but only as a move, not a capture)
        -   the king can cross the middle square on the way to the castling square

        Args:
            square: The source square is `self.square` (not necessary).

        Returns:
            Whether piece is placeable on target square.
        """
        return not self.has_moved \
            and self.deployable(square) \
            and self.deployable(square + (square - self.square) // -2)

    @property
    def squares(self) -> set[Square]:
        f"""{super().squares.__doc__}"""
        squares = super().squares

        if self.square is not None:
            for castle in self.castles:
                square = self.square + castle

                if self.castleable(square):
                    squares.add(square)

        return squares


@dataclass(init=False, repr=False, eq=False)
class Knight(Meleed):
    """A knight.

    Moves two squares in any direction and one square in a vertical to that direction as one move.
    It therefore can jump over other pieces. Target square must not be blocked by a same side piece.

    Knight steps (via product of diagonal steps with straigh steps:
        ↗ + ↑ north-north-east
        ↗ + ← = ↑ north (removed)
        ↗ + ↓ = → east (removed)
        ↗ + → north-east-east
        ↘ + ↑ = → east (removed)
        ↘ + ← = ↓ south (removed)
        ↘ + ↓ south-south-east
        ↘ + → south-east-east
        ↖ + ↑ north-north-west
        ↖ + ← north-west-west
        ↖ + ↓ = ← west (removed)
        ↖ + → = ↑ north (removed)
        ↙ + ↑ = ← west (removed)
        ↙ + ← south-west-west
        ↙ + ↓ south-south-west
        ↙ + → = ↓ south (removed)
    """

#   Knight main attributes:
    value: ClassVar[int] = 3
    _repr: ClassVar[str] = "♞"

#   Knight moves:
    steps: ClassVar[set[Vector]] = \
        {diagonal + straight for diagonal, straight in product(Piece.diagonals, Piece.straights)} - Piece.straights
