import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.ui import get_data, apply_theme, money
from utils.analysis import kpis, monthly_revenue, group_revenue, weekday_revenue

st.set_page_config(
    page_title="Sales Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()

df, all_data, quality = get_data()

# Header
head_left, head_right = st.columns([3, 1])
with head_left:
    st.markdown('<div class="eyebrow">BUSINESS INTELLIGENCE / SALES PERFORMANCE</div>', unsafe_allow_html=True)
    st.title("Sales Intelligence")
    st.markdown('<div class="subhead">A live view of revenue, demand and regional performance.</div>', unsafe_allow_html=True)
with head_right:
    st.markdown('<div class="status-pill">● DATA CONNECTED</div>', unsafe_allow_html=True)
    st.caption(f"Updated from {len(df):,} filtered records")

m = kpis(df)
k1, k2, k3, k4 = st.columns(4)
for col, label, value, note, icon in [
    (k1, "Total revenue", money(m["revenue"]), "Gross sales value", "₹"),
    (k2, "Orders", f'{m["orders"]:,}', "Distinct order IDs", "▤"),
    (k3, "Units sold", f'{m["units"]:,.0f}', "Total quantity", "↗"),
    (k4, "Average order value", money(m["aov"]), "Revenue per order", "◈"),
]:
    with col:
        st.markdown(
            f'<div class="metric-card"><div class="metric-top"><span>{label}</span><span class="metric-icon">{icon}</span></div>'
            f'<div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',
            unsafe_allow_html=True,
        )

st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)

# Main trend and breakdown
left, right = st.columns([1.65, 1], gap="large")
with left:
    st.markdown('<div class="section-title">Revenue trajectory <span>MONTHLY</span></div>', unsafe_allow_html=True)
    monthly = monthly_revenue(df)
    fig = px.area(monthly, x="Month", y="Revenue", markers=True)
    fig.update_traces(line=dict(color="#3978F6", width=3), fillcolor="rgba(57,120,246,0.12)",
                      marker=dict(size=7, color="#3978F6"))
    fig.update_layout(
        template="plotly_white", height=360, margin=dict(l=8,r=8,t=18,b=8),
        xaxis_title="", yaxis_title="", hovermode="x unified",
        font=dict(family="Arial", color="#65718A"),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_xaxes(showgrid=False, linecolor="#E9EDF5")
    fig.update_yaxes(gridcolor="#EEF1F6", zeroline=False, tickprefix="₹", tickformat=",.0f")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
with right:
    st.markdown('<div class="section-title">Revenue by region <span>SHARE</span></div>', unsafe_allow_html=True)
    reg = group_revenue(df, "Region")
    fig = px.pie(reg, names="Region", values="Revenue", hole=0.68,
                 color_discrete_sequence=["#3978F6","#21B8A6","#F5A84B","#8B72E8","#E46D8B","#8A9AAF"])
    fig.update_traces(textposition="outside", textinfo="percent", hole=0.68,
                      marker=dict(line=dict(color="white", width=3)))
    fig.update_layout(
        template="plotly_white", height=360, margin=dict(l=8,r=8,t=18,b=8),
        showlegend=True, legend=dict(orientation="h", y=-0.12, x=0.0, font=dict(size=10)),
        paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Arial", color="#65718A"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# Product leaderboard and weekday pattern
left, right = st.columns([1.2, 1], gap="large")
with left:
    st.markdown('<div class="section-title">Product leaderboard <span>BY REVENUE</span></div>', unsafe_allow_html=True)
    prod = group_revenue(df, "Product").head(8).sort_values("Revenue")
    fig = px.bar(prod, x="Revenue", y="Product", orientation="h",
                 color="Revenue", color_continuous_scale=["#BBD0FF","#3978F6"])
    fig.update_layout(template="plotly_white", height=330, margin=dict(l=8,r=8,t=10,b=8),
                      coloraxis_showscale=False, xaxis_title="", yaxis_title="",
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(family="Arial", color="#65718A"))
    fig.update_xaxes(gridcolor="#EEF1F6", tickprefix="₹", tickformat=",.0f")
    fig.update_yaxes(showgrid=False)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
with right:
    st.markdown('<div class="section-title">Demand by weekday <span>UNITS SOLD</span></div>', unsafe_allow_html=True)
    weekday = weekday_revenue(df)
    fig = px.bar(weekday, x="Weekday", y="Units", color="Units",
                 color_continuous_scale=["#C8F0E9","#21B8A6"])
    fig.update_layout(template="plotly_white", height=330, margin=dict(l=8,r=8,t=10,b=8),
                      coloraxis_showscale=False, xaxis_title="", yaxis_title="Units",
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(family="Arial", color="#65718A"))
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#EEF1F6")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# Insights
st.markdown('<div class="section-title">Business snapshot <span>QUICK INSIGHTS</span></div>', unsafe_allow_html=True)
best_region = reg.iloc[0]["Region"] if not reg.empty else "—"
best_product = group_revenue(df, "Product").iloc[0]["Product"] if not df.empty else "—"
peak_month = monthly.sort_values("Revenue", ascending=False).iloc[0]["Month"] if not monthly.empty else "—"
i1, i2, i3 = st.columns(3)
for col, label, value, desc in [
    (i1, "Leading region", best_region, "Highest revenue contribution"),
    (i2, "Top product", best_product, "Highest product revenue"),
    (i3, "Best month", peak_month, "Peak revenue month in selection"),
]:
    with col:
        st.markdown(f'<div class="insight-card"><div class="insight-label">{label}</div><div class="insight-value">{value}</div><div class="insight-desc">{desc}</div></div>', unsafe_allow_html=True)

# Detail table
st.markdown('<div class="section-title">Recent transactions <span>DETAIL VIEW</span></div>', unsafe_allow_html=True)
search = st.text_input("Search order, product or region", placeholder="e.g. ORD0012, Laptop, West")
table = df.copy()
if search.strip():
    mask = table.astype(str).apply(lambda s: s.str.contains(search.strip(), case=False, na=False)).any(axis=1)
    table = table[mask]
table = table.sort_values("Order_Date", ascending=False)
st.dataframe(table.head(100), use_container_width=True, hide_index=True)
st.download_button("↓  Export filtered transactions (CSV)", table.to_csv(index=False).encode("utf-8"),
                   "sales_transactions.csv", "text/csv", use_container_width=False)

st.markdown(
    f'<div class="footer-note">Showing <b>{len(df):,}</b> records after filters · '
    f'{quality["duplicates_removed"]:,} duplicate rows removed · {quality["invalid_rows_removed"]:,} invalid rows removed during cleaning.</div>',
    unsafe_allow_html=True,
)
