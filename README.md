# NOVA — Sales Intelligence Dashboard

A polished multi-page Sales Analytics dashboard built with Python, Pandas, Streamlit and Plotly.

## Dashboard features
- Executive overview with Revenue, Orders, Units Sold and Average Order Value.
- Sidebar filters for date range, region and product.
- Interactive monthly revenue trend, regional revenue mix, product leaderboard and weekday demand.
- Searchable recent transactions table and filtered CSV export.
- Dedicated Sales, Product, Regional and Data Quality pages.
- CSV upload with validation, cleaning and duplicate/invalid row reporting.
- Excel and CSV exports.

> Note: The provided dataset contains quantity and unit price, but no product cost. Therefore this project reports revenue and order metrics, not profit or margin. Add a `Unit_Cost` column to support profit analysis.

## Required CSV columns
`Order_ID, Order_Date, Product, Region, Quantity, Unit_Price`

## Setup (Windows PowerShell)
Use Python 3.12 or 3.13 for the easiest package compatibility. Open this folder in VS Code.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```

If `py -3.12` is unavailable, install Python 3.12 or 3.13, then recreate the environment with the installed launcher version. If PowerShell blocks activation:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Open the local URL Streamlit prints, usually `http://localhost:8501`.

## Project structure
```text
02_Sales_Data_Analysis_Dashboard/
├── app.py
├── data/
│   ├── sales.csv
│   └── cleaned_sales.csv
├── pages/
│   ├── 1_Sales_Analysis.py
│   ├── 2_Product_Analysis.py
│   ├── 3_Regional_Analysis.py
│   └── 4_Data_Quality.py
├── utils/
│   ├── __init__.py
│   ├── ui.py
│   ├── data_loader.py
│   ├── data_cleaning.py
│   ├── analysis.py
│   └── visualization.py
├── assets/
├── exports/
├── requirements.txt
├── README.md
└── .gitignore
```

## Run rule
Do not run individual files inside `pages/` directly. Always start the complete multi-page app from the project root with:
`python -m streamlit run app.py`
