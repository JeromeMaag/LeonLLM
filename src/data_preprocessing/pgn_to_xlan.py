import chess
import chess.pgn
import datetime
import logging
import os
import time
import multiprocessing


class pgn_to_xlan:
    """
    This class converts a PGN file with one or more games to a text file in an xLAN format.
    The typical LAN format has been slightly adjusted to our unique format xLAN,
    it so that we can use it later with a tokenizer for training a language model.

    Every move follows the format: {piece}{start_square}-{end_square}

    Exceptions:
        "+" and "#" are kept in the string, but they will later be ignored by the tokenizer.
        Castling is converted to the following format: {king}{start_square}{end_square}
        Promotion is converted to the following format: {goal_piece}+{start_square}-{end_square}

    Example:
        PGN:
            1. g3 e6 2. Bg2 Qf6 3. f4 Bc5 4. e4 Qd4 5. e5 Qf2# 0-1
        LAN:
            1. g2-g3 e7-e6 2. Bf1-g2 Qd8-f6 3. f2-f4 Bf8-c5 4. e2-e4 Qf6-d4 5. e4-e5 Qd4-f2# 0-1
        xLAN:
            1. Pg2-g3 Pe7-e6 2. Bf1-g2 Qd8-f6 3. Pf2-f4 Bf8-c5 4. Pe2-e4 Qf6-d4 5. Pe4-e5 Qd4-f2# 0-1

        xLAN+:
            1. Pg2g3- Pe7e6- 2. Bf1g2- Qd8f6- 3. Pf2f4- Bf8c5- 4. Pe2e4- Qf6d4- 5. Pe4e5- Qd4f2# 0-1

    Parameters:
        input_path: Path to the PGN file
        output_path: Path to the output file
        min_number_of_moves_per_game: Minimum number of moves in a game for it to be included in the output file, default is 10
        number_of_games: Number of games to include in the output file, default is -1 which processes all games
        chunk_size: Number of games to process at a time, to avoid memory issues, if necessary. If set to 0, all games will be processed at once.
        generate_all_moves: Whether to generate all possible moves for each game (WARNING: generates a lot of new data!). Default is False.
        xLanPlus: Whether to use the xLan+ format. Default is False.
        log: Whether to log the progress of the conversion. Default is False.
        filter_elo: Whether to filter games based on the ELO rating of the players. Default is False.
        elo_min: Minimum ELO rating of the players. Default is 0.
        elo_max: Maximum ELO rating of the players. Default is 4000.
    """

    def __init__(
        self,
        input_path,
        output_path,
        min_number_of_moves_per_game=10,
        number_of_games_to_write=-1,
        chunk_size=1000,
        generate_all_moves=False,
        xLanPlus=False,
        log=False,
        filter_elo=False,
        elo_min=0,
        elo_max=4000,
    ):
        self.input_path = input_path
        self.output_path = output_path
        self.min_number_of_moves_per_game = min_number_of_moves_per_game
        self.number_of_games_to_write = number_of_games_to_write
        self.chunk_size = chunk_size if chunk_size >= 0 else number_of_games_to_write
        self.generate_all_moves = generate_all_moves
        self.xLanPlus = xLanPlus
        self.log = log
        self.filter_elo = filter_elo
        self.elo_min = elo_min
        self.elo_max = elo_max

        self.number_of_games_processed = 0
        self.number_of_games_written = 0

        if self.log:
            self.setup_logging()

    def game_to_xlan(self, game):
        """
        Converts a game in PGN format to the xLAN format.

        Parameters:
            game: A game in PGN format.

        Yields:
            A string containing the game in the xLAN format.
        """
        if self.log:
            logging.info(f"game_to_xlan():")
        xlan_moves = []
        board = game.board()

        for index, move in enumerate(game.mainline_moves()):
            if self.generate_all_moves:
                for legal_move in board.legal_moves:
                    xlan = self.format_move(board, legal_move, index)
                    if xlan:
                        xlan_moves.append(xlan)
                        board.push(move)
                    processed_game = "".join(xlan_moves)
                    yield processed_game
                    self.number_of_games_written += 1
                    board.pop()
                    xlan_moves.pop()

            xlan = self.format_move(board, move, index)
            if xlan:
                xlan_moves.append(xlan)
                board.push(move)

        xlan_moves.append(game.headers["Result"])
        game_is_valid = self.is_valid_game(board)
        if self.log:
            logging.debug(f"\tgame_is_valid: {game_is_valid}")

        if not self.generate_all_moves and self.is_valid_game(board):
            processed_game = "".join(xlan_moves)
            yield processed_game
        elif not self.generate_all_moves and not self.is_valid_game(board):
            processed_game = ""
            yield processed_game

        self.game_logging(board, processed_game)

    def format_move(self, board, move, index):
        """
        Formats a move into LAN and then xLAN format (including move numbers).
        """
        turn_white = index % 2 == 0
        lan = board.lan(move)

        # Convert to adjusted xLAN format instead of standard LAN format
        xlan = self.move_lan_to_xlan(lan, turn_white)

        return f"{index // 2 + 1}. {xlan} " if turn_white else f"{xlan} "

    def move_lan_to_xlan(self, lan, turn_white):
        """
        Converts LAN move to xLAN format.
        Handles pawn moves, castling and promotions.
        """
        # Convert pawn moves
        xlan = lan
        if not lan[0].isupper():
            xlan = "P" + lan
        # Convert castling
        if "O" in lan:
            xlan = self.convert_castling(lan, turn_white)
        # Handle promotions
        if "=" in lan:
            xlan = self.convert_promotion(lan)

        if self.xLanPlus:
            xlan = self.convert_xlan_plus(xlan)
        return xlan

    def convert_xlan_plus(self, lan):
        """
        Converts xLAN to xLAN+ format, applying special markers for check, mate, and capture.
        """
        # Remove the dash and initialize the suffix for additional notation
        lan = lan.replace("-", "")
        suffix = ""

        # Determine the presence of check, mate, and capture, and prepare the suffix accordingly
        if "+" in lan:
            suffix = "+" if "x" not in lan else "$"
            lan = lan.replace("+", "")
        elif "#" in lan:
            suffix = "#" if "x" not in lan else "!"
            lan = lan.replace("#", "")
        elif "x" in lan:
            suffix = "x"
            lan = lan.replace("x", "")
        else:
            suffix = "-"

        # Remove capture notation if it hasn't been integrated into the suffix yet
        lan = lan.replace("x", "") if "x" not in suffix else lan

        return lan + suffix

    @staticmethod
    def convert_castling(lan, turn_white):
        """
        Converts castling moves to xLAN format.

        White's move:
            O-O -> Ke1g1
            O-O-O -> Ke1c1
        Black's move:
            O-O -> Ke8g8
            O-O-O -> Ke8c8
        """
        check_sign = "+" if "+" in lan else ""
        base_lan = lan.replace("+", "")
        castling_map = {
            "O-O": "Ke1g1" if turn_white else "Ke8g8",
            "O-O-O": "Ke1c1" if turn_white else "Ke8c8",
        }
        return castling_map.get(base_lan, lan) + check_sign

    @staticmethod
    def convert_promotion(lan):
        """
        Converts promotion moves to xLAN format.

        Example:
            Input = "Pd7-d8=Q+"
            Output = "Q+d7-d8"
        """
        lan, goal_piece = lan.split("=")
        return goal_piece + lan[1:] if lan[0].isupper() else goal_piece + lan

    def is_valid_game(self, board):
        """
        Checks if the game is valid based on the following conditions:
            The game has a minimum amount of moves (as defined in initialization of this class)
            The outcome of the game is not "None", meaning that the game has ended in checkmate or draw (by stalemate or move repetition), but not in timeout

        Further information:
            `Python Chess Documentation <https://python-chess.readthedocs.io/en/latest/core.html#outcome>`_
        """
        return (
            board.fullmove_number >= self.min_number_of_moves_per_game
            and board.outcome() is not None
        )

    def get_game_positions(self, pgn, num_games):
        """
        Gets the positions of the start of each game in the PGN file.
        """
        positions = [pgn.tell()]  # Startposition of first game
        current_game = 0
        # Search for the start of the next game
        while current_game < num_games:
            line = pgn.readline()
            if not line:
                # End of file reached
                break
            if line.strip() == "":
                # If there is an empty line, the next line contains the start of the next game
                pos = pgn.tell()
                line = (
                    pgn.readline()
                )  # Read next line to check if it is the start of a new game
                if line.startswith("["):
                    # Position is the start of a new game
                    positions.append(pos)
                    current_game += 1
        return positions

    def read_and_process_games_from_positions(self, positions):
        """
        Reads the games from the given positions and converts them to xLAN format.
        """
        buffer = []
        with open(self.input_path) as pgn:
            for pos in positions:
                pgn.seek(pos)
                game = chess.pgn.read_game(pgn)
                if game.headers["Termination"] == "Time forfeit":
                    continue
                if self.filter_elo:
                    headers = game.headers
                    white_elo = headers.get("WhiteElo", "?")
                    black_elo = headers.get("BlackElo", "?")

                    if white_elo == "?" and black_elo == "?":
                        continue

                    elos = [
                        int(white_elo) if white_elo != "?" else None,
                        int(black_elo) if black_elo != "?" else None,
                    ]
                    elos = [elo for elo in elos if elo is not None]
                    if not elos:
                        continue

                    average_elo = sum(elos) / len(elos)

                    if average_elo < self.elo_min or average_elo > self.elo_max:
                        continue
                for xlan_str in self.game_to_xlan(game):
                    if xlan_str:
                        buffer.append(xlan_str)
        return buffer

    def convert_pgn_parallel(self):
        """
        Converts all games in PGN file to xLAN format and writes to output file.
        Uses a buffer for more efficient writing to file.
        Uses multiprocessing and chunking to process the games in chunks.
        """
        start_time = self.start_logging()
        num_processes = multiprocessing.cpu_count()
        writen_games = 0
        with open(self.input_path) as pgn, open(self.output_path, "w") as outfile:
            while True:
                game_positions = self.get_game_positions(pgn, 100000)

                if not game_positions:
                    break

                chunk_size = len(game_positions) // num_processes

                if chunk_size == 0:
                    break

                chunks = [
                    game_positions[i : i + chunk_size]
                    for i in range(0, len(game_positions), chunk_size)
                ]

                with multiprocessing.Pool(num_processes) as pool:
                    results = pool.map(
                        self.read_and_process_games_from_positions, chunks
                    )

                for buffer in results:
                    outfile.write("\n".join(buffer))
                    outfile.write("\n")
                    writen_games += len(buffer)
                if (
                    self.number_of_games_to_write != -1
                    and writen_games >= self.number_of_games_to_write
                ):
                    break
                print(f"\tNumber of writen games: {writen_games}", end="\r")

        if self.log:
            self.final_logging(start_time)

    def convert_pgn(self):
        """
        Converts all games in PGN file to xLAN format and writes to output file.
        Uses a buffer for more efficient writing to file.
        """
        start_time = self.start_logging()

        buffer = []
        games_processed = 0

        with open(self.input_path) as pgn, open(self.output_path, "w") as outfile:
            total_file_size = os.path.getsize(self.input_path)

            while (self.number_of_games_to_write < 0) or (
                games_processed < self.number_of_games_to_write
            ):
                game = chess.pgn.read_game(pgn)

                # check for end of file
                if not game:
                    break

                if game.headers["Termination"] == "Time forfeit":
                    if self.log:
                        logging.debug(
                            f"\tgame #{self.number_of_games_processed} is a time forfeit"
                        )
                    continue
                else:
                    logging.debug(
                        f"\tgame #{self.number_of_games_processed} is not a time forfeit"
                    )

                self.number_of_games_processed += 1

                # print progress to console
                current_file_position = pgn.tell()
                progress_percentage = (current_file_position / total_file_size) * 100
                print(
                    f"\tProcessed: {progress_percentage:.2f}% of the input file",
                    end="\r",
                )
                self.progression_logging(game)

                for lan_str in self.game_to_xlan(game):
                    if lan_str:
                        buffer.append(lan_str)
                        games_processed += 1
                        self.number_of_games_written += 1

                # Write the buffer to the file if it reaches chunk size
                if len(buffer) == self.chunk_size:
                    outfile.write("\n".join(buffer))
                    buffer.clear()

            # write the remaining games in the buffer to the file
            if buffer:
                outfile.write("\n".join(buffer))
                buffer.clear()

        if self.log:
            self.final_logging(start_time)

    def san_to_xlan(self, san_game):
        """
        Converts a game in SAN format to the xLAN format.

        Parameters:
            san_game: A string containing a chess game in SAN format.

        Returns:
            A string containing the game in the xLAN format.
        """
        game = chess.pgn.Game()

        board = game.board()
        xlan = ""

        sequence = [move for move in san_game.split() if not move.endswith(".")]

        for san_move in sequence:
            move = board.parse_san(san_move)

            xlan_move = self.format_move(board, move, board.move_stack.__len__())
            xlan += xlan_move + " "

            # update board state
            board.push(move)
            game.add_main_variation(move)

        return xlan

    def setup_logging(self):
        """
        Sets up logging for the conversion.
        """
        if self.log:
            script_name = "PGNToxLANWithGeneratingAllMoves"
            current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = f"./logs/{script_name}_{current_time}.log"

            # Ensure the "debug" directory exists
            os.makedirs("./logs", exist_ok=True)

            logging.basicConfig(
                filename=log_filename,
                level=logging.DEBUG,
                format="%(asctime)s [DEBUG] %(message)s",
            )

            # Log configuration
            logging.info(f"{script_name}: __init__()")
            logging.info(f"\tInput file path = {self.input_path}")
            logging.info(f"\tOutput file path = {self.output_path}")
            logging.info(
                f"\tMinimum number of moves per game = {self.min_number_of_moves_per_game}"
            )
            logging.info(
                f"\tNumber of games to write = {self.number_of_games_to_write}"
            )
            logging.info(f"\tChunk size = {self.chunk_size}")
            logging.info(f"\tGenerate all moves = {self.generate_all_moves}")

    def final_logging(self, start_time):
        """
        Logs the time elapsed and other information about the conversion.

        Parameters:
            start_time: The time when the conversion started.
        """
        if self.log:
            end_time = time.time()
            elapsed_time = end_time - start_time
            if self.number_of_games_written > 0:
                estimated_time_for_one_million_games = (
                    elapsed_time / self.number_of_games_written * 1_000_000 / 60
                )
                logging.info(
                    f"Estimated time for 1'000'000 games = {estimated_time_for_one_million_games:.2f} minutes"
                )

            # PRINTING TIME ELAPSED

            logging.info(
                f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}"
            )
            logging.info(
                f"End time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}"
            )
            logging.info(f"Time elapsed: {elapsed_time:.2f} seconds")

            # PRINTING FURTHER INFORMATION
            logging.info(
                f"Number of games processed = {self.number_of_games_processed}"
            )
            logging.info(f"Number of games written = {self.number_of_games_written}")
            if self.number_of_games_processed > 0:
                logging.info(
                    f"Percentage of games written = {self.number_of_games_written / self.number_of_games_processed * 100:.2f}%"
                )

    def progression_logging(self, game):
        """
        Logs the progression of the conversion.

        Parameters:
            game: The game currently being processed.
        """
        if self.log:
            logging.debug(f"\tprocessing game #{self.number_of_games_processed}")
            logging.debug(f"\tgame before conversion: {game.mainline_moves()}")

    def start_logging(self):
        """
        Logs the start of the conversion.

        Returns:
            The time when the conversion started.
        """
        start_time = time.time()

        if self.log:
            logging.info("convert_pgn:")
        return start_time

    def game_logging(self, board, processed_game):
        """
        Logs information about the game after it has been processed.

        Parameters:
            board: The board of the game.
            processed_game: The game in xLAN format.
        """

        if self.log:
            logging.debug(f"\tprocessed_game: {processed_game}")
            logging.debug(f"\tboard.fullmove_number: {board.fullmove_number}")
            logging.debug(f"\tboard.outcome(): {board.outcome()}")
