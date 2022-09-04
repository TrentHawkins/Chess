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


@dataclass(init=False, repr=False)
class Meleed(Piece):
    """A close ranged piece:
        - King
        - Knight (has reach)

    For a meeled piece (pawns are special) all squares are target squares.
    """

    def moves(self) -> tuple[set[Square], set[Square]]:
        f"""{super().moves.__doc__}"""
        squares, targets = super().moves()

        if self.square is not None:  # If meleed piece is on a board,
            for step in self.steps:  # For all target squares,
                target = self.square + step  # Get target,

                if target is not None and self.condition(target):  # If said target is inside board limits,
                    targets.add(target)  # Add said target to meleed piece.

        return squares, targets


@dataclass(init=False, repr=False)
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

#   King moves:
    steps: ClassVar[set[Vector]] = Piece.straights | Piece.diagonals

    def __repr__(self) -> str:
        f"""{super().__repr__.__doc__}"""
        return {
            "white": "♔",
            "black": "♚",
        }[self.orientation.name]


@dataclass(init=False, repr=False)
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

#   Knight value:
    value: ClassVar[int] = 3

#   Knight moves:
    steps: ClassVar[set[Vector]] = \
        {diagonal + straight for diagonal, straight in product(Piece.diagonals, Piece.straights)} - Piece.straights

    def __repr__(self) -> str:
        f"""{super().__repr__.__doc__}"""
        return {
            "white": "♘",
            "black": "♞",
        }[self.orientation.name]
