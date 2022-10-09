"""This is it folks. Lets play."""

from sys import argv

from src.chess import Chess

if __name__ == "__main__":
    try:
        new_game = Chess(argv[1])

    except IndexError:
        new_game = Chess()

#   Main game loop:
#   Game engine can properly detect this from the abstract game rules, will wrap it in this class later.

    while not new_game.termination:
        new_game.turn()
