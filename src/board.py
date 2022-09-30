"""Implements a chessboard.

Referencing with chess algebraic notation is possible.
"""

from itertools import cycle
from typing import Generator

from .move import Capture, Move
from .moves.castle import Castle
from .moves.pawn import Promotion
from .piece import Orientation, Piece
from .pieces.melee import King, Knight
from .pieces.pawn import Pawn
from .pieces.ranged import Bishop, Queen, Rook
from .square import Square


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

#   Decide theme statically for now.
    default_board_theme = {
        'white': 3,
        'black': 1,
    }

#   Convinient piece color list.
    piece_colors = [
        "white",
        "black",
    ]

#   Convinient main piece file dictionary, as pieces' file by type match.
    main_pieces = {
        "a": Rook,
        "b": Knight,
        "c": Bishop,
        "d": Queen,
        "e": King,
        "f": Bishop,
        "g": Knight,
        "h": Rook,
    }

#   Graphics:
    rank_range = "12345678"
    file_range = "ABCDEFGH"

    def __init__(self, *, empty: bool = False, theme: dict[str, int] = default_board_theme, flipped: bool = False):
        """Initialize a chessboard with a new game congifuration."""
        self.pieces: list[list[Piece | None]] = [[None for _ in range(8)] for _ in range(8)]
        self.theme = theme  # Set board color theme.
        self.custom = empty  # Whether an empty or custom borad is being used.
        self.flipped = flipped  # Whether to display board flipped 180 degrees (from black's viewpoint)

        if not self.custom:
            for color in Board.piece_colors:
                pawn_rank = (Orientation[color] * 5 + 9) // 2  # Pawn rank per color.
                main_rank = (Orientation[color] * 7 + 9) // 2  # Main rank per color.

            #   All the pieces:
                for file, Main in Board.main_pieces.items():
                    self[f"{file}{main_rank}"] = Main(color)  # The main pieces (rooks, knights, bishops, queen, king)
                    self[f"{file}{pawn_rank}"] = Pawn(color)  # The pawns.

    def __repr__(self) -> str:
        """Represent the board in proper direction and use the representation of each piece.

        Returns:
            The board representation.
        """
        white = 3
        black = 1

        square_color = cycle(
            [
                f"\033[0m\033[4{self.theme['white']}m",  # white
                f"\033[0m\033[4{self.theme['black']}m",  # black
            ]
        )
        edge_color = cycle(
            [
                f"\033[0m\033[3{self.theme['black']};4{self.theme['white']}m▐",
                f"\033[0m\033[3{self.theme['white']};4{self.theme['black']}m▐",
            ]
        )
        border_color = cycle(
            [
                f"\033[0m\033[3{self.theme['white']}m▐",
                f"\033[0m\033[3{self.theme['black']}m▌\033[0m",
                f"\033[0m\033[3{self.theme['black']}m▐",
                f"\033[0m\033[3{self.theme['white']}m▌\033[0m",
            ]
        )

        representation = "\033[A" * 15 + "\n"

        if self.flipped:
            representation += " ▗▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▖ \n"
            representation += " ▐▌  H G F E D C B A  ▐▌ \n"

            for index, rank in enumerate(reversed(self.pieces)):
                representation += " ▐▌" + str(index + 1) + next(border_color)
                representation += (
                    next(square_color) + str(rank[7]) + next(edge_color) +
                    next(square_color) + str(rank[6]) + next(edge_color) +
                    next(square_color) + str(rank[5]) + next(edge_color) +
                    next(square_color) + str(rank[4]) + next(edge_color) +
                    next(square_color) + str(rank[3]) + next(edge_color) +
                    next(square_color) + str(rank[2]) + next(edge_color) +
                    next(square_color) + str(rank[1]) + next(edge_color) +
                    next(square_color) + str(rank[0])
                )
                representation += next(border_color) + str(index + 1) + "▐▌ \n"

                next(square_color)  # Flip colors for next rank to make a checkerboard.

            representation += " ▐▌  H G F E D C B A  ▐▌ \n"
            representation += " ▝▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▘ \n"

        else:
            representation += " ▗▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▖ \n"
            representation += " ▐▌  A B C D E F G H  ▐▌ \n"

            for index, rank in enumerate(self.pieces):
                representation += " ▐▌" + str(Square.index_to_rank[index]) + next(border_color)
                representation += (
                    next(square_color) + str(rank[0]) + next(edge_color) +
                    next(square_color) + str(rank[1]) + next(edge_color) +
                    next(square_color) + str(rank[2]) + next(edge_color) +
                    next(square_color) + str(rank[3]) + next(edge_color) +
                    next(square_color) + str(rank[4]) + next(edge_color) +
                    next(square_color) + str(rank[5]) + next(edge_color) +
                    next(square_color) + str(rank[6]) + next(edge_color) +
                    next(square_color) + str(rank[7])
                )
                representation += next(border_color) + str(Square.index_to_rank[index]) + "▐▌ \n"

                next(square_color)  # Flip colors for next rank to make a checkerboard.

            representation += " ▐▌  A B C D E F G H  ▐▌ \n"
            representation += " ▝▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▘ \n"

        return representation.replace("None", "\033[8m🨅\033[0m")

    def __setitem__(self, square: Square | str, piece: Piece | None):
        """Add a piece to a square.

        Args:
            square: The rank and file of the square.
            piece: The piece to be placed on the square.
        """
        square = Square(square)

        self.pieces[square.rank][square.file] = piece

    #   If a true piece is assigned, update its square.
        if piece is not None:
            piece.square = square

    def __getitem__(self, square: Square | str) -> Piece | None:
        """Get the piece of a given square.

        Args:
            square: The rank and file of the square.

        Returns:
            The piece on the given square.
        """
        square = Square(square)

    #   HACK: A square outside the board may be requested.
        if square is not None:
            return self.pieces[square.rank][square.file]

    def __delitem__(self, square: Square | str):
        """Remove the piece of a given square.

        Args:
            square: The rank and file of the square on which to remove a piece (if any).
        """
        square = Square(square)

        piece = self[square]

    #   If there truly is a piece on that square, and referenced elsewhere, best do the book-keeping of taking it off-board.
        if piece is not None:
            piece.square = None

        self.pieces[square.rank][square.file] = None

    def __iter__(self):
        """Iterate through existent pieces on the board."""
        for rank in self.pieces:
            for piece in rank:
                if piece is not None:
                    yield piece

    def __contains__(self, piece: Piece | None) -> bool:
        """Check if a piece is on the board.

        Args:
            piece: Basically type and color of piece to be checked.

        Returns:
            If piece is in board.
        """
        return any(piece in rank for rank in self.pieces)

    def __call__(self, move: Move | Castle) -> Piece | None:
        """Move the source piece to target square if move is valid.

        Whatever lies on the target square is saved for further processing, however its square is killed, naturally.

        Promotions should be checked here, as the move/capture happesn normally, and even the color doesn't change.
        What changes is simply the subclass of the pawn involved.

        Args:
            source_piece: The piece to move.
            target: The square in notation the piece wants to go to.

        Returns:
            Lost piece on target square if any.
        """
        source = move.piece.square  # This is defined for all kinds of moves.
        target = move.square  # This is defined for all kinds of moves either implicitely or explicitely.

    #   Save the piece captured in the move, if any.
        target_piece = self[move.square]

    #   If the move is a castling, move the rook first before moving the king.
        if type(move) is Castle:
            assist = move.other.square
            middle = move.middle

            move.piece(target)
            move.other(middle)

        #   Move the rook in-place. King will be moved as normal with the main move.
            self[middle], self[assist] = move.other, None  # type: ignore

    #   If the source piece is in-board and the target square is legit, make the move and switch its has-moved flag.
        else:
            if move.piece.square is not None:
                if type(move) is Promotion and type(move.piece) is Pawn:
                    move.piece.promote(target, move.Piece)

            #   If move is anything other than a promotion just move the piece.
                else:
                    move.piece(target)

    #   Make the move. If a castling, this is the king moving in place.
        self[target], self[source] = move.piece, None  # type: ignore

        return target_piece
