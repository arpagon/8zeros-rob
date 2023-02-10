"""
Shim layer for using the riffusion playground streamlit app with huggingface spaces.
It doesn't support the pages feature of streamlit yet.
"""
import importlib
from pathlib import Path
import sys

import streamlit as st


def render_main():
    RIFFUSION_PATH = Path(__file__).parent / "riffusion"
    sys.path.append(str(RIFFUSION_PATH))

    st.set_page_config(layout="wide", page_icon="🎸")

    # Disable the rest of the setting
    st.set_page_config = lambda **kwargs: None

    # Find all pages in the riffusion directory
    pages = sorted(
        p.name[:-3] for p in (RIFFUSION_PATH / "riffusion" / "streamlit" / "pages").glob("*.py")
    )

    # Add the pages to the sidebar
    page = st.sidebar.selectbox("Page", pages, index=pages.index("text_to_audio"))
    assert page is not None

    module = importlib.import_module(f"riffusion.streamlit.pages.{page}")
    render_func = getattr(module, f"render_{page}")
    render_func()


render_main()