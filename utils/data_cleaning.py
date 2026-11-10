import pandas as pd

REQUIRED = ["Order_ID", "Order_Date", "Product", "Region", "Quantity", "Unit_Price"]

def clean_sales(raw):
    df = raw.copy()
    df.columns = df.columns.astype(str).str.strip()
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))

    input_rows = len(df)
    df = df.drop_duplicates().copy()
    duplicates = input_rows - len(df)

    for col in ["Order_ID", "Product", "Region"]:
        df[col] = df[col].astype("string").str.strip().replace("", pd.NA)

    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    for col in ["Quantity", "Unit_Price"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    invalid = (
        df[REQUIRED].isna().any(axis=1)
        | (df["Quantity"] <= 0)
        | (df["Unit_Price"] < 0)
    )
    invalid_rows = int(invalid.sum())
    df = df.loc[~invalid].copy()
    df["Revenue"] = df["Quantity"] * df["Unit_Price"]
    df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)
    df["Weekday"] = df["Order_Date"].dt.day_name()
    return df, {
        "input_rows": input_rows,
        "duplicates_removed": duplicates,
        "invalid_rows_removed": invalid_rows,
        "valid_rows": len(df),
    }
