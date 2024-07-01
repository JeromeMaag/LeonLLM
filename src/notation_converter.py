import chess  #  type: ignore


def xlan_move_to_uci(board, move):
    """
    Converts a move from xLAN to UCI (Universal Chess Interface) format.
    Handles pawn promotions by checking if a pawn reaches the back rank and should be promoted.
    Removes piece identifiers from the move, e.g. 'Pe2e4' becomes 'e2e4'.

    Args:
    board (chess.Board): The current board position.
    move (str): The move in xLAN to be converted, expected in the format of 'Pe2e4' or similar.

    Returns:
    str: The move in UCI format, like 'e2e4', or 'e7e8=Q' for pawn promotion to a queen.
    """
    if len(move) < 4:
        return move
    if move[0] in ["Q", "B", "N", "R"]:
        if move[2] in ["7", "2"]:
            print("squares_no_parse", move[1] + move[2])
            piece = board.piece_at(chess.parse_square(move[1] + move[2]))
            print("piece", piece)
            if piece and piece.piece_type == chess.PAWN:
                # Return the move in UCI format with promotion to the indicated piece
                return move[1:] + move[0].lower()

    if move[0] in ["Q", "P", "B", "N", "K", "R"]:
        return move[1:]
    return move


def xlanplus_move_to_uci(board, move):
    """
    Converts a move from xLAN+ to UCI (Universal Chess Interface) format.
    Uses xlan_move_to_uci to handle pawn promotions and remove piece identifiers from the move.

    Args:
    board (chess.Board): The current board position.
    move (str): The move in xLAN+ to be converted, expected in the format of 'Pe2e4-' or similar.

    Returns:
    str: The move in UCI format, like 'e2e4', or 'e7e8=Q' for pawn promotion to a queen.
    """
    indicator = move[-1].strip()
    move = xlan_move_to_uci(board, move)
    return move, indicator


def uci_move_to_xlan(board, move):
    """
    Converts a move from UCI (Universal Chess Interface) format to unique xLAN format.
    Handles pawn promotions by checking if last character is a piece, e.g. 'e7e8q'. becomes 'Qe7e8'.
    Adds piece identifiers to the move, e.g. 'e2e4' becomes 'Pe2e4'.

    Args:
    move (str): The move to be converted, expected in the format of 'e2e4' or similar.

    Returns:
    str: The move in xLAN format, like 'Pe2e4', or 'Qe7e8' for pawn promotion to a queen.
    """
    piece = board.piece_at(chess.parse_square(move[0] + move[1]))
    if len(move) == 5:
        piece = move[4].upper()
        return piece + move[:4]
    return piece.symbol().upper() + move[:4]


def xlan_sequence_to_uci(moves_string):
    """
    Converts a string of moves from unique xLAN format to UCI format.

    Args:
    moves_string (str): A string containing moves in xLAN separated by spaces, e.g., "Pe2e4 Pe7e5 Ng1f3"

    Returns:
    str: The string of moves in UCI format, e.g., "e2e4 e7e5 g1f3"
    """
    board = chess.Board()
    moves = moves_string.split()
    uci_moves = []
    for move in moves:
        uci_move = xlan_move_to_uci(board, move)
        uci_moves.append(uci_move)
        board.push(chess.Move.from_uci(uci_move))

    return " ".join(uci_moves)


def uci_sequence_to_xlan(moves_string):
    """
    Converts a string of moves from UCI format to unique xLAN.

    Args:
    moves_string (str): A string containing moves separated by spaces, e.g., "e2e4 e7e5 g1f3"

    Returns:
    str: The string of moves in unique xLAN format, e.g., "Pe2e4 Pe7e5 Ng1f3"
    """
    board = chess.Board()
    moves = moves_string.split()
    xlan_moves = []
    for move in moves:
        xlan_move = uci_move_to_xlan(board, move)
        xlan_moves.append(xlan_move)
        board.push(chess.Move.from_uci(move))

    return " ".join(xlan_moves)


def legal_moves_from_position(moves_string, uci=False):
    """
    Returns the legal moves from a given position in xLAN or UCI format. Automatically detects if input is xLAN or xLAN+.

    Args:
    moves_string (str): A string containing moves separated by spaces, e.g., "Pe2e4 Pe7e5 Ng1f3"
    uci (bool): Whether to return the moves in UCI format or xLAN format. True for UCI, False for xLAN.

    Returns:
    list: A list of legal moves in xLAN or UCI format.
    """
    xlanplus = False
    if moves_string.find("-") != -1:
        xlanplus = True
    board = chess.Board()
    if xlanplus:
        moves_string = xlanplus_sequence_to_xlan(moves_string)
    uci_sequence = xlan_sequence_to_uci(moves_string)
    moves = uci_sequence.split()
    for move in moves:
        board.push(chess.Move.from_uci(move))

    legal_moves = board.legal_moves
    legal_moves_uci = [move.uci() for move in legal_moves]
    if uci:
        return legal_moves_uci
    legal_moves_xlan = []
    for move in legal_moves_uci:
        move = uci_sequence_to_xlan(uci_sequence + " " + move)
        if xlanplus:
            move = xlan_sequence_to_xlanplus(move)
        legal_moves_xlan.append(move.split()[-1])

    return legal_moves_xlan


def positions_of_piece(moves_string, piece):
    """
    Returns the positions of a given piece from a position in xLAN.

    Args:
    moves_string (str): A string containing xLAN moves separated by spaces, e.g., "Pe2e4 Pe7e5 Ng1f3"
    piece (str): The piece to find, e.g., "P" for pawn, "N" for knight, etc.

    Returns:
    list: A list of positions of the given piece, e.g., ["e2", "e4"] for white pawns.
    """

    board = chess.Board()
    uci_sequence = xlan_sequence_to_uci(moves_string)
    moves = uci_sequence.split()
    for move in moves:
        board.push(chess.Move.from_uci(move))

    squares = board.pieces(chess.Piece.from_symbol(piece).piece_type, board.turn)
    return [chess.square_name(square) for square in squares]


def positions_of_piece_with_legal_moves(moves_strig, piece):
    """
    Returns the positions a given piece that could move from a position in xLAN format.

    Args:
    moves_string (str): A string in xLAN containing moves separated by spaces, e.g., "Pe2e4 Pe7e5 Ng1f3"
    piece (str): The piece to find, e.g., "P" for pawn, "N" for knight, etc.

    Returns:
    list: A list of positions of the given piece which could move, e.g., ["e2", "e4"] for white pawns.
    """
    legal_moves = legal_moves_from_position(moves_strig, uci=False)
    positions = []
    for move in legal_moves:
        if move[0] == piece:
            positions.append(move[1:3])

    # Remove duplicates
    positions = list(dict.fromkeys(positions))
    return positions


def end_positions_of_piece_with_legal_moves(moves_string, piece, start_square):
    """
    Returns the end positions of a given piece that could move from a position in xLAN format.

    Args:
    moves_string (str): A string in xLAN containing moves separated by spaces, e.g., "Pe2e4 Pe7e5 Ng1f3"
    piece (str): The piece to find, e.g., "P" for pawn, "N" for knight, etc.
    start_square (str): The square the piece starts on, e.g., "e2" for a white pawn.

    Returns:
    list: A list of end positions of the given piece which could move, e.g., ["e4"] for a white pawn.
    """
    legal_moves = legal_moves_from_position(moves_string, uci=False)
    end_positions = []
    for move in legal_moves:
        if move[0] == piece and move[1:3] == start_square:
            end_positions.append(move[3:5])

    # Remove duplicates
    end_positions = list(dict.fromkeys(end_positions))
    return end_positions


def xlan_sequence_to_xlanplus(xlan_sequence):
    """
    Converts a string of moves from unique xLAN format to xLAN+ format.

    Args:
    xlan_sequence (str): A string containing moves in xLAN separated by spaces, e.g., "Pe2e4 Pe7e5 Ng1f3"

    Returns:
    str: The string of moves in xLAN+ format, e.g., "Pe2e4- Pe7e5- Ng1f3"
    """
    uci = xlan_sequence_to_uci(xlan_sequence)
    uci_moves = uci.split()
    xlan_moves = xlan_sequence.split()
    board = chess.Board()

    counter = 0  # Counter for the number of moves
    for uci_move in uci_moves:
        move = chess.Move.from_uci(uci_move)
        capture = board.is_capture(move)
        board.push(move)  # Make the move
        mate = board.is_checkmate()
        check = board.is_check()
        suffix = ""
        if check:
            suffix = "+" if not capture else "$"
        elif mate:
            suffix = "#" if not capture else "!"
        elif capture:
            suffix = "x"
        else:
            suffix = "-"
        xlan_moves[counter] += suffix
        counter += 1

    return " ".join(xlan_moves)


def xlanplus_sequence_to_xlan(xlanplus_sequence):
    """
    Converts a string of moves from xLAN+ format to unique xLAN format.

    Args:
    xlanplus_sequence (str): A string containing moves in xLAN+ separated by spaces, e.g., "Pe2e4- Pe7e5- Ng1f3"

    Returns:
    str: The string of moves in unique xLAN format, e.g., "Pe2e4 Pe7e5 Ng1f3"
    """
    xlanplus_moves = xlanplus_sequence.split()
    xlan_moves = []
    for move in xlanplus_moves:
        move = move[:-1]
        xlan_moves.append(move)

    return " ".join(xlan_moves)


def xlanplus_sequence_to_uci(xlanplus_sequence):
    """
    Converts a string of moves from xLAN+ format to UCI format.

    Args:
    xlanplus_sequence (str): A string containing moves in xLAN+ separated by spaces, e.g., "Pe2e4- Pe7e5- Ng1f3"

    Returns:
    str: The string of moves in UCI format, e.g., "e2e4 e7e5 g1f3"
    """
    xlan_sequence = xlanplus_sequence_to_xlan(xlanplus_sequence)
    return xlan_sequence_to_uci(xlan_sequence)
