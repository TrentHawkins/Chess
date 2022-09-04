from src.chess import Chess


if __name__ == "__main__":
    chess = Chess()
    score, winner = chess.run()
    print(score, winner)
