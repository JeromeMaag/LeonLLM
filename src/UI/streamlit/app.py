import streamlit as st
import streamlit.components.v1 as components
import chess
import streamlit_scrollable_textbox as stx
from st_bridge import bridge
from mychess import MyChess
from utility import set_page, init_states
from streamlit_js_eval import streamlit_js_eval
import datetime as dt

set_page(title="Leon LLM", page_icon="♟️")
init_states()

st.session_state.board_width = 400

side_options = ["white", "black"]
model_options = ["GPT2 350k", "GPT2 71k", "GPT2 19k", "Mamba 350k", "stockfish"]

# Select model and side
selected_model = st.selectbox("Select Model for Prediction", model_options)
if "side_choice" not in st.session_state:
    st.session_state.side_choice = side_options[0]

selected_side = st.selectbox(
    "Select Side to Play",
    side_options,
    index=side_options.index(st.session_state.side_choice),
)
st.session_state.selected_model = selected_model

# Update the side choice in session state
if st.session_state.side_choice != selected_side:
    st.session_state.side_choice = selected_side
    st.experimental_rerun()

# Get the info from current board after the user made the move
data = bridge("my-bridge")

if data is not None:
    st.session_state.lastfen = st.session_state.curfen
    st.session_state.curfen = data["fen"]
    st.session_state.curside = (
        data["move"]["color"].replace("w", "white").replace("b", "black")
    )
    st.session_state.moves.update(
        {
            st.session_state.curfen: {
                "side": st.session_state.curside,
                "curfen": st.session_state.curfen,
                "last_fen": st.session_state.lastfen,
                "last_move": data["pgn"],
                "data": None,
                "timestamp": str(dt.datetime.now()),
            }
        }
    )

if st.button("start new game"):
    st.session_state.curfen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    st.session_state.moves = {
        st.session_state.curfen: {
            "side": "GAME START",
            "curfen": st.session_state.curfen,
            "last_fen": "",
            "last_move": "",
            "data": None,
            "timestamp": str(dt.datetime.now()),
        }
    }
    st.experimental_rerun()

# Display the chessboard and game state
cols = st.columns([1, 1])
with cols[0]:
    game = MyChess(
        st.session_state.board_width,
        st.session_state.curfen,
        player_side=st.session_state.side_choice,
    )
    components.html(
        game.game_board(), height=st.session_state.board_width + 75, scrolling=False
    )
    board = chess.Board(st.session_state.curfen)
    outcome = board.outcome()
    st.warning(f"is_check: {board.is_check()}")
    st.warning(f"is_checkmate: {board.is_checkmate()}")
    st.warning(f"is_stalemate: {board.is_stalemate()}")
    st.warning(f"is_insufficient_material: {board.is_insufficient_material()}")
    if outcome:
        st.warning(f"Winner: { {True:'White',False:'Black'}.get(outcome.winner) }")

with cols[1]:
    with st.container():
        records = [
            f"##### {value['timestamp'].split('.')[0]} \n {value['side']} - {value.get('last_move','')}"
            for key, value in st.session_state["moves"].items()
        ]
        stx.scrollableTextbox("\n\n".join(records), height=500, border=True)
