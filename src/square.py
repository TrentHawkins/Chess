"""Implement square logic.

A different type is used for displacements on squares since they are also semantically distinct.
"""


import re
from dataclasses import dataclass

Rank = int
File = int


@dataclass(frozen=True)  # NOTE: That's right, vectors and squares must be immutable.
class Vector:
    """Integer 2-dimensional vector rerepsenting square displacements on the board.

    This type supports basic vector operations to allow making complex displacements out of simpler ones.
    This type can also be read as a square on the board,
    in which case the board origin is assumed to be the nested list origin (top-left as the board is printed).

    Attributes:
        rank: 1st component of displacement vector or row on the board if read as a square.
        file: 2nd component of displacement vector or column on the board if read as a square.

    Methods:
        +: Add displacements together.
        -: Subtract displacements.
        *: Scale displacements conformally.
    """

    rank: Rank
    file: File

    def __add__(self, other):
        """Vector addition."""
        return Vector(
            self.rank + other.rank,
            self.file + other.file,
        )

    def __sub__(self, other):
        """Vector subtraction."""
        return Vector(
            self.rank - other.rank,
            self.file - other.file,
        )

    def __mul__(self, times: int):
        """Vector multiplication with an factor."""
        return Vector(
            self.rank * times,
            self.file * times,
        )


@dataclass(frozen=True)
class Square(Vector):
    """A square on the chessboard.

    Squares are modelled after vector objects, with the logic that displacements become positions given an origin.
    Operations supported for squares only involve addition or subtraction of displacements, that return a new vector.

    Construction of squares is supercharged with the option of using chess notation instead.
    In addition, unlike vector displacements, chess squares are also represented in chess notation.

    You can operate on squares with squares, but results will be unpredictable unless you know what you are doing.
    """

    rank_range = "87654321"
    file_range = "abcdefgh"

    index_to_file = {index_: file_ for index_, file_ in zip(range(8), file_range)}  # translate range index to file in chess
    file_to_index = {file_: index_ for index_, file_ in zip(range(8), file_range)}  # translate file in chess to range index
    index_to_rank = {index_: rank_ for index_, rank_ in zip(range(8), rank_range)}  # translate range index to rank in chess
    rank_to_index = {rank_: index_ for index_, rank_ in zip(range(8), rank_range)}  # translate rank in chess to range index

    notation_range = re.compile(f"[{file_range}][{rank_range}]")

    def __new__(cls, square: Vector | str):
        """Abort if attempted square is illegal.

        This is used to make `Square` objects self-correcting upon behavior.
        Failure of creation will be its own validity check.

        Args:
            square: A square in notation form or a vector (assuming the board origin is top-left in the latter case).

        Returns:
            `None` if square specification is illegal.
        """
        match square:
            case Vector(rank, file):
                return super().__new__(cls) if rank in range(8) and file in range(8) else None
            case str():
                return super().__new__(cls) if Square.notation_range.match(square) else None

    def __init__(self, square: Vector | str):
        """Make square.

        Args:
            square: A square in notation form or a vector (assuming the board origin is top-left in the latter case).
        """
        match square:
            case Vector(rank, file):
                super().__init__(rank, file)
            case str():
                super().__init__(
                    Square.rank_to_index[square[1]],
                    Square.file_to_index[square[0]],
                )

    def __repr__(self):
        """Represent square in chess notation.

        Returns:
            The rank and file of square in chess notation.
        """
        return (
            Square.index_to_file[self.file] +
            Square.index_to_rank[self.rank]
        )

    def __add__(self, other: Vector):
        """Add vector (displacement) to a square."""
        return Square(super().__add__(other))
