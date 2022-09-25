"""Implements the chess pieces that are placed in a chessboard.

Of the 6 type of chess pieces pawns are special:
    Pawn: Moves one step forward, unless first move, where it may move two squares forward.
        Captures diagonally. Can en-pasant. Can be promoted to a higher value piece at the end of a player's board. Worth 1.
"""

from dataclasses import dataclass
from typing import ClassVar

from ..piece import Piece
from ..square import Square, Vector
from .meleed import King
from .ranged import Rook


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

#   Pawn moves:
    step: ClassVar[Vector] = Vector(+1, 0)  # One step.
    captures: ClassVar[set[Vector]] = {
        Vector(+1, -1),  # Capturing to the west.
        Vector(+1, +1),  # Capturing to the east.
    }

#   Pawn flags:
    promoted: bool = False

    def __repr__(self) -> str:
        super().__repr__.__doc__
        return {
            "white": f"\033[37;1m♟\033[0m",
            "black": f"\033[30;1m♟\033[0m",
        }[self.orientation.name]

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
                    square += self.step * self.orientation  # Get next forward square,

                    if self.deployable(square):  # If said square is inside board limits,
                        squares.add(square)  # Add the next forward square to possible moves too.

            else:  # Otherwise,
                self.promoted = True  # The pawn is promoted, assuming it falls outside because it can only move forward.

        return squares


@dataclass
class Castle:
    """ A pair of king and rook for facilitating castling.

    For each game, two such pairs are created per player, a king-side and a queen-side castle.
    This class attempts at abstracting the castling logic to its fundamental rules:
    -   The king must not have moved.
    -   The corresponding rook to castle must not have moved.
    -   The king must not be in check.
    -   The square the king skips with castling must not be threatened.
    -   There must not be any obstructing pieces (of any color).

    Relative positions will be used for checking and performing the castling,
    relying on the `has_moved` flags and proper board initialization to ensure correctness.

    Attributes:
        king: reference to a king piece
        rook: reference to a rook piece (of same color and on the same board)

    NOTE: Color logic will become cosmetic only, as soon as `Player` objects are implemented.
    This will solve both the "same color" and "same game (board)" issues,
    as pieces will be drawn from a player's collection.

    Castles belong to player and are a piece wrapper for such special moves.
    """

    king: King  # reference to a king piece
    rook: Rook  # reference to a rook piece (of same color)

    def deployable(self) -> bool:
        """Check if castling with the two pieces is still possible.

        This check will be refined with context from the board.
        For now check if either piece has moved, king is unchecked and corresponding rook is still alive.

        Returns:
            Whether castling with the two pieces is still possible.
        """
        return not (self.king.has_moved or self.rook.has_moved or self.king.in_check or self.rook.square is not None)
