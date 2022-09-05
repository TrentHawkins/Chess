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

        assert repr(Board()) == initial_board_state

    def test_board_piece_relations(self):
        """Test the various logical conditions imposed at board level."""
        from src.board import Board

        board = Board()

        source = board["h1"]
        friend = board["h2"]
        foe = board["h8"]

    #   Pylance, stop whining already!
        assert source
        assert friend
        assert foe

        assert source.has_friend(friend)
        assert not source.has_friend(foe)
        assert not source.has_foe(friend)
        assert source.has_foe(foe)

    def test_move(self):
        """Test legal moves on initial board."""
        from src.board import Board
        from src.square import Square

        board = Board()

        assert board.moves == {
            Square("a1"): set(),
            Square("b1"): {Square("a3"), Square("c3")},  # Knight!
            Square("c1"): set(),
            Square("d1"): set(),
            Square("e1"): set(),
            Square("f1"): set(),
            Square("g1"): {Square("f3"), Square("h3")},  # Knight!
            Square("h1"): set(),
            Square("a2"): {Square("a3"), Square("a4")},  # Pawn.
            Square("b2"): {Square("b3"), Square("b4")},  # Pawn.
            Square("c2"): {Square("c3"), Square("c4")},  # Pawn.
            Square("d2"): {Square("d3"), Square("d4")},  # Pawn.
            Square("e2"): {Square("e3"), Square("e4")},  # Pawn.
            Square("f2"): {Square("f3"), Square("f4")},  # Pawn.
            Square("g2"): {Square("g3"), Square("g4")},  # Pawn.
            Square("h2"): {Square("h3"), Square("h4")},  # Pawn.
            Square("a8"): set(),
            Square("b8"): {Square("a6"), Square("c6")},  # Knight!
            Square("c8"): set(),
            Square("d8"): set(),
            Square("e8"): set(),
            Square("f8"): set(),
            Square("g8"): {Square("f6"), Square("h6")},  # Knight!
            Square("h8"): set(),
            Square("a7"): {Square("a6"), Square("a5")},  # Pawn.
            Square("b7"): {Square("b6"), Square("b5")},  # Pawn.
            Square("c7"): {Square("c6"), Square("c5")},  # Pawn.
            Square("d7"): {Square("d6"), Square("d5")},  # Pawn.
            Square("e7"): {Square("e6"), Square("e5")},  # Pawn.
            Square("f7"): {Square("f6"), Square("f5")},  # Pawn.
            Square("g7"): {Square("g6"), Square("g5")},  # Pawn.
            Square("h7"): {Square("h6"), Square("h5")},  # Pawn.
        }


class TestSquare:
    """Unit tests exclusive to the squares."""

    def test_square_operations(self):
        """Test that squares can safely be operated on and that operations can be stacked."""
        from src.square import Square, Vector

        assert Square("e4") + Vector(-1, 0) == Square("e5")
        assert Square("e4") + Vector(0, -1) == Square("d4")
        assert Square("e4") + Vector(+1, 0) == Square("e3")
        assert Square("e4") + Vector(0, +1) == Square("f4")


