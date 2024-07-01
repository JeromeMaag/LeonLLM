from src.validation.validate_position import evaluate_hard_positions
from src.validation.validate_position import evaluate_legal_piece_moves
from src.validation.validate_sequence import validate_sequence
import wandb
import torch
from transformers import TrainerCallback, AutoModelForCausalLM


def validate_model(
    model: torch.nn.Module,
    number_of_sequences: int = 500,
    number_of_plies_to_generate: int = 170,
    max_batch_size: int = 30,
    seed: int = None,
    do_sequence_validation: bool = True,
    tokens_per_ply: int = 4,
    notation: str = "xLANplus",
    left_padding: bool = False,
) -> tuple[
    float,
    float,
    float,
    dict[str, int],
    list[tuple[int, str, bool]],
    list[tuple[float, list[tuple[int, str, str, bool, str]]]],
    list[tuple[str, int, str, str]],
]:
    """
    Validate a model with the following metrics:
    - Hard position accuracy
    - Legal piece moves accuracy
    - Average correct plies
    - Error frequencies

    Parameters:
    model (Model): The chess model to be evaluated.
    number_of_sequences (int): Number of sequences to be generated.
    number_of_plies_to_generate (int): Number of plies to be generated for each sequence.
    max_batch_size (int): Maximum batch size to be used for generation.
    seed (int): Seed to be used for sequence generation.
    do_sequence_validation (bool): Whether to do sequence validation.
    tokens_per_ply (int): Number of tokens per ply in this notation to generate.
    notation (str): The notation to be used for the model.
    left_padding (bool): Whether to left pad the input sequences.

    Returns:
    tuple: A tuple containing the following metrics:
        hard_position_accuracy (float): The accuracy of the model on hard positions.
        legal_piece_moves_accuracy (float): The accuracy of the model on legal piece moves.
        average_correct_plies (float): The average number of correct plies.
        error_frequencies (dict): A dictionary containing the frequencies of each error.
        hard_position_results (list): A list of tuples containing position ID, predicted move, and correctness.
        legal_piece_moves_results (list): A list of tuples containing the model's accuracy and a list of tuples with position ID, predicted moves, correct moves, correctness, piece and tag..
        sequence_results (list): A list of tuples containing game as string, number of moves until error, error type, and first illegal move.
    """
    hard_position_accuracy, hard_position_results = evaluate_hard_positions(
        model=model,
        notation=notation,
        tokens_per_ply=tokens_per_ply,
        left_padding=left_padding,
    )
    legal_piece_moves_accuracy, legal_piece_moves_results = evaluate_legal_piece_moves(
        model=model,
        notation=notation,
    )
    if do_sequence_validation:
        average_correct_plies, error_frequencies, sequence_results = validate_sequence(
            model=model,
            number_of_games=number_of_sequences,
            number_of_plies_to_generate=number_of_plies_to_generate,
            max_batch_size=max_batch_size,
            seed=seed,
            input_prefix="",
            tokens_per_ply=tokens_per_ply,
            notation=notation,
            left_padding=left_padding,
        )
    else:
        average_correct_plies = None
        error_frequencies = None
        sequence_results = None

    return (
        hard_position_accuracy,
        legal_piece_moves_accuracy,
        average_correct_plies,
        error_frequencies,
        hard_position_results,
        legal_piece_moves_results,
        sequence_results,
    )


class ChessValidationCallback(TrainerCallback):
    """
    Custom callback for the Hugging Face Trainer to perform validation of the chess model.

    This callback is invoked at each model log step, and it runs validation tests on the model.

    Attributes:
        model (torch.nn.Module): The model being trained.
        model_type (str): The type of the model being trained. "GPT2" or "Mamba".
        skip_validation (bool): If True, skips the validation process.
        wandb (bool): If True, logs the validation results to Weights & Biases.
        notation_config (dict): A dictionary containing file paths for the notation configuration.
        left_padding (bool): If True, left pads the input sequences.
    """

    def __init__(
        self,
        model: torch.nn.Module,
        model_type: str,
        skip_validation: bool,
        wandb: bool = True,
        notation_config: dict = None,
        left_padding: bool = False,
    ) -> None:
        self.model = model
        self.model_type = model_type
        self.skipvalidation = skip_validation
        self.notation_config = notation_config
        self.left_padding = left_padding
        self.tokens_per_ply = self.notation_config["tokens_per_ply"]
        self.notation = self.notation_config["notation"]
        self.wandb = wandb

    def on_log(self, args, state, control, **kwargs) -> None:
        """
        Called when the model is saved. If validation is not skipped, it triggers the validation and logging process.
        """
        if not self.skipvalidation:
            # if mamba is used, the model is saved in the cache folder
            if self.model_type == "Mamba":
                self.model.save_pretrained("Leon-LLM-Models/.cache")
                self.cached_model = AutoModelForCausalLM.from_pretrained(
                    "Leon-LLM-Models/.cache"
                )
            self.validate_and_log()

    def validate_and_log(self) -> None:
        """
        Performs validation of the model using the validate_model function and logs the results to wandb.
        """
        results = validate_model(
            self.cached_model if self.model_type == "Mamba" else self.model,
            max_batch_size=100,
            number_of_plies_to_generate=80,
            number_of_sequences=100,
            do_sequence_validation=True,
            tokens_per_ply=self.tokens_per_ply,
            notation=self.notation,
            left_padding=self.left_padding,
        )
        self.log_metrics(*results)

    def log_metrics(
        self,
        hard_position_accuracy: float,
        legal_piece_moves_accuracy: float,
        average_correct_plies: int,
        error_frequencies: dict[str, int],
        hard_position_results: list[tuple[int, str, bool]],
        legal_piece_moves_results: list[
            tuple[float, list[tuple[int, str, str, bool, str]]]
        ],
        sequence_results: list[tuple[str, int, str, str]],
    ) -> None:
        """
        Logs the validation metrics to Weights & Biases.

        Parameters:
            hard_position_accuracy (float): The accuracy of the model on hard positions.
            legal_piece_moves_accuracy (float): The accuracy of the model on legal piece moves.
            average_correct_plies (float): The average number of correct plies.
            error_frequencies (dict): A dictionary containing the frequencies of each error.
            hard_position_results (list): A list of tuples containing position ID, predicted move, and correctness.
            legal_piece_moves_results (list): A list of tuples containing the model's accuracy and a list of tuples with position ID, predicted moves, correct moves, correctness, piece and tag.
            sequence_results (list): A list of tuples containing game as string, number of moves until error, error type, and first illegal move.
        """
        if self.wandb:
            wandb.log(
                {
                    "hard position accuracy": hard_position_accuracy,
                    "legal piece moves accuracy": legal_piece_moves_accuracy,
                    "average correct plies": average_correct_plies,
                }
            )

            error_frequencies_chart = self.create_error_frequencies_chart(
                error_frequencies
            )
            hard_position_table = self.create_hard_position_table(hard_position_results)
            legal_moves_table = self.create_legal_moves_table(legal_piece_moves_results)
            sequence_table = self.create_sequence_table(sequence_results)
            wandb.log(
                {
                    "hard position results table": hard_position_table,
                    "legal piece moves results table": legal_moves_table,
                    "sequence results table": sequence_table,
                    "error frequency bar chart": error_frequencies_chart,
                }
            )

    def create_error_frequencies_chart(
        self, error_frequencies: dict[str, int]
    ) -> wandb.plot.bar:
        """
        Creates a bar chart of error frequencies.

        Parameters:
            error_frequencies (list of tuples): List containing tuples of error types and their frequencies.

        Returns:
            wandb.plot.bar: A bar chart of error frequencies.
        """

        table = wandb.Table(columns=["Error Type", "Frequency"])
        for error_type, frequency in error_frequencies:
            table.add_data(error_type, frequency)

        bar_chart = wandb.plot.bar(
            table, "Error Type", "Frequency", title="Error Frequencies"
        )

        return bar_chart

    def create_hard_position_table(
        self, hard_position_results: list[tuple]
    ) -> wandb.Table:
        """
        Creates a table of hard position results.

        Parameters:
            hard_position_results (list of tuples): List containing tuples of position ID, predicted move, and correctness.

        Returns:
            wandb.Table: A table of hard position results.
        """

        hard_position_table = wandb.Table(
            data=hard_position_results,
            columns=["Position ID", "Predicted Move", "Correctness"],
        )

        return hard_position_table

    def create_legal_moves_table(
        self, legal_piece_moves_results: list[tuple]
    ) -> wandb.Table:
        """
        Creates a table of legal piece moves results.

        Parameters:
            legal_piece_moves_results (list of tuples): List containing tuples of position ID, predicted moves, correct moves correctness, piece and tag.

        Returns:
            wandb.Table: A table of legal piece moves results.
        """

        legal_moves_table = wandb.Table(
            data=legal_piece_moves_results,
            columns=[
                "Position ID",
                "Predicted Move",
                "Correct Moves",
                "Correctness",
                "Piece",
                "Tag",
            ],
        )

        return legal_moves_table

    def create_sequence_table(self, sequence_results: list[tuple]) -> wandb.Table:
        """
        Creates a table of sequence results.

        Parameters:
            sequence_results (list of tuples): List containing tuples of game as string, number of moves until error, error type, and first illegal move.

        Returns:
            wandb.Table: A table of sequence results.
        """

        sequence_table = wandb.Table(
            data=sequence_results,
            columns=[
                "Game String",
                "Moves Until Error",
                "Error Type",
                "First Illegal Move",
                "Predicted Tokens",
            ],
        )

        return sequence_table
