"""
Chess Game with AI Integration
------------------------------

This class encapsulates a chess game, providing functionalities to play the game between two entities, 
which could be human players, AI models, or a combination of both. The class uses the `pythonChess` library 
to handle game logic and the IPython `display` function to visualize the chess board in Jupyter notebooks.

The game supports input from players in xLAN format and can also utilize an AI model to generate 
moves. This AI integration requires a separate model that can be trained using the train.ipynb notebook or
downloaded from https://huggingface.co/Leon-LLM.

xLAN is a unique move notation:
- The first letter represents the piece moved, e.g., P for pawn, N for knight, etc.
- The next two letters represent the start square, e.g., e2, e4, etc.
- The next two letters represent the end square, e.g., e2, e4, etc.
    -Pawn promotion is represented by the piece to promote to, e.g., Q for queen and the start and end square, e.g., Qe7e8.
    -Castling is represented by the start and end square of the king, e.g., Ke1g1.

Attributes:
- player1_type (str): The type of player 1, which can be "player" for a human or "model" for an AI.
- player2_type (str): The type of player 2, similar to player 1.
- model_p1 (torch.nn.Module): The AI model instance for player 1 if player1_type is "model". If player1 is "player" use None.
- model_p2 (torch.nn.Module): The AI model instance for player 2 if player2_type is "model". If player1 is "player" use None.
- notation (str): The notation used for the game, e.g., "xLAN" or "xLANplus". Default is "xLANplus".
- max_model_tries (int): The maximum number of attempts the AI model should make to produce a valid move.
- temperature (float): A parameter for the AI model that may affect move diversity and unpredictability.
- starting_sequence (str): A string of moves to start the game in xLAN with, e.g., "Pe2e4 Pe7e5 Ng1f3".

Example usage:
To initiate a game with two human players:

    >> from chess_game import ChessGame
    >> game = ChessGame(player1_type='player', player2_type='player', model_p1=None, model_p2=None, notation='xLANplus')
    >> game.play_game()

For a game between a human and an AI:

    >> game =    ChessGame(player1_type='player',
                 player2_type='model',
                 model_p1=None, 
                 model_p2=ai_model, 
                 notation='xLANplus',
                 max_model_tries=10,
                 temperature=0.3)
    >> game.play_game()
"""

import chess
import chess.engine
import src.notation_converter as converter
import os
import chess.svg

from IPython.display import display, clear_output
from ipywidgets import Output
from src.generate_prediction import generate_prediction
from IPython.display import SVG
from dotenv import load_dotenv


class ChessGame:
    def __init__(
        self,
        player1_type,
        player2_type,
        model_p1,
        model_p2,
        notation="xLANplus",
        max_model_tries=5,
        temperature=0.5,
        starting_sequence="",
        show_game_history=True,
        engine_path=None,
        survival_rate=False,
        show_output=True,
        manual_input=True,
        mate_score=100_000,
    ):
        load_dotenv()
        self.player1_type = player1_type
        self.player2_type = player2_type
        self.model_p1 = model_p1
        self.model_p2 = model_p2
        self.notation = notation
        self.max_model_tries = max_model_tries
        self.temperature = temperature
        self.movehistory = starting_sequence
        self.show_game_history = show_game_history
        self.engine_path = engine_path
        self.show_output = show_output
        self.manual_input = manual_input
        self.mate_score = mate_score
        self.survival_rate = survival_rate

        self.TOKENS_TO_PREDICT = 3  # Number of tokens to predict: 3 Tokens = 1 Move
        self.board = chess.Board()
        self.output_display = Output()  # Output widget to display the board
        self.number_of_plies = 1
        self.outcome = None
        self.player_scores = []
        if self.engine_path is not None:
            self.engine = chess.engine.SimpleEngine.popen_uci(self.engine_path)
        else:
            self.engine = None

    def display_board(self, size=600, save_to_file=False):
        """
        Displays the current state of the board.
        """
        with self.output_display:
            clear_output(wait=True)
            display(self.board)

            if save_to_file:
                filename = f"{save_to_file}.svg"

                # Ensure the directory exists
                os.makedirs("./results/plots/saved_boards/", exist_ok=True)
                filepath = os.path.join("./results/plots/saved_boards", filename)

                board_svg = chess.svg.board(board=self.board, size=size)

                # Save the SVG data to the file
                with open(filepath, "w") as file:
                    file.write(board_svg)

                print(f"Board saved to {filepath}")

    def get_next_move(self, player_type, model):
        """
        Gets the next move from the player.
        If the player type is 'player', it prompts the user for input.
        If the player type is 'model', it attempts to get a move from the AI model.

        Args:
        player_type (str): The type of the player, either 'player' or 'model'.
        model: The AI model to predict the move if player_type is 'model'.

        Returns:
        str: Next move in xLAN format, e.g., 'Pe2e4'.
        """
        if player_type == "player":
            user_move = self.get_next_move_from_player()
            if self.show_game_history:
                print("Your input: ", user_move)
            return user_move
        elif player_type == "model":
            return self.get_next_move_from_model(model)
        elif player_type == "engine":
            return self.get_next_move_from_engine()
        else:
            raise ValueError(
                "Invalid player type. Must be 'player', 'model', or 'engine'."
            )

    def get_next_move_from_player(self):
        """
        Prompts the user for input and returns the move in xLAN format.

        Returns:
        str: Next move in xLAN format, e.g., 'Pe2e4'.
        """
        user_move = input("Your move (e.g., Pe2e4) 'exit' to terminate program: ")
        if user_move == "exit":
            print("Exiting game...")
            raise ExitGameException("Player requested to exit the game.")
        return user_move

    def get_next_move_from_model(self, model):
        """
        Attempts to get a move from the AI model. If the model fails to produce a valid move, it prompts the user
        for input.

        Args:
        model (torch.nn.Module): The AI model to predict the move.

        Returns:
        str: Next move in xLAN format, e.g., 'Pe2e4'.
        """
        for _ in range(self.max_model_tries):
            model_move = self.model_prediction(model)
            UCI_move = converter.xlan_move_to_uci(self.board, model_move)
            try:
                if chess.Move.from_uci(UCI_move) in self.board.legal_moves:
                    if self.show_game_history:
                        print("Model move: ", model_move)
                    return model_move
            except ValueError:
                print("Model move is not legal, please try again. Move: ", model_move)

        if self.manual_input:
            # If the model fails to produce a valid move, ask for manual input
            print("Model failed to produce a valid move. Please enter a move manually.")
            user_move = self.get_next_move_from_player()
            print("Your played for model move: ", user_move)
            return user_move
        else:
            #  If the model fails to produce a valid move, end game
            self.outcome = "invalid_move"
            raise ExitGameException(
                "Model failed to produce a valid move. Ending game."
            )

    def get_next_move_from_engine(self):
        """
        Gets the next move from the engine.

        Returns:
        str: Next move in xLAN format, e.g., 'Pe2e4'.
        """

        result = self.engine.play(self.board, chess.engine.Limit(time=0.1))
        move = self.board.uci(result.move)
        return converter.uci_move_to_xlan(self.board, move)

    def make_move(self, move_xlan):
        """
        Attempts to make a move on the board. Validates if the move is legal, converts it to UCI format,
        and applies it to the board.

        Args:
        move (str): The move in xLAN format, e.g., 'Pe2e4'.

        Returns:
        bool: True if the move was successfully made, False otherwise.
        """
        UCI_move = converter.xlan_move_to_uci(self.board, move_xlan)
        if len(UCI_move) != 4 and len(UCI_move) != 5:
            print("Invalid move length, please try again. Your input: ", move_xlan)
            return False
        try:
            move_uci = chess.Move.from_uci(UCI_move)
            if move_uci in self.board.legal_moves:
                capture = self.board.is_capture(move_uci)
                self.board.push(chess.Move.from_uci(UCI_move))
                mate = self.board.is_checkmate()
                check = self.board.is_check()
                suffix = ""

                # Add move to move history in unique move notation - model uses this to predict next move
                if self.notation != "xLAN":
                    if check:
                        suffix = "+" if not capture else "$"
                    elif mate:
                        suffix = "#" if not capture else "!"
                    elif capture:
                        suffix = "x"
                    else:
                        suffix = "-"
                self.movehistory += move_xlan + suffix + " "

                # add score of current position
                if self.survival_rate:
                    info = self.engine.analyse(self.board, chess.engine.Limit(time=0.1))
                    evaluation = (
                        info["score"].white().score(mate_score=self.mate_score)
                    )  # https://python-chess.readthedocs.io/en/latest/engine.html#chess.engine.Score
                    self.player_scores.append(evaluation)

                return True
            else:
                print("Invalid move, please try again. Move: ", move_xlan)
        except ValueError:
            print("Move is not legal, please try again. Move: ", move_xlan)
        return False

    def model_prediction(self, model):
        """
        Uses the AI model to predict a move based on the current move history.

        Args:
        model (torch.nn.Module): The AI model to predict the move.

        Returns:
        str: The predicted move by the model in xLAN format, e.g., 'Pe2e4'.
        """
        output, _, _ = generate_prediction(
            input=self.movehistory,
            num_tokens_to_generate=self.TOKENS_TO_PREDICT,
            model=model,
            notation=self.notation,
            temperature=self.temperature,
        )
        if self.show_game_history:
            print("Model input: ", self.movehistory)
            print("Model Output: ", output)

        return output.split(" ")[-1]

    def check_result(self):
        """
        Checks the current state of the game and prints out the result if the game has ended.
        It handles various conditions such as checkmate, stalemate, insufficient material, and the 75-move rule.
        """
        if self.board.is_checkmate():
            self.outcome = "checkmate"
        elif self.board.is_stalemate():
            self.outcome = "stalemate"
        elif self.board.is_insufficient_material():
            self.outcome = "insufficient_material"
        elif self.board.is_seventyfive_moves():
            self.outcome = "75_move_rule"
        elif self.board.is_fivefold_repetition():
            self.outcome = "fivefold_repetition"
        elif self.outcome != "invalid_move":
            self.outcome = "unknown"
        if self.show_output:
            print(f"Game result: {self.outcome} ({self.board.result()})")

    def push_starting_sequence(self):
        """
        Pushes the starting sequence of moves to the board. The starting sequence is provided as a string
        of moves separated by spaces, e.g., "Pe2e4 Pe7e5 Ng1f3". It is converted to UCI format and pushed to the board.
        """
        if self.movehistory == "":
            if self.show_output:
                print(f"Start sequence is empty. Starting from the initial position.")
            return

        starting_sequence = self.movehistory.strip().split(" ")

        for move in starting_sequence:
            try:
                # Convert the move to UCI format and push it to the board
                UCI_move = converter.xlan_move_to_uci(self.board, move)
                if chess.Move.from_uci(UCI_move) in self.board.legal_moves:
                    self.board.push(chess.Move.from_uci(UCI_move))
                else:
                    print(f"Invalid move encountered: {move}. Ending sequence.")
                    break
            except ValueError:
                print(
                    f"Move is not legal or incorrectly formatted: {move}. Ending sequence."
                )
                break

    def play_game(self):
        """
        The main method to start and play through the game. It handles turn-taking, move making, and game state updates.
        The game continues until a terminal state (checkmate, stalemate, etc.) is reached. It also handles the case
        where the maximum token length is reached and the player can choose to continue or remove the first moves.
        Model maximum input token length is 512 tokens
        """
        if self.show_output:
            self.start_informations()
            self.print_game_config()
        display(self.output_display)
        self.push_starting_sequence()
        while not self.board.is_game_over():
            if self.show_output:
                self.display_board()
            if self.show_game_history:
                display(self.board)
                print("Move ply (number): ", self.number_of_plies)

            if self.number_of_plies * self.TOKENS_TO_PREDICT >= 508:
                #  Player can choose to finish or remove first moves
                continue_game = input(
                    "Max moves reached. Remove first move now. Continue? (y/n): "
                )
                if continue_game == "y":
                    moves = self.movehistory.strip().split(" ")
                    moves = moves[1:]
                    self.movehistory = " ".join(moves)
                    self.movehistory += " "
                else:
                    print("Game stopped - Max moves reached.")
                    break

            try:
                if self.board.turn == chess.WHITE:
                    move = self.get_next_move(self.player1_type, self.model_p1)
                else:
                    move = self.get_next_move(self.player2_type, self.model_p2)

                while not self.make_move(move):
                    if self.board.turn == chess.WHITE:
                        move = self.get_next_move(self.player1_type, self.model_p1)
                    else:
                        move = self.get_next_move(self.player2_type, self.model_p2)

                self.number_of_plies += 1
            except ExitGameException as e:
                print(e)
                break

        if self.show_output:
            self.display_board()
        self.check_result()

    def start_informations(self):
        """
        Prints out the starting information for the game.
        """

        print("Welcome to the Chess Game!")
        print(
            "Instructions: Enter your moves in xLAN format [Piece][Startsquare][Endsquare]. eg. Pe2e4"
        )
        print(
            "For Pawn promotion, enter the piece you want to promote instead of Pawn. eg. Qe7e8"
        )
        print(
            "The game will continue until a checkmate, stalemate, or other draw condition is reached."
        )
        print("To exit the game, enter 'exit'.")

    def print_game_config(self):
        print("Player 1: ", self.player1_type)
        print("Player 2: ", self.player2_type)
        print("Max model tries: ", self.max_model_tries)
        print("Temperature: ", self.temperature)
        print("Starting sequence: ", self.movehistory)

    def show_position_from_sequence(self, move_sequence, save_to_file):
        """
        Takes a string of moves, plays them on the board, and displays the final position.

        Args:
        moves_string (str): A string containing moves in xLAN separated by spaces, e.g., "Pe2e4 Pe7e5 Ng1f3"
        save_to_file (str): The filename to save the board to as an SVG file.
        """
        self.movehistory = move_sequence
        self.push_starting_sequence()

        display(self.output_display)
        self.display_board(save_to_file=save_to_file)

    def print_game_history(self):
        """
        Prints out the move history of the game.
        """
        print(f"Game history: {self.movehistory}")
        print(f"Number of plies: {self.number_of_plies}")
        print(f"Result: {self.outcome} ({self.board.result()})")

    def get_stats(self):
        """
        Returns the game history and result.
        """
        return (
            self.movehistory,
            self.number_of_plies,
            self.outcome,
            self.board.result(),
            self.player_scores,
        )


class ExitGameException(Exception):
    """Custom exception for exiting the game."""

    pass
