import plotly.express as px

BLUE = "#3978F6"

def trend(df):
    fig = px.area(df, x="Month", y="Revenue", markers=True)
    fig.update_traces(line=dict(color=BLUE, width=3), fillcolor="rgba(57,120,246,.12)")
    fig.update_layout(template="plotly_white", xaxis_title="", yaxis_title="Revenue (₹)",
                      hovermode="x unified", margin=dict(l=8,r=8,t=20,b=8))
    return fig

def bars(df, column, title, horizontal=False):
    if horizontal:
        fig = px.bar(df, x="Revenue", y=column, orientation="h", title=title,
                     color_discrete_sequence=[BLUE])
        fig.update_layout(yaxis={"categoryorder":"total ascending"})
    else:
        fig = px.bar(df, x=column, y="Revenue", title=title, color_discrete_sequence=[BLUE])
    fig.update_layout(template="plotly_white", showlegend=False, margin=dict(l=8,r=8,t=45,b=8))
    return fig
