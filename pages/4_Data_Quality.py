import streamlit as st
import pandas as pd
from io import BytesIO
from utils.ui import get_data

st.title("🧹 Data Quality & Exports")
st.caption("Review data preparation results and export clean business data.")
filtered, cleaned, quality = get_data()
a,b,c,d = st.columns(4)
a.metric("Input rows", f'{quality["input_rows"]:,}')
b.metric("Duplicates removed", f'{quality["duplicates_removed"]:,}')
c.metric("Invalid rows removed", f'{quality["invalid_rows_removed"]:,}')
d.metric("Valid rows", f'{quality["valid_rows"]:,}')
st.subheader("Cleaned data preview")
st.dataframe(cleaned.head(200), use_container_width=True, hide_index=True)
st.download_button("Download all cleaned data (CSV)", cleaned.to_csv(index=False).encode("utf-8"),
                   "cleaned_sales.csv", "text/csv")
output = BytesIO()
with pd.ExcelWriter(output, engine="openpyxl") as writer:
    filtered.to_excel(writer, index=False, sheet_name="Filtered Sales")
    cleaned.to_excel(writer, index=False, sheet_name="All Cleaned Sales")
st.download_button("Download Excel report", output.getvalue(), "sales_report.xlsx",
                   "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
