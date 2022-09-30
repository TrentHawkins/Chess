"""Implements a player.

A game of chess always has two players, but this class will be able to keep track of each player stats in a meaningful way.
"""

from collections import Counter
from re import Pattern, compile
from types import MethodType

from .board import Board
from .move import Capture, Move
from .moves.castle import Castle
from .moves.pawn import EnPassant, Jump, Promotion
from .piece import Orientation, Piece
from .pieces.melee import King
from .pieces.pawn import Pawn
from .square import Square


class Player:
    """A player.

    Attributes:
        name: The player's name.
        board: The board this player is playing on.
        orientation: The allegiance of the player, defining the correspponding orientation of the board.
        pieces: A collection of the player's pieces on the board.
        captured: A collection of captured pieces hashed by piece type.
            NOTE: All captured pieces are expected to have `square == None` making them distinct only by type.
    """

    def __init__(self, name: str, color: str, board: Board):
        """Create collections for player.

        Args:
            name: The player's name.
            color: The color of the player's pieces.
            board: The board this player is playing on.

        Also defines player-context-sensitive rules for evaluating piece legal moves.
        King safety is not relevant nor can be resolve here.
        The piece legal moves shall be agnostically updated here though,
        because the squares the player checks are legit, since king safety is irrelevant when it is not their turn!
        In elaboration, if an opponent walks their king in danger, it does not matter if your king will be in danger after;
        their king will die first.
        """
        self.name: str = name
        self.orientation: Orientation = Orientation[color]  # The allegiance of the player.
        self.board: Board = board  # The board this player is playing on.

    #   Assign pieces to player agnostically, so that custom position can also be loaded.
        self.pieces: set[Piece] = set(piece for piece in self.board if piece.orientation == self.orientation)
        self.captured: Counter[Piece] = Counter()  # NOTE: Not yet implemented.

        def piece_deployable(source_piece: Piece, target: Square):
            source_piece.deployable.__doc__
            target_piece = self.board[target]

            is_empty = target_piece is None or type(target_piece) is Piece

            return source_piece.__class__.deployable(source_piece, target) and is_empty

        def piece_capturable(source_piece: Piece, target: Square):
            source_piece.capturable.__doc__
            target_piece = self.board[target]

            is_not_empty = target_piece is not None and type(target_piece) is not Piece \
                and source_piece.orientation != target_piece.orientation

            return source_piece.__class__.capturable(source_piece, target) and is_not_empty

    #   Add ghost pieces to target of pawns:
        def pawns_capturable(source_piece: Piece, target: Square):
            source_piece.capturable.__doc__
            target_piece = self.board[target]

            is_not_empty = target_piece is not None \
                and source_piece.orientation != target_piece.orientation

            return source_piece.__class__.capturable(source_piece, target) and is_not_empty

        for piece in self.pieces:
            piece.deployable = MethodType(piece_deployable, piece)

            if type(piece) is Pawn:
                piece.capturable = MethodType(pawns_capturable, piece)

            else:
                piece.capturable = MethodType(piece_capturable, piece)

    #   Keep the player's king registered, as it is a special piece.
        for piece in self.pieces:
            if type(piece) is King:
                self.king: King = piece

    def __repr__(self):
        """Represent a player by name and captured pieces.

        NOTE: Timer is not implemented yet.

        Returns:
            Players name followed by a color window and captured pieces
        """
        ...

    def __call__(self, move: Move | Castle):
        """Move the source piece to target square if move is valid.

        Jumps should be checked here, because a ghost piece of the same color as the player must be generated with them.

        Args:
            source_piece: The piece to move.
            target: The square in notation the piece wants to go to.
        """
        target_piece = self.board(move)  # Make the move.

    #   If move is a pawn jump, add a trailing ghost piece temporarily.
        if type(move) is Jump:
            self.board[move.middle] = Piece(self.orientation)  # This will have to go on the next round (2 turns).

    #   NOTE: The en-passant can only be detected by type-checking, I think...
        if type(target_piece) is Piece:  # If target piece is a ghost,
            if type(move.piece) is Pawn:  # If it is a pawn targeting it en-passant,
                target = move.square + move.piece.step * target_piece.orientation

                target_piece, self.board[target] = self.board[target], None

    #   If there was a opponent piece there, properly dispose of it.
        if target_piece is not None:
            target_piece.square = None

            self.captured[target_piece] += 1

    def read(self) -> Move | Castle:
        """Read move from standard input with a prompt.

        Try forever till a legit move is found.
        FIXME: This will get stuck upon checkmate.

        Args:
            move: _description_
        """
        message = "your turn"

        while True:
            input_move = input(f"\033[A{self.name}, {message}: \033[K")

        #   If a plain move is given:
            if Move.notation.match(input_move):
                for piece in self.pieces:
                    source = Square(input_move[-5:-3])
                    target = Square(input_move[-2:])

                    if type(piece) is Move.letterPiece[input_move[:-5]] and piece.square == source:
                        move = Move(piece, target)

        #   If a capture is given:
            if Capture.notation.match(input_move):
                for piece in self.pieces:
                    source = Square(input_move[-5:-3])
                    target = Square(input_move[-2:])

                    if type(piece) is Move.letterPiece[input_move[:-5]] and piece.square == source:
                        move = Capture(piece, target)

        #   If a starting pawn jump is given:
            if Jump.notation.match(input_move):
                for piece in self.pieces:
                    source = Square(input_move[-5:-3])
                    target = Square(input_move[-2:])

                    if type(piece) is Pawn and piece.square == source:
                        move = Jump(piece, target)

        #   If a pawn promotion is given:
            if Promotion.notation.match(input_move):
                for piece in self.pieces:
                    source = Square(input_move[-5:-3])
                    target = Square(input_move[-2:])

                    if type(piece) is Pawn and piece.square == source:
                        move = Promotion(piece, target, Move.letterPiece[input_move[:-5]])

        #   If a castle symbol is given (no need for pattern matching here really):
            if Castle.notation.match(input_move):
                king = self.king

                if input_move == "O-O":
                    rook = self.board[f"h{king.square.rank}"]  # type: ignore

                if input_move == "O-O-O":
                    rook = self.board[f"a{king.square.rank}"]  # type: ignore

                move = Castle(king, rook)  # type: ignore

        #   Check move here too to catch the re-try:
            try:
                if move.is_legal():  # type: ignore
                    return move  # type: ignore

                else:
                    message = "try again"
                    continue

            except UnboundLocalError:
                message = "try again"
                continue

    @property
    def squares(self) -> set[Square]:
        """Get all squares checked by player.

        Returns:
            A flattened union of all squares the player has access to.
        """
        return {square for piece in self.pieces for square in piece.squares}
