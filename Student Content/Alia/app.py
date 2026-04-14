import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- 1. SETUP & GET DATA ---
st.set_page_config(page_title="Sleep Analytics", layout="wide")
st.title("🌙 Sleep Analysis Dashboard")

fp_sleep ="/workspaces/AIML-nexperts4/Student Content/Alia/Sleep_health_and_lifestyle_dataset.csv"

sleep_dt= pd.read_csv(fp_sleep)

@st.cache_data
def get_sleep_data():
    # Creating 30 days of synthetic data
    dates = pd.date_range(end=datetime.now(), periods=30)
    hours = np.random.normal(7.5, 0.8, 30).clip(5, 10)
    quality = np.random.randint(60, 100, 30)
    
    # Sleep stage breakdown
    deep = hours * np.random.uniform(0.15, 0.25, 30)
    rem = hours * np.random.uniform(0.20, 0.25, 30)
    light = hours - deep - rem
    
    return pd.DataFrame({
        "Date": dates, "Total Hours": hours, "Quality %": quality,
        "Deep": deep, "REM": rem, "Light": light
    })

df = get_sleep_data()

# --- 2. KEY METRICS ---
avg_sleep = sleep_dt["Sleep Duration"].mean()
avg_quality = sleep_dt["Quality of Sleep"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Avg Sleep Duration", f"{avg_sleep:.1f} hrs")
col2.metric("Avg Quality", f"{avg_quality:.0f}%")
col3.metric("Best Night", f"{df['Sleep Duration'].max():.1f} hrs")

# --- 3. VISUALISATIONS ---
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Total Sleep Trend")
    fig_line = px.line(df, x="Date", y="Total Hours", markers=True,
                       color_discrete_sequence=["#636EFA"])
    st.plotly_chart(fig_line, use_container_width=True)

with chart_col2:
    st.subheader("Sleep Quality Distribution")
    fig_hist = px.histogram(df, x="Quality %", nbins=10, 
                            color_discrete_sequence=["#00CC96"])
    st.plotly_chart(fig_hist, use_container_width=True)

st.subheader("Nightly Sleep Stage Breakdown")
# Reshaping data for a stacked bar chart
df_melted = df.melt(id_vars=["Date"], value_vars=["Deep", "REM", "Light"], 
                    var_name="Stage", value_name="Hours")

fig_bar = px.bar(df_melted, x="Date", y="Hours", color="Stage",
                 color_discrete_map={"Deep": "#0D2A63", "REM": "#19D3F3", "Light": "#AB63FA"})
st.plotly_chart(fig_bar, use_container_width=True)