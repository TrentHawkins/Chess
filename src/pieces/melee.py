"""Implements the chess pieces that are placed in a chessboard.

Of the 6 type of chess pieces the following are melee units:
    Knights: Moves 2 squares in one directions and 1 in a vertical to that direction).
        Can jump over other pieces. Worth 3. Worth 3+ in closed games.
    King: Moves one square in any direction. Worth N/A (you loose the king it's game over).

Remember pawns are kind of special.
"""

from dataclasses import dataclass
from itertools import product
from typing import ClassVar

from ..piece import Piece
from ..square import Square, Vector


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

    in_check: bool = False

    def __repr__(self) -> str:
        super().__repr__.__doc__
        return {
            "white": f"\033[37;1m{self._repr}\033[0m",
            "black": f"\033[30;1m{self._repr}\033[0m",
        }[self.orientation.name]


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

    def __repr__(self) -> str:
        super().__repr__.__doc__
        return {
            "white": f"\033[37;1m{self._repr}\033[0m",
            "black": f"\033[30;1m{self._repr}\033[0m",
        }[self.orientation.name]
