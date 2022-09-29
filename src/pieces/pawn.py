"""Implements the chess pieces that are placed in a chessboard.

Of the 6 type of chess pieces pawns are special:
    Pawn: Moves one step forward, unless first move, where it may move two squares forward.
        Captures diagonally. Can en-pasant. Can be promoted to a higher value piece at the end of a player's board. Worth 1.
"""

from dataclasses import dataclass
from typing import ClassVar, Type

from ..piece import Piece
from ..square import Square, Vector
from .melee import Knight
from .ranged import Bishop, Queen, Rook

Officer: Type = Bishop | Knight | Queen | Rook


@dataclass(init=False, repr=False, eq=False)
class Pawn(Piece):
    """A Pawn.

    Moves forward a square, unless its first move where it can move two and unless blocked by any piece.
    It captured forward-diagonally. I can capture en-passant:
        If an enemy pawn passes yours trying to escape capture, well... it cannot, not for this round.

    Upon reaching the end of the board, it is promoted to an officer:
        - Rook
        - Bishop
        - Knight
        - Queen

    Pawn steps:
        black:
            ↓ one step
            ↓ + ↓ two step
            ↓ + ← = ↙ capture west
            ↓ + → = ↘ capture east
        white:
            ↑ one step
            ↑ + ↑ two step
            ↑ + ← = ↖ capture west
            ↑ + → = ↗ capture east
    """

#   Pawn value:
    value: ClassVar[int] = 1

#   Pawn notation:
    letter: ClassVar[str] = ""
    symbol: ClassVar[str] = "♟"

#   Pawn moves:
    step: ClassVar[Vector] = Vector(+1, 0)  # One-step.
    jump: ClassVar[Vector] = Vector(+2, 0)  # Two-step.
    captures: ClassVar[set[Vector]] = {
        Vector(+1, -1),  # Capturing to the west.
        Vector(+1, +1),  # Capturing to the east.
    }

    @property
    def squares(self) -> set[Square]:
        f"""{super().squares.__doc__}"""
        squares = super().squares

        if self.square is not None:  # If pawn is on a board,
            for step in self.captures:  # For all target squares (diagonally with respect to pawn),
                square = self.square + step * self.orientation  # Get target,

                if self.capturable(square):  # If said target is inside board limits,
                    squares.add(square)  # Add said target to pawn.

            square = self.square + self.step * self.orientation  # Get forward square,

            if self.deployable(square):  # If said square is inside board limits,
                squares.add(square)  # Add said square to possible moves,

                if not self.has_moved:  # If the pawn is in its starting position,
                    square = self.square + self.jump * self.orientation  # Get next forward square,

                    if self.deployable(square):  # If said square is inside board limits,
                        squares.add(square)  # Add the next forward square to possible moves too.

        return squares

    @property
    def can_promote(self) -> bool:
        """Check if pawn is promotable."""
        return self.square is not None and self.square.rank == Square.rank_to_index[str((9 - self.orientation * 5) // 2)]

    def promote(self, target: Square, Piece: Type):
        super().__call__.__doc__

        if Piece in Officer.__args__ and self.can_promote:
            super().__call__(target)
            self.__class__ = Piece  # Promote pawn without changing any of its other attributes.

        return self
