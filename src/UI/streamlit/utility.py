import streamlit as st
import datetime as dt


def apply_css():
    """
    Apply custom CSS styling to the app.
    """
    # You'll need to ensure that the CSS file path correctly points to where your style.css is located.
    st.markdown(
        '<link rel="stylesheet" href="streamlit\style.css">', unsafe_allow_html=True
    )


def set_page(title="Leon LLM", page_icon="♟️"):
    """
    Sets the page configuration with a custom title, icon, and other settings.
    """
    st.set_page_config(
        page_title=title,
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "About": "This is the LeonLLM project, created by Jerome Maag and Lars Schmid. Find more on https://github.com/JeromeMaag/LeonLLM",
        },
    )

    apply_css()

    # This sets the header or title of your app's main page
    st.title(title)


def init_states():
    """
    Initialize session state variables.
    """
    if "next" not in st.session_state:
        st.session_state.next = 0

    if "curfen" not in st.session_state or "moves" not in st.session_state:
        st.session_state.curside = "white"
        st.session_state.curfen = (
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        )
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
