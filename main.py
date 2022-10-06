"""This is it folks. Lets play."""

from src.chess import Chess

if __name__ == "__main__":
    new_game = Chess()

#   Main game loop:
#   Game engine can properly detect this from the abstract game rules, will wrap it in this class later.
    while not new_game.gameover:
        new_game.turn()
