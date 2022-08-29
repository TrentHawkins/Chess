"""Unit tests for the Chess project."""


initial_board_state = """
▐\033[7m  A B C D E F G H  \033[0m▌
▐\033[7m8\033[27m\033[4m▌♜│♞│♝│♛│♚│♝│♞│♜▐\033[24m\033[7m8\033[0m▌
▐\033[7m7\033[27m\033[4m▌♟│♟│♟│♟│♟│♟│♟│♟▐\033[24m\033[7m7\033[0m▌
▐\033[7m6\033[27m\033[4m▌ │ │ │ │ │ │ │ ▐\033[24m\033[7m6\033[0m▌
▐\033[7m5\033[27m\033[4m▌ │ │ │ │ │ │ │ ▐\033[24m\033[7m5\033[0m▌
▐\033[7m4\033[27m\033[4m▌ │ │ │ │ │ │ │ ▐\033[24m\033[7m4\033[0m▌
▐\033[7m3\033[27m\033[4m▌ │ │ │ │ │ │ │ ▐\033[24m\033[7m3\033[0m▌
▐\033[7m2\033[27m\033[4m▌♙│♙│♙│♙│♙│♙│♙│♙▐\033[24m\033[7m2\033[0m▌
▐\033[7m1\033[27m\033[4m▌♖│♘│♗│♕│♔│♗│♘│♖▐\033[24m\033[7m1\033[0m▌
▐\033[7m  A B C D E F G H  \033[0m▌

"""


class TestBoard:
    """Unit tests for the board."""

    def test_board(self):
        """Test initial state of the board."""
        from src.board import Board

        assert str(Board()) == initial_board_state

    def test_square(self):
        """Test piece referencing on the board."""
        from src.board import Board

        board = Board()

        for rank in board._board:
            for piece in rank:
                assert board[board.square_of(piece)] is piece

    def test_square_operations(self):
        """Test that squares can safely be operated on and that operations can be stacked."""
        from src.square import Vector, Square

        north = Vector(-1, 0)
        west = Vector(0, -1)
        south = Vector(+1, 0)
        east = Vector(0, +1)

        square = Square("e4")

        assert square + north == Square("e5")
        assert square + west == Square("d4")
        assert square + south == Square("e3")
        assert square + east == Square("f4")
