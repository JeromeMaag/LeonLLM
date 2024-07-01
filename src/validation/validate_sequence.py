import chess  # type: ignore
import src.notation_converter as converter
from src.generate_prediction import generate_batch_predictions
from IPython.display import display, clear_output
from time import sleep


CASTLING_MOVES = {"Ke1g1", "Ke1c1", "Ke8g8", "Ke8c8"}


def is_valid_move_pawn(move, color, number_of_plies_until_error):
    """
    Checks if the pawn's move is valid.

    Args:
        move (str): The move string in xLAN-format, e.g. 'Pe2e4'.
        color (chess.Color/bool): The color of the moving player (chess.WHITE or chess.BLACK).

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    multiplier = 1 if number_of_plies_until_error % 2 == 0 else -1

    origin_file, origin_rank, target_file, target_rank = (
        move[1],
        int(move[2]),
        move[3],
        int(move[4]),
    )
    file_difference = ord(target_file) - ord(origin_file)
    rank_difference = target_rank - origin_rank

    # A pawn moves straight forward one rank
    if file_difference == 0 and rank_difference == 1 * multiplier:
        return True
    # A pawn moves straight forward two ranks from its initial position
    elif (
        origin_rank in (2, 7)
        and file_difference == 0
        and rank_difference == 2 * multiplier
    ):
        return True
    # A pawn captures diagonally one rank forward
    elif abs(file_difference) == 1 and rank_difference == 1 * multiplier:
        return True

    return False


def is_valid_move_rook(move):
    """
    Checks if the rook's move is valid.

    Args:
        move (str): The move string in xLAN-format, e.g. 'Pe2e4'.

    Returns:
        bool: True if the move is valid, False otherwise.
    """

    origin_file, origin_rank, target_file, target_rank = (
        move[1],
        move[2],
        move[3],
        move[4],
    )

    # A rook moves along the same file (different ranks) or the same rank (different files).
    return (origin_file == target_file and origin_rank != target_rank) or (
        origin_file != target_file and origin_rank == target_rank
    )


def is_valid_move_king(move):
    """
    Checks if the king's move is valid, including castling.

    Args:
        move (str): The move string in xLAN-format, e.g. 'Pe2e4'.

    Returns:
        bool: True if the move is valid, False otherwise.
    """

    origin_file, origin_rank, target_file, target_rank = (
        move[1],
        int(move[2]),
        move[3],
        int(move[4]),
    )

    # Calculate the difference in file and rank.
    file_difference = abs(ord(target_file) - ord(origin_file))
    rank_difference = abs(target_rank - origin_rank)

    # Check for standard king move or castling.
    is_standard_move = file_difference in [0, 1] and rank_difference in [0, 1]
    is_castling_move = move[:5] in CASTLING_MOVES

    return is_standard_move or is_castling_move


def is_valid_move_bishop(move):
    """
    Checks if the bishop's move is valid, which must be diagonal.

    Args:
        move (str): The move string in xLAN-format, e.g. 'Pe2e4'.

    Returns:
        bool: True if the move is valid, False otherwise.
    """

    origin_file, origin_rank, target_file, target_rank = (
        move[1],
        int(move[2]),
        move[3],
        int(move[4]),
    )

    # A bishop moves diagonally, so the change in file should be equal to the change in rank.
    return abs(ord(origin_file) - ord(target_file)) == abs(origin_rank - target_rank)


def is_valid_move_knight(move):
    """
    Checks if the knight's move is valid, which must be an 'L' shape.

    Args:
        move (str): The move string in xLAN-format, e.g. 'Pe2e4'.

    Returns:
        bool: True if the move is valid, False otherwise.
    """

    origin_file, origin_rank, target_file, target_rank = (
        move[1],
        int(move[2]),
        move[3],
        int(move[4]),
    )

    # Calculate the absolute difference in file and rank.
    file_difference = abs(ord(origin_file) - ord(target_file))
    rank_difference = abs(origin_rank - target_rank)

    # Check for 'L' shaped movement: 2 by 1 or 1 by 2 squares.
    return (file_difference == 1 and rank_difference == 2) or (
        file_difference == 2 and rank_difference == 1
    )


def target_square_is_obstructed_by_own_piece(board, color, target_square):
    """
    Checks if the target square of a move is occupied by a piece of the same color.

    Args:
        board (chess.Board): The current state of the chess board.
        color (chess.Color/bool): The color of the moving player (chess.WHITE or chess.BLACK).
        target_square (int): The target square in chess.Square format.

    Returns:
        bool: True if the target square is occupied by a piece of the same color, False otherwise.
    """

    piece_at_target = board.piece_at(target_square)
    return piece_at_target and piece_at_target.color == color


def is_path_obstructed(board, from_square, target_square):
    """
    Checks for any obstruction in the path of a move or at the target square.

    Args:
        board (chess.Board): The current state of the chess board.
        from_square (int): The starting square in chess.Square format.
        target_square (int): The target square in chess.Square format.

    Returns:
        bool: True if there's an obstruction in the path, False otherwise.
    """

    for square in chess.SquareSet.between(from_square, target_square):
        if board.piece_at(square):
            return True

    return False


def is_path_obstructed_pawn(board, move, color, target_square):
    """
    Validates a pawn's move, considering obstructions and movement rules.

    Args:
        board (chess.Board): The current state of the chess board.
        move (str): The move string in xLAN-format, e.g. 'Pe2e4'.
        color (chess.Color/bool): The color of the moving player (chess.WHITE or chess.BLACK).
        target_square (int): The target square in chess.Square format.

    Returns:
        bool: True if there's an obstruction in the path, False otherwise.
    """

    origin_file, target_file = (move[1], move[3])
    file_difference = abs(ord(origin_file) - ord(target_file))

    tmp = board.pop()

    target_square_is_obstructed = board.piece_at(target_square)

    board.push(tmp)

    # Pawns move straight forward without capture or diagonally forward with capture
    if target_square_is_obstructed_by_own_piece(board, color, target_square) or (
        file_difference == 0 and target_square_is_obstructed
    ):
        return True
    return False


def update_evaluation(
    debug,
    evaluation,
    game,
    number_of_plies_until_error,
    error_type,
    move,
    game_moves,
    token_sequence,
):
    """
    Updates the evaluation list.
    Evaluation list contains tuples of (game_as_string, number_of_moves_until_error, error_type, first_illegal_move).

    Args:
        debug (bool): If True, the board is displayed after each move.
        evaluation (list): The list of tuples containing (game_as_string, number_of_moves_until_error, error_type).
        game (str): The game string in xLAN format.
        number_of_plies_until_error (int): The number of plies until an error occurred.
        error_type (str): The type of error that occurred.
        move (str): The move string in xLAN-format, e.g. 'Pe2e4'.
    """

    if debug:
        print(f"wrong move: {move}")
        print(f"error type: {error_type}")
        print(f"number of correct moves until error: {number_of_plies_until_error}")

    evaluation.append(
        (
            game,
            number_of_plies_until_error,
            error_type,
            " ".join(game_moves[: (number_of_plies_until_error + 1)]),
            token_sequence,
        )
    )


def get_error_category(
    game_moves, error_move, number_of_plies_until_error, board, notation="xLAN"
):
    """
    Returns the error category of a move.

    Args:
        game_moves (list): The list of moves in xLAN format.
        error_move (str): The move string in xLAN-format, e.g. 'Pe2e4'.
        number_of_plies_until_error (int): The number of plies until an error occurred.
        board (chess.Board): The current state of the chess board.
        notation (str): The notation used for the game sequences.

    Returns:
        error_type (str): The type of error that occurred.
    """
    try:
        if number_of_plies_until_error == len(game_moves):
            return "max length"
        if board.outcome():
            # check for different endings and corresponding fourth token
            if notation == "xLANplus" or notation == "xLANchk" or notation == "xLANcap":
                indicator = error_move[5]
                parsed_move = chess.Move.from_uci(
                    converter.xlan_move_to_uci(board, error_move[:5])
                )
                return (
                    "indicator error"
                    if not checkIndicator(board, indicator, parsed_move, notation)
                    else "no error"
                )
        elif not (check_syntax(error_move, notation)):
            return "syntax"
        else:
            color = chess.WHITE if board.turn else chess.BLACK
            piece_type = get_piece_type(error_move)
            plus_notation = (
                notation == "xLANplus" or notation == "xLANchk" or notation == "xLANcap"
            )

            error_move_uci = (
                converter.xlanplus_move_to_uci(board, error_move)[0]
                if notation == "xLANplus"
                else converter.xlan_move_to_uci(board, error_move)
            )

            if not piece_type:
                return "syntax"

            if is_piece_logic_error(
                error_move, color, piece_type, number_of_plies_until_error
            ):
                return "piece logic"

            if is_path_obstruction_error(error_move, color, piece_type, board):
                return "path obstruction"

            elif (
                chess.Move.from_uci(error_move_uci) in board.pseudo_legal_moves
                or error_move[:5] in CASTLING_MOVES
            ):
                return "pseudolegal"

            elif plus_notation:
                indicator = error_move[5]
                error_move = error_move[:5]
                try:
                    move = converter.xlan_move_to_uci(board, error_move)
                    parsed_move = chess.Move.from_uci(move)
                    start_square = parsed_move.from_square
                    board.pop()
                    piece_at_start = board.piece_at(start_square)
                    board.push(parsed_move)
                    if str(piece_at_start).lower() != error_move[0].lower():
                        return "pseudolegal"
                    if not checkIndicator(board, indicator, parsed_move):
                        return "indicator error"
                    else:
                        return "pseudolegal"
                except Exception as e:
                    print(f"e: {e}")
                    return "pseudolegal"
            else:
                return "pseudolegal"
    except:
        return "unknown error"


def get_piece_type(move):
    """
    Returns the piece type of a move.

    Args:
        move (str): The move string in xLAN-format, e.g. 'Pe2e4'.

    Returns:
        piece_type (chess.PieceType): The piece type of the move.
    """

    try:
        return chess.Piece.from_symbol(move[0]).piece_type
    except:
        return None


def is_piece_logic_error(move, color, piece_type, number_of_plies_until_error):
    """
    Checks if the move follows the rules of the piece.

    Args:
        move (str): The move string in xLAN-format, e.g. 'Pe2e4'.
        color (chess.Color/bool): The color of the moving player (chess.WHITE or chess.BLACK).
        piece_type (chess.PieceType): The piece type of the move.

    Returns:
        bool: True if the move is not valid, False otherwise.
    """

    if piece_type == chess.PAWN:
        if not is_valid_move_pawn(move, color, number_of_plies_until_error):
            return True

    elif piece_type == chess.KNIGHT:
        if not is_valid_move_knight(move):
            return True

    elif piece_type == chess.BISHOP:
        if not is_valid_move_bishop(move):
            return True

    elif piece_type == chess.ROOK:
        if not is_valid_move_rook(move):
            return True

    elif piece_type == chess.QUEEN:
        if not (is_valid_move_rook(move) or is_valid_move_bishop(move)):
            return True

    elif piece_type == chess.KING:
        if not is_valid_move_king(move):
            return True
    else:
        return True

    return False


def is_path_obstruction_error(move, color, piece_type, board):
    """
    Checks if there is a path obstruction in the move or
    if the target square is occupied by a piece of the same color.

    Args:
        move (str): The move string in xLAN-format, e.g. 'Pe2e4'.
        color (chess.Color/bool): The color of the moving player (chess.WHITE or chess.BLACK).
        piece_type (chess.PieceType): The piece type of the move.
        board (chess.Board): The current state of the chess board.

    Returns:
        bool: True if the move is not valid, False otherwise.
    """

    from_square = chess.parse_square(move[1:3])
    target_square = chess.parse_square(move[3:5])
    if target_square_is_obstructed_by_own_piece(board, color, target_square):
        return True

    if is_path_obstructed(board, from_square, target_square):
        return True

    if piece_type == chess.PAWN:
        if is_path_obstructed_pawn(board, move, color, target_square):
            return True

    return False


def check_syntax(move, notation="xLAN"):
    """
    Checks if the move string is in the correct format.

    Args:
        move (str): The move string in xLAN-format, e.g. 'Pe2e4'.
        notation (str): The notation used for the game sequences.

    Returns:
        bool: True if the move is in the correct format, False otherwise.
    """
    plus_notation = (
        notation == "xLANplus" or notation == "xLANchk" or notation == "xLANcap"
    )
    if move == "" or len(move) != (5 if not plus_notation else 6):
        return False
    piece = move[0]
    origin_sqare = move[1:3]
    target_square = move[3:5]
    if plus_notation:
        indicator = move[5]
        if indicator not in ["-", "x", "+", "$", "!", "#"]:
            return False

    is_piece = piece in ["K", "Q", "R", "B", "N", "P"]
    is_sqare_origin = origin_sqare in chess.SQUARE_NAMES
    is_sqare_target = target_square in chess.SQUARE_NAMES

    return is_piece and is_sqare_origin and is_sqare_target


def get_legal_sequence_length(debug, game_moves, notation="xLAN"):
    """
    Returns the number of plies until an error occurs. If no error occurs, the number of plies is equal to the length of the game.

    Args:
        debug (bool): If True, the board is displayed after each move.
        game_moves (list): The list of moves in xLAN format.
        notation (str): The notation used for the game sequences.

    Returns:
        move (str): The move string from which the error occurred in xLAN-format, e.g. 'Pe2e4'.
        number_of_plies_until_error (int): The number of plies until an error occurred.
        board (chess.Board): The current state of the chess board.
    """
    number_of_plies_until_error = 0
    board = chess.Board()
    move = ""
    plus_notation = (
        notation == "xLANplus" or notation == "xLANchk" or notation == "xLANcap"
    )

    for move in game_moves:
        if plus_notation:
            uci_move, indicator = converter.xlanplus_move_to_uci(board, move)
        else:
            uci_move = converter.xlan_move_to_uci(board, move)
            indicator = None
        try:
            parsed_move = chess.Move.from_uci(uci_move)
        except:
            break
        if parsed_move in board.legal_moves:
            board.push(parsed_move)
            if not checkIndicator(board, indicator, parsed_move, notation):
                break
            number_of_plies_until_error += 1
        else:  # move is not legal
            break

        if debug:
            clear_output(wait=True)
            display(board)
            sleep(0.05)

        if board.outcome():
            break
    return move, number_of_plies_until_error, board


def checkIndicator(board, indicator, move, notation="xLANplus"):
    """
    Checks if the indicator is correct.

    Args:
        board (chess.Board): The current state of the chess board.
        indicator (str): The indicator of the move in xLAN+ format.
        move (chess.Move): The move in UCI format.
        notation (str): The notation used for the game sequences.

    Returns:
        bool: True if the indicator is correct, False otherwise.
    """
    if notation == "xLAN":
        return True
    check = board.is_check()
    checkmate = board.is_checkmate()
    move_tmp = board.pop()
    capture = board.is_capture(move_tmp)
    board.push(move_tmp)
    if notation == "xLANchk":
        capture = False
    if notation == "xLANcap":
        check = False
        checkmate = False
    if checkmate:
        if capture:
            return indicator == "!"
        else:
            return indicator == "#"
    elif check:
        if capture:
            return indicator == "$"
        else:
            return indicator == "+"
    else:
        if capture:
            return indicator == "x"
        else:
            return indicator == "-"


def evaluate_sequence(game_sequences, token_sequences, debug=False, notation="xLAN"):
    """
    Evaluates sequences of tokens of an aritrary number of chess games.
    The moves in each generated sequence are evaluated until a wrong move is made or the game ends.

    Error types:
        *Syntax:* Move does not correspond to {piece}{start_square}-{end_square}. This error indicates failure at producing correct tokens.
        *Piece Logic:* Piece moves in an invalid way. This error indicates failure at learning how pieces move.
        *Path Obstruction:* Move ignores other pieces that prevent this move. This error indicates failure at keeping track of the board state.
        *Pseudolegal:* Everything else. This error indicates failure at keeping track of the board state.
            * castling through check,
            * castling when not available,
            * moving king into check,
            * moving pinned piece,
            * not moving out of check,
            * etc.
        *Indicator Error:* The indicator does not match the move.
        *Max Length:* The game reached the max sequence length.
        *No Error:* The game ended without any errors.

    Args:
        game_sequences (list): The list of games in xLAN format.
        token_sequences (list): The list of token sequences corresponding to the games.
        debug (bool): If True, the board is displayed after each move.
        notation (str): The notation used for the game sequences.

    Return:
        evaluation (list): The list of tuples containing (game_as_string, number_of_moves_until_error, error_type , first_illegal_move).
    """

    evaluation = []

    for game in game_sequences:
        if not len(token_sequences) == 0:
            token_sequence = token_sequences[game_sequences.index(game)]
        game_moves = game.split()

        (
            error_move,
            number_of_plies_until_error,
            board,
        ) = get_legal_sequence_length(debug, game_moves, notation)
        if debug:
            print(f"error_move: {error_move}")
            print(f"number_of_plies_until_error: {number_of_plies_until_error}")
            print(f"board: {board}")

        error_type = get_error_category(
            game_moves, error_move, number_of_plies_until_error, board, notation
        )

        update_evaluation(
            debug,
            evaluation,
            game,
            number_of_plies_until_error,
            error_type,
            error_move,
            game_moves,
            token_sequence,
        )
    if debug:
        print(f"evaluation: {evaluation}")

    return evaluation


def analyze_evaluation(evaluation, xLanPlus=False):
    """
    Analyzes the evaluation of a sequence of tokens.

    Args:
        evaluation (list): The list of tuples containing (game_as_string, number_of_moves_until_error, error_type , first_illegal_move).

    Returns:
        average_number_of_moves_until_error (float): The average number of moves until an error occurred.
        error_frequencies (list): A list of tuples containing (error_type, frequency).
    """

    number_of_games = len(evaluation)
    error_counts = {}

    average_number_of_moves_until_error = (
        sum([game[1] for game in evaluation]) / number_of_games
    )
    for _, _, error_type, _, _ in evaluation:
        if error_type in error_counts:
            error_counts[error_type] += 1
        else:
            error_counts[error_type] = 1

    error_frequencies = [
        (error_type, count / number_of_games)
        for error_type, count in error_counts.items()
    ]

    return average_number_of_moves_until_error, error_frequencies


def validate_sequence(
    model,
    number_of_games=500,
    number_of_plies_to_generate=170,
    input_prefix="",
    max_batch_size=30,
    seed=1,
    tokens_per_ply=3,
    notation="xLANplus",
    left_padding=False,
):
    """
    Generates a batch of predictions and evaluates the generated sequences.

    Args:
        model (Model): The chess model to be evaluated.
        number_of_games (int): The number of games to be generated.
        number_of_plies_to_generate (int): The number of plies to be generated for each game.
        input_prefix (str): The input prefix to be used for generation.
        max_batch_size (int): The maximum batch size for generation.
        seed (int): The seed to be used for generation.
        tokens_per_ply (int): Number of tokens to generate per ply.
        left_padding (bool): If True, the model uses left padding.

    Returns:
        average_correct_plies (float): The average number of correct plies in the generated sequences.
        error_frequencies (list): A list of tuples containing (error_type, frequency).
        evaluation (list): The list of tuples containing (game_as_string, number_of_moves_until_error, error_type , first_illegal_move).
    """
    output_batch, tokens_batch, _ = generate_batch_predictions(
        inputs=[input_prefix] * number_of_games,
        num_tokens_to_generate=number_of_plies_to_generate * tokens_per_ply,
        model=model,
        notation=notation,
        temperature=0.7,
        seed=seed,
        max_batch_size=max_batch_size,
        left_side_padding=left_padding,
    )
    evaluation = evaluate_sequence(
        game_sequences=output_batch,
        token_sequences=tokens_batch,
        debug=False,
        notation=notation,
    )

    average_correct_plies, error_frequencies = analyze_evaluation(evaluation)

    return average_correct_plies, error_frequencies, evaluation
