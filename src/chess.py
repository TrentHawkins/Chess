"""A game of chess."""
from typing import Callable

from .board import Board
from .piece import Color, Piece, King, Pawn, Queen, Rook, Knight, Bishop
from .square import Square


Score = tuple[int, int]
Checkmate = bool


def default_ending(board: Board):
    starting_board = Board()
    return board == starting_board


class Chess:
    """A chess game."""

    pawn_upgrade = {
        "Queen": Queen,
        "Rook": Rook,
        "Knight": Knight,
        "Bishop": Bishop
    }

    def __init__(self, input_: Callable[[str], str]=input, ending_condition: Callable[[Board], bool]=default_ending) -> None:
        """Start a chess game."""
        self._board = Board()
        self._input = input_
        self._ending_condtion = ending_condition

    def _take_turns(self, color: Color) -> tuple[Score, Checkmate]:
        """A player's turn, where he selects a piece to move and a target square to move to.

        Args:
            color: the color of the player.

        Returns:
            a tuple of the current score and whether the game has ended with checkmate.
        """
        if self._ending_condtion(self._board):
            return (0, 0), True

        piece: Piece | None = None
        selected_square: Square | None = None
        move_selection: set[Square] | None = None
        print(self._board)
        # will loop until all a proper square is selected.
        while True:
            selected_square = Square(self._input("Choose a piece to move: "))
            piece = self._board[selected_square]
            move_selection = self._board.list_moves(selected_square)
            if not move_selection:
                print(f"No moves available for {piece} at {selected_square}.")
                continue
            if piece is not None and piece.color == color:
                break
            print("Invalid square selection.")
        
        # select target square from legal moves.
        choice:int | None = None
        while choice is None:
            self._print_options(move_selection)
            choice = self._input("Choose target square from the above options: ")
            if Square(choice) not in move_selection:
                print("Invalid option.")
                choice = None

        # apply chosen move and return score and that the game continues.
        target_square = Square(choice)
        other_piece = self._move(piece, selected_square, target_square)
        self._special_event(piece, target_square)
        if other_piece is not None:
            return ((other_piece.value, 0), False) if color == Color.white else ((0, other_piece.value), False)
        # just a move to ane empty square
        return (0, 0), False

    def run(self) -> tuple[Score, Color]:
        """Start the game of chess, it finishes when a checkmate occurs.

        Returns:
            the final score of the game and the color of the winner.
        """
        game_over = False
        color = Color.white
        score = (0, 0)
        while not game_over:
            diff_score, checkmate = self._take_turns(color)
            score = self._update_score(score, diff_score)
            color = Color.white if color == Color.black else Color.black
            if checkmate:
                game_over = True
                winner = color
            
        return score, winner

    @staticmethod
    def _update_score(score: Score, diff_score: tuple[int, int]) -> Score:
        """Update the score after a move was made.

        Args:
            score: the previous score before the move.
            diff_score: how much the score changed.

        Returns:
            the new score.
        """
        score_white, score_black = score
        diff_white, diff_black = diff_score
        return score_white + diff_white, score_black + diff_black

    def _move(self, piece: Piece, start_square: Square, target_square: Square) -> Piece:
        """Move a piece on the board, returning any enemy piece captured.

        Args:
            piece: the piece to move
            start_square: the starting position of the piece.
            target_square: the position the piece will move to.

        Returns:
            any enemy piece that is captured because of the move.
        """
        other_piece = self._board[target_square]
        self._board[start_square], self._board[target_square] = None, piece

        return other_piece

    def _special_event(self, piece: Piece, square: Square) -> None:
        """Handles special events, such as a pawn reaching the end of the board and transforming.
        """
        if isinstance(piece, Pawn) and square.rank in {0, 7} :
            new_piece: str | None = None
            while True:
                print("A pawn has reached the end of the board.")
                for to_choose in self.pawn_upgrade:
                    print(f"- Option: {to_choose}")
                new_piece = self._input("Please choose pawn upgrade: ")
                if new_piece not in self.pawn_upgrade:
                    print("Invalid choice, please try again.")
                else:
                    break
            self._board[square] = self.pawn_upgrade[new_piece](piece.color)


    def _print_options(self, move_selection: set[Square]) -> None:
        """Print movement options to the screen.
        
        Args:
            move_selection: the moves to be printed.

        Returns:
            Nothing, only prints to screen.
        """
        for target_square in move_selection:
            other_piece = self._board[target_square]
            if other_piece is not None:
                print(f"- Option: {target_square} capturing {other_piece}.")
            else:
                print(f"- Option: {target_square}")
