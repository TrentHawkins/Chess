import re
import numpy

from pieces import Piece, Pawn, Bishop, Knight, Rook, Queen, King


class Board(numpy.ndarray):
    def __new__(cls):
        """A chess-board shall be a fixed 8 times 8 2-dimensional array of type `Piece(object)`."""
        return super(Board, cls).__new__(cls, (8, 8), dtype=Piece)  # [https: //numpy.org/doc/stable/user/basics.subclassing.html]

    def __init__(self):
        """Board initialization with pieces.

        The direction of a 2-dimennsional array is top-right, while that of a chess-board is bottom-right.
        Therefore the white pieces are placed on rows 7 and 6 while the black pieces on rows 0 and 1.

        See the `Piece` class tree for details."""
        super(Board, self).__init__()

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

    def __repr__(self):
        """A compact represantation of the board in proper direction and with using the representation of each piece."""
        ranker = range(8)

        return (
            "\n▐\033[7m  A B C D E F G H  \033[0m▌\n" +
            "\n".join(
                f"▐\033[7m{Square.rank(index)}\033[0m▌" +
                " ".join(file.__repr__() for file in rank) +
                f"▐\033[7m{Square.rank(index)}\033[0m▌"
                for index, rank in enumerate(self)) +
            "\n▐\033[7m  A B C D E F G H  \033[0m▌\n\n"
        ).replace("None", " ")

    def __setitem__(self, key: str, value: Piece):
        """Finish using the chess algebraic notation by changing the indexing of the board by the user."""
        if isinstance(key, str):
            super(Board, self).__setitem__(Square(key), value)  # delegate wrong notation to the `Square` class
        else:
            super(Board, self).__setitem__(key, value)  # delegate all other indexing to NumPy as normal

    def __getitem__(self, key: str):
        """Finish using the chess algebraic notation by changing the indexing of the board by the user."""
        if isinstance(key, str):
            return super(Board, self).__getitem__(Square(key))  # delegate wrong notation to the `Square` class
        else:
            return super(Board, self).__getitem__(key)  # delegate all other indexing to NumPy as normal

    def __delitem__(self, key: str):
        """Finish using the chess algebraic notation by changing the indexing of the board by the user."""
        if isinstance(key, str):
            super(Board, self).__delitem__(Square(key))  # delegate wrong notation to the `Square` class

        else:
            super(Board, self).__delitem__(key)  # delegate all other indexing to NumPy as normal


notation = re.compile("[abcdefgh][12345678]")
index_to_file = {index_: file_ for index_, file_ in zip(range(8), "abcdefgh")}
file_to_index = {file_: index_ for index_, file_ in zip(range(8), "abcdefgh")}
index_to_rank = {index_: rank_ for index_, rank_ in zip(range(8), "87654321")}
rank_to_index = {rank_: index_ for index_, rank_ in zip(range(8), "87654321")}
