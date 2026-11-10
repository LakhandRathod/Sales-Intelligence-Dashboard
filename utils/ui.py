from datetime import date
import streamlit as st
from utils.data_loader import load_sales

def apply_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] {font-family:'DM Sans', sans-serif;}
    .stApp {background:#F5F7FB;}
    [data-testid="stSidebar"] {background:#101B33;}
    [data-testid="stSidebar"] * {color:#EAF0FC !important;}
    [data-testid="stSidebar"] [data-baseweb="select"] * {color:#18233A !important;}
    [data-testid="stSidebar"] input {color:#18233A !important;}
    [data-testid="stSidebar"] .stDateInput input {color:#18233A !important;}
    h1 {color:#14213D !important; font-weight:800 !important; letter-spacing:-1.3px;}
    h2,h3 {color:#172744 !important; font-weight:700 !important;}
    .eyebrow {font-size:10px; letter-spacing:2px; font-weight:800; color:#3978F6; margin-bottom:7px;}
    .subhead {color:#7B879B; font-size:14px; margin-top:-12px; margin-bottom:20px;}
    .status-pill {display:inline-block; float:right; margin-top:15px; background:#E5F8F1; color:#15966D;
        border:1px solid #C8F0E1; border-radius:30px; padding:8px 13px; font-size:10px; font-weight:800; letter-spacing:1px;}
    .metric-card {background:white; border:1px solid #E9EDF5; border-radius:15px; padding:18px 20px;
        min-height:125px; box-shadow:0 5px 18px rgba(24,45,80,.035);}
    .metric-top {display:flex; justify-content:space-between; color:#7B879B; font-size:12px; font-weight:600;}
    .metric-icon {background:#EEF4FF; color:#3978F6; border-radius:8px; padding:3px 8px; font-weight:800;}
    .metric-value {font-size:27px; line-height:1.5; font-weight:800; color:#172744; letter-spacing:-.8px;}
    .metric-note {font-size:11px; color:#9AA5B5;}
    .section-gap {height:18px;}
    .section-title {font-size:16px; font-weight:800; color:#172744; margin:12px 0 8px; padding-bottom:8px;
        border-bottom:1px solid #E8EDF5;}
    .section-title span {float:right; color:#9AA5B5; font-size:9px; letter-spacing:1.4px; padding-top:5px;}
    .insight-card {background:white; border:1px solid #E9EDF5; border-radius:13px; padding:16px 18px; margin-bottom:18px;}
    .insight-label {font-size:11px; color:#8793A7; font-weight:600;}
    .insight-value {font-size:21px; color:#172744; font-weight:800; margin:5px 0;}
    .insight-desc {font-size:11px; color:#9AA5B5;}
    .footer-note {color:#98A3B4; font-size:11px; padding:18px 0 8px;}
    div[data-testid="stMetric"] {background:white; border:1px solid #E9EDF5; border-radius:13px; padding:12px;}
    div[data-testid="stDataFrame"] {border:1px solid #E9EDF5; border-radius:12px; overflow:hidden;}
    .block-container {padding-top:2rem; padding-bottom:2rem; max-width:1500px;}
    button[kind="primary"] {background:#3978F6;}


/* ===== CSV UPLOAD DESIGN FIX ===== */

[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: #172642 !important;
    padding: 12px !important;
    border-radius: 12px !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploader"] section {
    background: #1B2B49 !important;
    border: 1px dashed #7188B5 !important;
    border-radius: 10px !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploader"] button {
    background: #3978F6 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 7px !important;
    font-weight: 600 !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploader"] small {
    color: #B9C7DD !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploader"] section div {
    color: #EAF0FC !important;
}

    </style>
    """, unsafe_allow_html=True)

def get_data():
    st.sidebar.markdown("## 📊 Sales Analytics")
    st.sidebar.caption("SALES INTELLIGENCE PLATFORM")
    uploaded = st.sidebar.file_uploader("Upload sales CSV", type=["csv"], help="Required: Order_ID, Order_Date, Product, Region, Quantity, Unit_Price")
    try:
        df, quality = load_sales(uploaded)
    except Exception as exc:
        st.error(f"Could not load data: {exc}")
        st.stop()
    if df.empty:
        st.warning("No valid records found. Check your CSV data.")
        st.stop()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Filters")
    regions = sorted(df["Region"].dropna().unique().tolist())
    products = sorted(df["Product"].dropna().unique().tolist())
    chosen_regions = st.sidebar.multiselect("Region", regions, default=regions)
    chosen_products = st.sidebar.multiselect("Product", products, default=products)

    min_date = df["Order_Date"].min().date()
    max_date = df["Order_Date"].max().date()
    date_range = st.sidebar.date_input(
        "Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date,
    )
    filtered = df[df["Region"].isin(chosen_regions) & df["Product"].isin(chosen_products)].copy()
    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
        filtered = filtered[filtered["Order_Date"].dt.date.between(date_range[0], date_range[1])]
    st.sidebar.markdown("---")
    st.sidebar.caption(f"Loaded {len(df):,} valid rows")
    if filtered.empty:
        st.warning("No records match the selected filters. Change the filters in the sidebar.")
        st.stop()
    return filtered, df, quality

def money(value):
    return f"₹{value:,.0f}"

def download_csv(df, label="Download filtered CSV"):
    st.download_button(label, df.to_csv(index=False).encode("utf-8"), "sales_filtered.csv", "text/csv")
