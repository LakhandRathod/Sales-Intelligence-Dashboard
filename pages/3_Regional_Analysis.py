import streamlit as st
import plotly.express as px
from utils.ui import get_data
from utils.analysis import group_revenue

st.title("🌍 Regional Analysis")
st.caption("Compare revenue contribution across sales regions.")
df, _, _ = get_data()
regions = group_revenue(df, "Region")
a,b = st.columns(2)
with a:
    fig = px.bar(regions, x="Region", y="Revenue", color="Region", title="Revenue by region")
    fig.update_layout(template="plotly_white", showlegend=False, xaxis_title="", yaxis_title="Revenue (₹)")
    st.plotly_chart(fig, use_container_width=True)
with b:
    fig = px.pie(regions, names="Region", values="Revenue", hole=.58, title="Regional share")
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)
st.subheader("Regional performance")
st.dataframe(regions, use_container_width=True, hide_index=True)
