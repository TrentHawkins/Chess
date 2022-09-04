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

Here you will find the implementation of pawns as they are a special type of pieces.
"""

from dataclasses import dataclass
from enum import IntEnum
from itertools import combinations, product
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
        return " "  # An unspecified piece is a ghost piece.

    def has_friend(self, other):
        """Check weather `target` is a foe of `source`.

        NOTE: this can be done with `Piece` objects instead of `Square` ones.

        Args:
            source: The source piece.
            source: The target piece to check allegiance of.

        Returns:
            True if `target` square has a foe of whatever is on `source` square.
        """
        if self and other:
            return self.orientation == other.orientation

        return False

    def has_foe(self, other):
        """Check weather `target` is a friend of `source`.

        NOTE: this can be done with `Piece` objects instead of `Square` ones.

        Args:
            source: The source piece.
            source: The target piece to check allegiance of.

        Returns:
            True if `target` square has a foe of whatever is on `source` square.
        """
        if self and other:
            return self.orientation != other.orientation

        return False

    def condition(self, target: Square) -> bool:
        """Special conditions pertaining the particular piece type and source square.

        This method is to be lazily-defined in board, access to current piece data makes it appropriate to sign it in here.

        Args:
            target: The source square is `self.square`.

        Returns:
            Whether the specific condition are met.
        """
        return self.square is not None  # The most basic condition if for a piece to be on a legal square.

#   NOTE: The king might be prove to be problematic, as it has an extra condition of blocked movement, squares that are checked.
    def moves(self) -> tuple[set[Square], set[Square]]:
        f"""Generate all legal moves a {self.__class__.__name__} can apriori make.

        2 sets are returned, one for empty squares the piece can move to and one for potential target squares.
        The logic is to unify movement blocking logic, and basically differentiate blocks by type.
        Only target squares may mutate into viable move squares.

        Example:
            Suppose there is a rook at "h1" and a pawn at "h6". The rook can move freely up to "h5".
            If the pawn at "h6" is friednly this is it. If it is foe, then rook on "h1" can capture pawn on "h6".
            Instead of differentiating scenario early,
            apply a global blocking movement policy and add blockers to potential targets instead, to be trimmed by color.

        Example with block resolution:
            Suppose there is a white pawn at "e4" and two black pawns at "d5" and "e5" respectively.
            Upon checking the white pawn for legal moves,
                squares will be blocked if any piece is found in them
                targets will be blocked if an enemy piece is not found in them.

        The reason is that, no matter how a piece moves,
        target resolution happens only at the trailing end of its move pattern.
        Therefore, if target squares do not contain an enemy, the piece cannot go there,
        because target are created when the trigger for blocking squares is activated.
        See implementation of `Range(Piece)` for an illustrative application of this logic.

        Pawns:
            This logic is extensible to pawns as well.
            Their diagonals will be checked with and only with enemy pieces, as it should.
            The front of a pawn will be checked if blocked normally. No color check is needed, if blocked, that is it.

        Why does the latter not affect other pieces?
        Because the trailing end of all movements is always a target square for all pieces.

        Args:
            square: Square on which piece is placed.
                Default is no square, in which case displacements are not resolved into squares and generators not unfold.
            condition: A condition that depends on a square, usually a target square.

        Returns:
            2 sets of moves:
                squares: any empty potential square the piece can move to
                targets: any potential square in squares that the piece can target another piece
        """
        squares, targets = set(), set()
        return squares, targets  # A ghost piece cannot move or capture.


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
        self.__repr__.__doc__
        return {
            "white": "♙",
            "black": "♟",
        }[self.orientation.name]

    def moves(self) -> tuple[set[Square], set[Square]]:
        super().moves.__doc__
        squares, targets = super().moves()

        if self.square is not None:  # If pawn is on a board,
            for step in self.captures:  # For all target squares (diagonally with respect to pawn),
                target = self.square + step * self.orientation  # Get target,

                if target is not None:  # If said target is inside board limits,
                    targets.add(target)  # Add said target to pawn.

            square = self.square + self.step * self.orientation  # Get forward square,

            if square is None:  # If said square is outside board limits,
                self.promoted = True  # The pawn is promoted, assuming it falls outside because it can only move forward.

            else:  # Otherwise,
                squares.add(square)  # Add said square to possible moves,

                if not self.has_moved:  # If the pawn is in its starting position,
                    squares.add(square + self.step * self.orientation)  # Add the next forward square to possible moves too.

        return squares, targets


@dataclass(init=False, repr=False)
class Meleed(Piece):
    """A close ranged piece:
        - King
        - Knight (has reach)

    For a meeled piece (pawns are special) all squares are target squares.
    """

    def moves(self) -> tuple[set[Square], set[Square]]:
        super().moves.__doc__
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
        super().__repr__.__doc__
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
        super().__repr__.__doc__
        return {
            "white": "♘",
            "black": "♞",
        }[self.orientation.name]


@dataclass(init=False, repr=False)
class Ranged(Piece):
    """A long range piece:
        - Rook
        - Bishop
        - Queen
    """

    def moves(self) -> tuple[set[Square], set[Square]]:
        super().moves.__doc__
        squares, targets = super().moves()

        if self.square is not None:  # If ranged piece is on a board,
            for step in self.steps:  # For all legal directions,
                square = self.square + step  # Get next square in direction,

                while square is not None and self.condition(square):  # If said square is inside board limits,
                    squares.add(square)  # Add said square to ranged piece.
                    square += step  # Advance to the next square in said direction.

                if square is not None:  # NOTE: This check will become relevant as soon as condition is defined too.
                    targets.add(square)  # Do not forget to add trailing square to targets.

        return squares, targets


@dataclass(init=False, repr=False)
class Rook(Ranged):
    """A rook.

    Moves anywhere along its rank xor its file, unless blocked by enemy (which captures) or same piece.

    Rook steps:
        ↑ north
        ← west
        ↓ south
        → east
    """

#   Knight value:
    value: ClassVar[int] = 5

#   Straight lines:
    steps: ClassVar[set[Vector]] = Piece.straights

    def __repr__(self) -> str:
        super().__repr__.__doc__
        return {
            "white": "♖",
            "black": "♜",
        }[self.orientation.name]


@dataclass(init=False, repr=False)
class Bishop(Ranged):
    """A bishop.

    Moves anywhere along a diagonal, unless blocked by enemy (which captures) or same piece.
    This means that a bishop never leaves the color of the square it is on.
    A player starts with two bishops:
        A black-square bishop.
        A white-square bishop.
    So both cover the squares of the whole board, and it is the reason the worth more when both on the board.

    Bishop steps:
        ↗ north-east
        ↘ south-east
        ↖ north-west
        ↙ south-west
    """

#   Knight value:
    value: ClassVar[int] = 3

#   Diagonal lines:
    steps: ClassVar[set[Vector]] = Piece.diagonals

    def __repr__(self) -> str:
        super().__repr__.__doc__
        return {
            "white": "♗",
            "black": "♝",
        }[self.orientation.name]


@dataclass(init=False, repr=False)
class Queen(Ranged):
    """A queen.

    Moves both like a rook and bishop, unless blocked by enemy (which captures) or same piece.
    Can access all squares.

    Inherits the steps of a King but the movement of Range.

    Queen steps:
        ↑ north
        ← west
        ↓ south
        → east
        ↗ north-east
        ↘ south-east
        ↖ north-west
        ↙ south-west
    """

#   Knight value:
    value: ClassVar[int] = 9

#   Queen lines:
    steps: ClassVar[set[Vector]] = Piece.straights | Piece.diagonals

    def __repr__(self) -> str:
        super().__repr__.__doc__
        return {
            "white": "♕",
            "black": "♛",
        }[self.orientation.name]
