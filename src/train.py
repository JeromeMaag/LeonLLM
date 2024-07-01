import torch
import wandb
import json
from torch.utils.data import Dataset
from transformers import (
    GPT2LMHeadModel,
    GPT2Config,
    MambaForCausalLM,
    Trainer,
    TrainingArguments,
    AutoConfig,
)
from peft import PeftModel

from src.validation.validate_model import ChessValidationCallback


class ChessTrainer:
    """
    This class handles the training of a LLM on the Chess dataset.
    It also handles the logging of training metrics to Weights & Biases.


    Attributes:
    - model_type (str): The type of model to be trained. Options are "GPT2" and "Mamba".
    - batch_size (int): The number of games to be processed in each batch. The larger the batch size, the more memory is required.
    - learning_rate (float): The learning rate for training the LLM.
    - epochs (int): The number of times the model will see the entire dataset during training.
    - input_file (str): Path to the text file containing tokenized Chess games.
    - output_dir (str): Path to the directory where the trained model will be saved.
    - save_steps (int): The number of steps between each checkpoint save. Defaults to 1000.
    - logging_steps (int): The number of steps between each logging of training metrics. Defaults to 50.
    - skip_validation (bool): Whether to skip the validation step during training. Defaults to False.
    - weight_and_biases (bool): Whether to use Weights & Biases for logging training metrics. Defaults to True.
    - use_FP16 (bool): Whether to use FP16 mixed precision training. Defaults to True.
    - notation (str): The notation used to represent the Chess games. Defaults to "xLANplus". Options are "xLAN" and "xLANplus" and xLANc".
    - peft (PeftModel): A pretrained model to use for training. Defaults to None.
    - left_padding (bool): Whether to pad the left side of the game sequence. Defaults to False.

    Example:

        from path_to_your_script import ChessTrainer

        trainer = ChessTrainer(
            model_type="GPT2",
            batch_size=512,
            learning_rate=0.0001,
            save_steps=25,
            epochs=5,
            input_file="./data/games_train.txt",
            output_dir="./trained_models",
            skip_validation=False,
            weight_and_biases=True,
            use_FP16=True,
            notation="xLAN",
            peft=None,
            left_padding=False,
        )

        trainer.train()
    """

    def __init__(
        self,
        model_type: str,
        batch_size: int,
        learning_rate: float,
        epochs: int,
        input_file: str,
        output_dir: str,
        checkpoint_dir: str = None,
        save_steps: int = 1000,
        logging_steps: int = 50,
        skip_validation: bool = False,
        weight_and_biases: bool = True,
        use_FP16: bool = True,
        notation: str = "xLANplus",
        peft: PeftModel = None,
        left_padding: bool = False,
    ) -> None:
        self.model_type = model_type
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.input_file = input_file
        self.output_dir = output_dir
        self.checkpoint_dir = checkpoint_dir
        self.save_steps = save_steps
        self.logging_steps = logging_steps
        self.skip_validation = skip_validation
        self.weight_and_biases = weight_and_biases
        self.use_FP16 = use_FP16
        self.notation = notation
        self.peft = peft
        self.left_padding = left_padding

        self.notation_config = self.load_notation_config()

        # GPT-2 model configuration using the loaded tokenization config.
        self.VOCAB_SIZE = self.notation_config[
            "vocab_size"
        ]  # Number of tokens in the vocabulary.
        self.N_POSITION = self.notation_config[
            "n_positions"
        ]  # Maximum number of tokens the model can handle in a single input sequence.
        self.PAD_TOKEN_ID = self.notation_config[
            "pad_token_id"
        ]  # Token used for padding.
        self.BOS_TOKEN_ID = self.notation_config[
            "bos_token_id"
        ]  # Token used for beginning of sequence.
        self.EOS_TOKEN_ID = self.notation_config[
            "eos_token_id"
        ]  # Token used for end of sequence.
        self.model_name = output_dir.split("/")[-2]
        self.wand_project_name = "Leon LLM"
        self.logging_dir = "./logs"
        self.report_to = "none"

        if self.weight_and_biases:
            # Initialize the Weights & Biases tool.
            self.setup_wandb()

        # Create a dataset object for training.
        self.dataset = self.create_dataset()

        # Initialize the model.
        if self.model_type == "GPT2":
            self.model = self.create_GPT2_model()
        elif self.model_type == "Mamba":
            self.model = self.create_mamba_model()

    class ChessDataset(Dataset):
        """
        A subclass of torch.utils.data.Dataset that prepares the Chess game data for training.

        Methods:
        - __init__: Initializes the dataset with the games and their corresponding properties.
        - __len__: Returns the number of games in the dataset.
        - __getitem__: Retrieves a game from the dataset by index.
        """

        def __init__(
            self,
            games: list[list[int]],
            max_length: int,
            padding_id: int,
            left_padding: bool = False,
        ) -> None:
            self.games = games
            self.max_length = max_length
            self.padding_id = padding_id
            self.left_padding = left_padding

        def __len__(self) -> int:
            return len(self.games)

        def __getitem__(self, index: int) -> torch.Tensor:
            game = self.games[index]
            if self.left_padding:
                padded_game = [self.padding_id] * (self.max_length - len(game)) + game
            else:
                padded_game = game + [self.padding_id] * (self.max_length - len(game))

            return torch.tensor(padded_game)

    def load_notation_config(self) -> dict[str, int]:
        config_path = "./src/notation.json"
        with open(config_path, "r") as file:
            configs = json.load(file)
        return configs[self.notation]

    def setup_wandb(self) -> None:
        """
        Initializes the Weights & Biases (wandb) tool for monitoring and logging the training process.
        """
        self.report_to = "wandb"
        wandb.init(
            project=self.wand_project_name,
            sync_tensorboard=True,
            name=self.model_name,
            config={
                "Dataset": self.input_file,
                "Epochs": self.epochs,
                "Learning Rate": self.learning_rate,
                "Batch Size": self.batch_size,
                "Name": self.model_name,
                "Validation": not self.skip_validation,
                "Save Steps": self.save_steps,
                "Logging Steps": self.logging_steps,
                "notation": self.notation,
            },
        )

    def load_games(self) -> tuple[list[list[int]], int]:
        """
        Loads the tokenized Chess games from the input file.

        Returns:
        - List[List[int]]: A list of lists containing the tokenized Chess games.
        - int: The lenght of the longest game in the dataset.
        """

        with open(self.input_file, "r") as file:
            lines = file.readlines()

        games = [[int(token) for token in line.split()] for line in lines]
        max_length = max(len(game) for game in games)
        return games, max_length

    def create_dataset(self) -> ChessDataset:
        """
        Creates a Chess dataset instance for training.

        Returns:
        - ChessDataset: An instance of the ChessDataset class.
        """
        # Load and preprocess the game data.
        games, max_length = self.load_games()
        return self.ChessDataset(
            games, max_length, self.PAD_TOKEN_ID, self.left_padding
        )

    def create_GPT2_model(self) -> GPT2LMHeadModel:
        """
        Initializes and returns a GPT-2 model with the specified configuration,
        or loads a model from a checkpoint.

        Returns:
        - GPT2LMHeadModel: An instance of the GPT2LMHeadModel class.
        """
        if self.checkpoint_dir:
            # Load the model from the specified checkpoint.
            model = GPT2LMHeadModel.from_pretrained(self.checkpoint_dir)
        elif self.peft:
            model = self.peft
        else:
            # Initialize a new model with the specified configuration.
            config = GPT2Config(
                vocab_size=self.VOCAB_SIZE,
                n_positions=self.N_POSITION,
                bos_token_id=self.BOS_TOKEN_ID,
                eos_token_id=self.EOS_TOKEN_ID,
            )
            model = GPT2LMHeadModel(config)

        return model

    def create_mamba_model(self) -> MambaForCausalLM:
        """
        Initializes and returns a Mamba model with the specified configuration,
        or loads a model from a checkpoint.

        Returns:
        - MambaForCausalLM: An instance of the MambaForCausalLM class.
        """
        if self.checkpoint_dir:
            # Load the model from the specified checkpoint.
            model = MambaForCausalLM.from_pretrained(self.checkpoint_dir)
        elif self.peft:
            model = self.peft
        else:
            # Load the configuration from "state-spaces/mamba-130m-hf".
            config = AutoConfig.from_pretrained("state-spaces/mamba-130m-hf")
            config.vocab_size = self.VOCAB_SIZE
            config.bos_token_id = self.BOS_TOKEN_ID
            config.eos_token_id = self.EOS_TOKEN_ID

            model = MambaForCausalLM(config)

        return model

    def data_collator(self, data: list[torch.Tensor]) -> dict[str, torch.Tensor]:
        """
        Collates the data into a dictionary of tensors for model consumption.
        For padding Tokens a tensor of -100 is used, which is used by the model to ignore the padded tokens.

        Parameters:
        - data (List of torch.Tensor): A list of tensors containing game data.

        Returns:
        - Dict[str, torch.Tensor]: A dictionary of tensors containing the input data and labels.
        """
        input_data = torch.stack(data)
        labels = input_data.clone().where(
            input_data != self.PAD_TOKEN_ID, torch.tensor(-100)
        )
        return {"input_ids": input_data, "labels": labels}

    def train(self) -> None:
        """
        Trains the model on the Chess dataset.
        """

        training_args = TrainingArguments(
            output_dir=self.output_dir,
            per_device_train_batch_size=self.batch_size,
            num_train_epochs=self.epochs,
            logging_dir=self.logging_dir,
            logging_steps=self.logging_steps,
            save_steps=self.save_steps,
            learning_rate=self.learning_rate,
            fp16=self.use_FP16,
            report_to=self.report_to,
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=self.dataset,
            data_collator=self.data_collator,
            callbacks=[
                ChessValidationCallback(
                    self.model,
                    self.model_type,
                    self.skip_validation,
                    self.weight_and_biases,
                    self.notation_config,
                    self.left_padding,
                )
            ],
        )
        trainer.train()
        self.model.save_pretrained(f"{self.output_dir}/{self.model_name}")

        if self.weight_and_biases:
            wandb.finish()
