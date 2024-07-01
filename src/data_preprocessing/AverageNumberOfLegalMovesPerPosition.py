import chess
import chess.pgn
import os


def average_legal_moves_per_game(game):
    """
    Calculates the average number of legal moves per position in a game.

    Results of experiments:
        schmila7, 2023-10-23:
        The analysis of 21255 games in "lichess_elite_2016-12.pgn" (source: https://database.nikonoel.fr/) shows that the average number of legal moves per position is 30.8.
        The analysis of 3400418 games in "lichess_db_standard_rated_2015-10.pgn" (source: https://database.lichess.org/) shows that the average number of legal moves per position is 30.4.
    """

    board = game.board()
    legal_moves_count = []
    for move in game.mainline_moves():
        legal_moves_count.append(len(list(board.legal_moves)))
        board.push(move)
    return (
        sum(legal_moves_count) / len(legal_moves_count)
        if legal_moves_count
        else 0
    )


import os


def analyze_pgn_file(input_path):
    """
    Analyze a PGN file and return the average number of legal moves per game and the total number of games.
    """
    total_file_size = os.path.getsize(input_path)

    avg_legal_moves = []

    with open(input_path) as pgn:
        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break
            avg_legal_moves.append(average_legal_moves_per_game(game))

            # print progress to console
            current_file_position = pgn.tell()
            progress_percentage = (
                current_file_position / total_file_size
            ) * 100
            print(
                f"Processed: {progress_percentage:.2f}% of the input file",
                end="\r",
            )

    return {
        "average_moves": sum(avg_legal_moves) / len(avg_legal_moves)
        if avg_legal_moves
        else 0,
        "number_of_games": len(avg_legal_moves),
    }


if __name__ == "__main__":
    input_path = "./data/raw/lichess_db_standard_rated_2015-10.pgn"
    results = analyze_pgn_file(input_path)
    print(f"average number of legal moves: {results['average_moves']:.2f}")
    print(f"number of games processed = {results['number_of_games']}")
