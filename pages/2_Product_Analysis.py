import streamlit as st
import plotly.express as px
from utils.ui import get_data, money
from utils.analysis import group_revenue

st.title("📦 Product Analysis")
st.caption("Understand which products contribute most to sales.")
df, _, _ = get_data()
products = group_revenue(df, "Product")
left, right = st.columns([1.5,1])
with left:
    fig = px.bar(products.sort_values("Revenue"), x="Revenue", y="Product", orientation="h",
                 color="Revenue", color_continuous_scale=["#C8D9FF","#3978F6"],
                 title="Revenue by product")
    fig.update_layout(template="plotly_white", coloraxis_showscale=False, xaxis_title="Revenue (₹)", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)
with right:
    fig = px.pie(products, names="Product", values="Revenue", hole=.62, title="Product revenue mix")
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)
st.subheader("Product performance table")
st.dataframe(products, use_container_width=True, hide_index=True)
