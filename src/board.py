"""Implements a chessboard.

Referencing with chess algebraic notation is possible.
"""

from .pieces import Piece, Pawn, Bishop, Knight, Rook, Queen, King


class Board:
    """A Chessboard.

    Pieces can be assigned, obtained or removed by referencing squares with chess algebraic notation.
    The notation consists of a letter ('A' through 'H') for the file (column) of a square and a number (1-8) for the rank (row).
    The convention here is to match `index+1` to file for columns (inner lists) and `8-index` for rows (reverse row referencing).

    Examples:
        Item at [2][3] is referenced as ["d6"].
        Item at [5][3] is referenced as ["d3"].
        Item at [0][7] is referenced as ["h8"].
        Item at [7][0] is referenced as ["a1"].
    """

    index_to_file = {index_: file_ for index_, file_ in zip(range(8), "abcdefgh")}
    file_to_index = {file_: index_ for index_, file_ in zip(range(8), "abcdefgh")}
    index_to_rank = {index_: rank_ for index_, rank_ in zip(range(8), "87654321")}
    rank_to_index = {rank_: index_ for index_, rank_ in zip(range(8), "87654321")}

    def __init__(self):
        """Initialize a chessboard with a new game congifuration."""

        self.matrix: list[list[Piece | None]] = [[None] * 8 for _ in range(8)]

        self["a1"] = Rook("white")
        self["b1"] = Knight("white")
        self["c1"] = Bishop("white")
        self["d1"] = Queen("white")
        self["e1"] = King("white")
        self["f1"] = Bishop("white")
        self["g1"] = Knight("white")
        self["h1"] = Rook("white")
        self["a2"] = Pawn("white")
        self["b2"] = Pawn("white")
        self["c2"] = Pawn("white")
        self["d2"] = Pawn("white")
        self["e2"] = Pawn("white")
        self["f2"] = Pawn("white")
        self["g2"] = Pawn("white")
        self["h2"] = Pawn("white")

        self["a8"] = Rook("black")
        self["b8"] = Knight("black")
        self["c8"] = Bishop("black")
        self["d8"] = Queen("black")
        self["e8"] = King("black")
        self["f8"] = Bishop("black")
        self["g8"] = Knight("black")
        self["h8"] = Rook("black")
        self["a7"] = Pawn("black")
        self["b7"] = Pawn("black")
        self["c7"] = Pawn("black")
        self["d7"] = Pawn("black")
        self["e7"] = Pawn("black")
        self["f7"] = Pawn("black")
        self["g7"] = Pawn("black")
        self["h7"] = Pawn("black")

    @classmethod
    def board_coordinates(cls, file_rank: str) -> tuple[int, int]:
        """Provide the board coordinates for a given file and rank.

        Args:
            file_rank: The file and rank.

        Returns:
            The board coordinates.
        """

        return cls.rank_to_index[file_rank[1]], cls.file_to_index[file_rank[0]]

    def __setitem__(self, file_rank: str, value: Piece | None = None):
        """Place a piece to a square.

        Args:
            file_rank: The file and rank of the square.
            value: The piece to be placed on the square.
        """

        i, j = self.board_coordinates(file_rank)
        self.matrix[i][j] = value

    def __getitem__(self, file_rank: str) -> Piece | None:
        """Get the piece of a given square.

        Args:
            file_rank: The file and rank.

        Returns:
            The piece to the given file and rank.
        """

        i, j = self.board_coordinates(file_rank)
        return self.matrix[i][j]

    def __repr__(self) -> str:
        """Represent the board in proper direction and use the representation of each piece.

        Returns:
            The board representation.
        """
        return (
            "\n▐\033[7m  A B C D E F G H  \033[0m▌\n" +
            "\n".join(
                f"▐\033[7m{self.index_to_rank[index]}\033[0m▌" +
                " ".join(str(piece) for piece in rank) +
                f"▐\033[7m{self.index_to_rank[index]}\033[0m▌"
                for index, rank in enumerate(self.matrix)) +
            "\n▐\033[7m  A B C D E F G H  \033[0m▌\n\n"
        ).replace("None", " ")
