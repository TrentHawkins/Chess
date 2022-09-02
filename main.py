from src.chess import Chess


if __name__ == "__main__":
    chess = Chess()
    score, color = chess.run()
    print(score, color)