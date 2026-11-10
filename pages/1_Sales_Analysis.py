import streamlit as st
import plotly.express as px
from utils.ui import get_data, money
from utils.analysis import kpis, monthly_revenue

st.title("📈 Sales Analysis")
st.caption("Track revenue patterns and order performance.")
df, _, _ = get_data()
m = kpis(df)
a,b,c = st.columns(3)
a.metric("Revenue", money(m["revenue"]))
b.metric("Orders", f'{m["orders"]:,}')
c.metric("Average order value", money(m["aov"]))
monthly = monthly_revenue(df)
fig = px.line(monthly, x="Month", y="Revenue", markers=True, title="Monthly revenue trend")
fig.update_traces(line_color="#3978F6", line_width=3)
fig.update_layout(template="plotly_white", xaxis_title="", yaxis_title="Revenue (₹)")
st.plotly_chart(fig, use_container_width=True)
st.subheader("Monthly performance")
st.dataframe(monthly, use_container_width=True, hide_index=True)
