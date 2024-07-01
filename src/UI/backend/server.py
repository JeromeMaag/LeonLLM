from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, ROOT_DIR)
from src.UI.backend.chess_engine import get_stockfish_move, get_LLL_move

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Sequences(BaseModel):
    fen: str
    history: str
    model: str


@app.post("/get_move")
async def get_move(sequences: Sequences):
    print(f"Received request {sequences}")
    if sequences.model == "stockfish":
        move = get_stockfish_move(sequences.fen)
        print(f"Stockfish move: {move}")
    else:
        move = get_LLL_move(sequences.fen, sequences.history, sequences.model)
        print(f"LLL move: {move}")

    if not move:
        raise HTTPException(status_code=404, detail="Move could not be generated")
    return {"move": move}
