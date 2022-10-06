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
from .ranged import Bishop, Queen, Rook


@dataclass(init=False, repr=False, eq=False)
class Melee(Piece):
    """A close ranged piece:
        - King
        - Knight (has reach)

    For a meeled piece (pawns are special) all squares are target squares.
    """

    def __repr__(self) -> str:
        super().__repr__.__doc__
        return {
            "white": f"\033[37;1m{self.symbol}\033[0m",
            "black": f"\033[30;1m{self.symbol}\033[0m",
        }[self.orientation.name]

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
class Knight(Melee):
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

#   Knight notation:
    letter: ClassVar[str] = "N"
    symbol: ClassVar[str] = "♞"

#   Knight moves:
    steps: ClassVar[set[Vector]] = \
        {diagonal + straight for diagonal, straight in product(Piece.diagonals, Piece.straights)} - Piece.straights


@dataclass(init=False, repr=False, eq=False)
class King(Melee):
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

#   King value is normally infinite, but put is as the maximum possible player value with 9 Queens instead of pawns +1:
    value: int = (8 + 1) * Queen.value + 2 * (Knight.value + Bishop.value + Rook.value) + 1  # 104

#   King notation:
    letter: ClassVar[str] = "K"
    symbol: ClassVar[str] = "♚"

#   King moves:
    steps: ClassVar[set[Vector]] = Piece.straights | Piece.diagonals

#   Castles (key: king move, value: corresponding rook relative position):
    short = Vector(0, +2)
    other = Vector(0, -2)

    castles: ClassVar[dict[Vector, Vector]] = {
        short: Vector(0, +3),
        other: Vector(0, -4),
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
