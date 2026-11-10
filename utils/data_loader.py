from pathlib import Path
import pandas as pd
import streamlit as st
from utils.data_cleaning import clean_sales

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "data" / "sales.csv"

@st.cache_data(show_spinner=False)
def _read_and_clean(file_bytes):
    from io import BytesIO
    raw = pd.read_csv(BytesIO(file_bytes))
    return clean_sales(raw)

def load_sales(uploaded=None):
    if uploaded is not None:
        return _read_and_clean(uploaded.getvalue())
    return _read_and_clean(SAMPLE.read_bytes())
