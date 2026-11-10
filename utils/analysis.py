import pandas as pd

def kpis(df):
    revenue = float(df["Revenue"].sum())
    orders = int(df["Order_ID"].nunique())
    return {
        "revenue": revenue,
        "orders": orders,
        "units": float(df["Quantity"].sum()),
        "aov": revenue / orders if orders else 0,
    }

def group_revenue(df, column):
    return df.groupby(column, as_index=False)["Revenue"].sum().sort_values("Revenue", ascending=False)

def monthly_revenue(df):
    return df.groupby("Month", as_index=False)["Revenue"].sum().sort_values("Month")

def weekday_revenue(df):
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    out = df.groupby("Weekday", as_index=False).agg(Units=("Quantity", "sum"), Revenue=("Revenue", "sum"))
    out["Weekday"] = pd.Categorical(out["Weekday"], categories=order, ordered=True)
    return out.sort_values("Weekday")
