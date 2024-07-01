import os
import platform
import chess
import chess.engine
import chess.pgn
import io
from transformers import AutoModelForCausalLM
from src.generate_prediction import generate_prediction
import src.notation_converter as converter


models = {
    "Mamba 350k": "Leon-LLM/R4_Mamba_350k_4E_xLANplus",
    "GPT2 350k": "Leon-LLM/R2_GPT2_350k_4E_xLANplus",
    "GPT2 71k": "Leon-LLM/R5_GPT2_71k_4E_xLANplus",
    "GPT2 19k": "Leon-LLM/R1_GPT2_19k_4E_xLANplus",
}

for name, model_path in models.items():
    models[name] = AutoModelForCausalLM.from_pretrained(model_path)


def get_engine_path():
    system = platform.system()
    ROOT_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..")
    )
    if system == "Windows":
        return os.path.join(ROOT_DIR, "src/stockfish/stockfish-windows-x86-64-avx2.exe")
    else:
        return os.path.join(ROOT_DIR, "src/stockfish/stockfish-macOS")


engine = chess.engine.SimpleEngine.popen_uci(get_engine_path())


def get_stockfish_move(fen):
    board = chess.Board(fen)
    result = engine.play(board, chess.engine.Limit(time=0.1))
    return result.move.uci()


def get_LLL_move(fen, history, model_name):
    model = models.get(model_name)
    if not model:
        raise ValueError("Model not found")

    board = chess.Board(fen)
    input_string = process_game_history(history, fen)
    prediction = generate_move(input_string, model)
    last_move_uci = process_prediction(prediction, board)
    return last_move_uci


def process_game_history(history, fen):
    if len(history) > 1:
        game = chess.pgn.read_game(io.StringIO(history))
        board = game.board()
        uci_moves = [board.uci(move) for move in game.mainline_moves()]
        x_lan_sequence = converter.uci_sequence_to_xlan(" ".join(uci_moves))
        return converter.xlan_sequence_to_xlanplus(x_lan_sequence)
    else:
        return fen


def generate_move(input_string, model):
    return generate_prediction(
        input_string,
        num_tokens_to_generate=3,
        model=model,
        notation="xLANplus",
        temperature=0.01,
    )[0]


def process_prediction(prediction, board):
    last_move = prediction.split(" ")[-1]
    return "".join(converter.xlanplus_move_to_uci(board, last_move)[0])
