# Language Models Explore the Linguistics of Chess

## Table of Contents

- [Introduction](#introduction)
- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running Your First Example](#running-your-first-example)
- [Notebooks](#notebooks)
- [Python Files](#python-files)
- [Data Folder](#data-folder)
- [New Chess Notations](#notations)
   - [xLAN](#xlan)
   - [xLAN+](#xlan-1)
  - [Format Illustration](#format-illustration)
- [Tools and Resources Used](#tools-and-resources-used)
## Introduction

This repository contains the research work and codebase for training a Large Language Model (LLM) solely on chess game sequences. The goal is to train an LLM to understand and replicate the rules of chess, make legal moves, and predict chess game outcomes without explicit rule-based programming.

Two architectures were employed: a Transformer model based on OpenAI's GPT-2 configuration and a [Mamba](https://github.com/state-spaces/mamba) model with comparable dimensions.

The following papers have been written:

- December 2023, Lars Schmid, Jerome Maag: [Language Models Explore the Linguistics of Chess](LanguageModelsExploreTheLinguisticsOfChess.pdf)
   - GitHub Repository: [Project Thesis Branch](https://github.zhaw.ch/schmila7/leon-llm/tree/project-thesis)
- June 2024, Lars Schmid, Jerome Maag: [Optimizing Language Models for Chess: The Impact of Custom Notation and Elo-Based Fine-Tuning](OptimizingLanguageModelsForChess.pdf)

The datasets used to train the models are encoded in our unique chess notations [xLAN/xLAN+](#notations).

Models and datasets can be found here: [Hugging Face](https://huggingface.co/collections/Leon-LLM/leon-llm-chess-6584387dbef870ffa4a7605f)



## Quick Start

This guide will help you get started with the project. Follow these steps to set up the environment and run your first example.

This guide covers using the models (Transformer and Mamba) and training a Transformer model. To train the Mamba model, follow the installation guide on [Mamba's GitHub repository](https://github.com/state-spaces/mamba).

Note: Training the Mamba model is currently only possible on Linux.

### Prerequisites

- Ensure you have Python installed on your system. We used Python version 3.10.9. You can download it from [Python's official website](https://www.python.org/downloads/release/python-3109/).
- For training and efficient predictions, you should use CUDA. We used CUDA Version 12.1. For PyTorch to work with CUDA, you need to download the correct version for your machine from the [PyTorch website](https://pytorch.org/get-started/locally/).

### Installation

1. Clone the repository to your local machine:
   - Open your terminal.
   - Navigate to the directory where you want to clone the repository.
   - Run `git clone https://github.zhaw.ch/schmila7/leon-llm`.
   - Navigate to the cloned repository by running `cd leon-llm`.
2. Install the required dependencies:
   - In the repository's root directory, run `pip install -r requirements.txt`.
   - Install the correct PyTorch version if you want to use CUDA (see [Prerequisites](#prerequisites)).

### Using frontend to play

1. Install Frontend requirements:
   ```sh
   pip install -r frontend_requirements.txt
   ```

2. Run the backend server (FastAPI):
   ```sh
   fastapi dev src/UI/backend/server.py
   ```
3. Run the Streamlit app:
   ```sh
   streamlit run src/UI/streamlit/app.py
   ```

### Running Your First Example

1. Open a notebook:
   - Open the `useModel.ipynb` notebook.
2. Run the notebook:
   - Follow the instructions in the notebook to interact with the trained chess model.
   - Experiment with playing a chess game against the model or use the model to predict the next move in a given chess position.

## Notebooks

In this section, you'll find Jupyter notebooks designed to facilitate various stages of the LLM development and use. These notebooks serve as an interactive interface to run processes and execute code in a step-by-step fashion. The notebooks are interconnected with the Python files, calling upon them as needed. Instead of running Python scripts directly, it is recommended to perform all actions through these notebooks.

1. [analysis.ipynb](analysis.ipynb): Analysis of trained models and datasets, including visualizations and statistics.
2. [dataPreProcessing.ipynb](dataPreProcessing.ipynb): Conversion tools between different chess notations and dataset preparation.
3. [evaluation.ipynb](evaluation.ipynb): Evaluate models on our metrics and inspect the evaluation results.
4. [finetune.ipynb](finetune.ipynb): Notebook for finetuning a model using LoRA.
5. [huggingface.ipynb](huggingface.ipynb): Use to upload and download models and datasets from HuggingFace.
6. [train.ipynb](train.ipynb): Notebook for training and evaluating the chess model.
7. [useModel.ipynb](useModel.ipynb): Interface to play chess against the model, for self-play, and to predict the next move from a given position.
## Files

This section includes scripts and files that provide specific functionalities or information necessary for the LLM's training and operation. These files are typically not run directly. Instead, they are integrated into the Jupyter notebooks, providing the underlying logic and processing power required for tasks such as data preprocessing, model training, and validation.

- [`notation.json`](src/notation.json): Contains all training, prediction, and evaluation configurations for all notations.
- [`xlan_tokens.json and similar`](src/tokenizer/xlan_tokens.json): Each notation has a corresponding .json file that includes the mappings of the chess notation into tokens.
- [`pgn_to_xlan.py`](src/data_preprocessing/pgn_to_xlan.py): Converts PGN format files into the custom [xLAN or xLAN+](#notations) format.
- [`tokenizer.py`](src/tokenizer/tokenizer.py): Tokenizer that uses a JSON mapping file for dataset tokenization.
- [`detokenizer.py`](src/tokenizer/detokenizer.py): Reverses the tokenization process for datasets.
- [`train.py`](src/train.py): Script to train models using GPT-2 configurations on chess datasets.
- [`validate_model.py`](src/validation/validate_model.py): Validates models using various metrics like average correct plies, hard position accuracy, and legal piece move accuracy.
- [`validate_position.py`](src/validation/validate_position.py): Validates models using specific positions defined in a JSON file.
- [`validate_sequence.py`](src/validation/validate_sequence.py): Validates generated move sequences for their legality.
- [`check_duplicates_and_common_lines.py`](src/check_duplicates_and_common_lines.py): Checks for and removes common lines and duplicates between datasets.
- [`chess_game.py`](src/chess_game.py): Framework for playing chess games.
- [`generate_prediction.py`](src/generate_prediction.py): Generates predictions using trained models.
- [`notation_converter.py`](src/notation_converter.py): Converts between different chess notations (e.g., [xLAN](##xLAN) to UCI, UCI to [xLAN](##xLAN)).

## Data Folder

The `data` folder contains training and validation files required for the project.

## Notations

### xLAN

xLAN, an adaptation of LAN (Long Algebraic Notation), was developed to provide a uniform and fixed-length format, facilitating the prompting process for our Language Model. Unlike standard LAN, xLAN explicitly specifies the piece type for each move. This results in a consistent three-token structure per move: `{piece}{start_square}{end_square}`.

### xLAN+

xLAN+ is an extension to xLAN. In addition to the tokens used in xLAN, namely `{piece}`, `{start_square}`, and `{end_square}`, xLAN+ includes an additional `{move_status}` token (referred to as the indicator in code) at the end of each move. This additional token contains information about captures (`x`), checks (`+`), and checkmates (`#`).

### Format Illustration

- **PGN Example:** `1. g3 e6 2. Bg2 Qf6 3. f4 Bc5 4. e4 Qd4 5. e5 Qf2# 0-1`
- **LAN Conversion:** `1. g2-g3 e7-e6 2. Bf1-g2 Qd8-f6 3. f2-f4 Bf8-c5 4. e2-e4 Qf6-d4 5. e4-e5 Qd4-f2# 0-1`
- **xLAN Adaptation:** `1. Pg2g3 Pe7e6 2. Bf1g2 Qd8f6 3. Pf2f4 Bf8c5 4. Pe2e4 Qf6d4 5. Pe4e5 Qd4f2 0-1`
- **xLAN+ Adaptation:** `1. Pg2g3- Pe7e6- 2. Bf1g2- Qd8f6- 3. Pf2f4- Bf8c5- 4. Pe2e4- Qf6d4- 5. Pe4e5- Qd4f2# 0-1`

Special Moves in xLAN/xLAN+:

- **Castling:** Indicated explicitly by the king's movement, e.g., `{king}{start_square}{end_square}`.
- **Pawn Promotion:** Represented as `{goal_piece}{start_square}{end_square}`.
- **Combination in move_status:** `$` represents captures combined with a check, and `!` is used for captures combined with checkmate.


## Tools and Resources Used

1. <a href="https://wandb.ai/site" target="blank">Weights & Biases</a>: A machine learning experiment tracking tool used for visualizing and comparing our models' training progress.
2. <a href="https://python-chess.readthedocs.io/en/latest/" target="blank">Python Chess</a>: A chess library for Python, providing essential functionalities for chess manipulations and move generation.
3. <a href="https://database.lichess.org/" target="blank">Lichess Database</a>: Source of comprehensive chess game data, utilized for training and testing our LLM.
4. <a href="https://huggingface.co/" target="blank">Hugging Face</a>: A platform for sharing and collaborating on machine learning models, used for hosting our trained models and datasets.

---

Feel free to contribute or use this research for academic purposes. For any questions or collaboration, please open an issue or pull request or send us an email: maag.jerome@gmail.com / lars.schmid@gmx.ch

Frontend-Design from https://github.com/dakotalock/QuantumBlue
