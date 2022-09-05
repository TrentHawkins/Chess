"""Implements the chess pieces that are placed in a chessboard.

Of the 6 type of chess pieces pawns are special:
    Pawn: Moves one step forward, unless first move, where it may move two squares forward.
        Captures diagonally. Can en-pasant. Can be promoted to a higher value piece at the end of a player's board. Worth 1.
"""

from dataclasses import dataclass
from itertools import product
from typing import ClassVar

from ..piece import Piece
from ..square import Square, Vector


@dataclass(init=False, repr=False)
class Pawn(Piece):
    """A Pawn.

    Moves forward a square, unless its first move where it can move two and unless blocked by any piece.
    It captured forward-diagonally. I can capture en-passant:
        If an enemy pawn passes yours trying to escape capture, well... it cannot, not for this round.
    NOTE: That probably means that board will invoke this method multiple times (unti a better way is thought).
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

#   Pawn moves:
    step: ClassVar[Vector] = Vector(+1, 0)  # One step.
    captures: ClassVar[set[Vector]] = {
        Vector(+1, -1),  # Capturing to the west.
        Vector(+1, +1),  # Capturing to the east.
    }

#   Pawn flags:
    has_moved: bool = False
    promoted: bool = False

    def __repr__(self) -> str:
        super().__repr__.__doc__
        return {
            "white": "♙",
            "black": "♟",
        }[self.orientation.name]

    @property
    def moves(self) -> tuple[set[Square], set[Square]]:
        f"""{super().moves.__doc__}"""
        squares, targets = super().moves

        if self.square is not None:  # If pawn is on a board,
            for step in self.captures:  # For all target squares (diagonally with respect to pawn),
                square = self.square + step * self.orientation  # Get target,

                if square is not None:  # If said target is inside board limits,
                    targets.add(square)  # Add said target to pawn.

            square = self.square + self.step * self.orientation  # Get forward square,

            if square is not None:  # If said square is inside board limits,
                squares.add(square)  # Add said square to possible moves,

                if not self.has_moved:  # If the pawn is in its starting position,
                    squares.add(square + self.step * self.orientation)  # Add the next forward square to possible moves too.

            else:  # Otherwise,
                self.promoted = True  # The pawn is promoted, assuming it falls outside because it can only move forward.

        return squares, targets
