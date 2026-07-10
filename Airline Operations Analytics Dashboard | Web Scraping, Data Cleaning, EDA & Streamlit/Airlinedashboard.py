import streamlit as st
import pandas as pd

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Airline Operations Analytics Dashboard",
    page_icon="✈",
    layout="wide"
)

# -----------------------------
# Load Dataset
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Airline_final.csv")
    return df

df = load_data()

# -----------------------------
# Dashboard Title
# -----------------------------
st.title("✈ Airline Operations Analytics Dashboard")
st.markdown("""
Analyze airline operational performance, customer satisfaction,
flight delays and airport efficiency through interactive visualizations.
""")

st.markdown("---")

# ==========================================================
# Sidebar
# ==========================================================

st.sidebar.header("🔎 Filters")

# Airline Filter
airline = st.sidebar.selectbox(
    "Select Airline",
    ["All"] + sorted(df["Airline"].unique())
)

# Status Filter
status = st.sidebar.selectbox(
    "Flight Status",
    ["All"] + sorted(df["Status"].unique())
)

# Origin Airport
origin = st.sidebar.selectbox(
    "Origin Airport",
    ["All"] + sorted(df["Origin_Airport"].unique())
)

# Destination Airport
destination = st.sidebar.selectbox(
    "Destination Airport",
    ["All"] + sorted(df["Destination_Airport"].unique())
)

# Recommendation Filter
recommend = st.sidebar.selectbox(
    "Recommended",
    ["All"] + sorted(df["Recommended"].unique())
)

# ==========================================================
# Apply Filters
# ==========================================================

filtered_df = df.copy()

if airline != "All":
    filtered_df = filtered_df[
        filtered_df["Airline"] == airline
    ]

if status != "All":
    filtered_df = filtered_df[
        filtered_df["Status"] == status
    ]

if origin != "All":
    filtered_df = filtered_df[
        filtered_df["Origin_Airport"] == origin
    ]

if destination != "All":
    filtered_df = filtered_df[
        filtered_df["Destination_Airport"] == destination
    ]

if recommend != "All":
    filtered_df = filtered_df[
        filtered_df["Recommended"] == recommend
    ]

# ==========================================================
# KPI Cards
# ==========================================================

st.subheader("📌 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

col4, col5, col6 = st.columns(3)

# KPI 1
col1.metric(
    "✈ Total Flights",
    f"{len(filtered_df):,}"
)

# KPI 2
col2.metric(
    "⏱ Average Delay (Min)",
    round(filtered_df["Delay_Minutes"].mean(),2)
)

# KPI 3
col3.metric(
    "⭐ Average Rating",
    round(filtered_df["Overall_Rating"].mean(),2)
)

# KPI 4
on_time = (
    filtered_df["Status"]=="On Time"
).sum()

col4.metric(
    "✅ On-Time Flights",
    on_time
)

# KPI 5
cancelled = (
    filtered_df["Status"]=="Cancelled"
).sum()

col5.metric(
    "❌ Cancelled Flights",
    cancelled
)

# KPI 6
recommend_rate = (
    (filtered_df["Recommended"]=="Yes").mean()
)*100

col6.metric(
    "👍 Recommendation Rate",
    f"{recommend_rate:.1f}%"
)

st.markdown("---")

import plotly.express as px
import plotly.graph_objects as go
st.subheader("📊 Average Delay by Airline")

delay = (
    filtered_df.groupby("Airline")["Delay_Minutes"]
    .mean()
    .reset_index()
)

fig = px.bar(
    delay,
    x="Airline",
    y="Delay_Minutes",
    color="Delay_Minutes",
    text_auto=".2f",
    title="Average Flight Delay",
    color_continuous_scale="Blues"
)

fig.update_layout(
    xaxis_title="Airline",
    yaxis_title="Average Delay (Minutes)",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🥧 Flight Status Distribution")

status = (
    filtered_df["Status"]
    .value_counts()
    .reset_index()
)

status.columns = ["Status","Flights"]

fig = px.pie(
    status,
    names="Status",
    values="Flights",
    hole=0.45
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.subheader("🛫 Origin Airport Traffic")

origin = (
    filtered_df["Origin_Airport"]
    .value_counts()
    .reset_index()
)

origin.columns=["Airport","Flights"]

fig = px.bar(
    origin,
    x="Airport",
    y="Flights",
    color="Flights",
    text_auto=True,
    color_continuous_scale="Viridis"
)

fig.update_layout(
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🛬 Destination Airport Traffic")

destination = (
    filtered_df["Destination_Airport"]
    .value_counts()
    .reset_index()
)

destination.columns=["Airport","Flights"]

fig = px.bar(
    destination,
    x="Airport",
    y="Flights",
    color="Flights",
    text_auto=True,
    color_continuous_scale="Plasma"
)

fig.update_layout(
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("⏱ Delay Distribution")

fig = px.histogram(
    filtered_df,
    x="Delay_Minutes",
    nbins=30,
    color_discrete_sequence=["royalblue"]
)

fig.update_layout(
    template="plotly_white",
    xaxis_title="Delay (Minutes)",
    yaxis_title="Flights"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📈 Delay vs Overall Rating")

fig = px.scatter(
    filtered_df,
    x="Delay_Minutes",
    y="Overall_Rating",
    color="Airline",
    hover_data=[
        "Origin_Airport",
        "Destination_Airport"
    ]
)

fig.update_layout(
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.header("⭐ Customer Experience Analytics")

st.subheader("⭐ Average Overall Rating by Airline")

rating = (
    filtered_df.groupby("Airline")["Overall_Rating"]
    .mean()
    .reset_index()
)

fig = px.bar(
    rating,
    x="Airline",
    y="Overall_Rating",
    color="Overall_Rating",
    text_auto=".2f",
    color_continuous_scale="Greens"
)

fig.update_layout(
    template="plotly_white",
    xaxis_title="Airline",
    yaxis_title="Average Rating"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("💰 Average Value For Money")

value = (
    filtered_df.groupby("Airline")["Value_For_Money"]
    .mean()
    .reset_index()
)

fig = px.bar(
    value,
    x="Airline",
    y="Value_For_Money",
    color="Value_For_Money",
    text_auto=".2f",
    color_continuous_scale="Teal"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.subheader("💺 Seat Comfort Rating")

seat = (
    filtered_df.groupby("Airline")["Seat_Comfort"]
    .mean()
    .reset_index()
)

fig = px.bar(
    seat,
    x="Airline",
    y="Seat_Comfort",
    color="Seat_Comfort",
    text_auto=".2f",
    color_continuous_scale="Purples"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.subheader("👨‍✈️ Cabin Staff Service")

staff = (
    filtered_df.groupby("Airline")["Cabin_Staff_Service"]
    .mean()
    .reset_index()
)

fig = px.bar(
    staff,
    x="Airline",
    y="Cabin_Staff_Service",
    color="Cabin_Staff_Service",
    text_auto=".2f",
    color_continuous_scale="Bluered"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.subheader("🍽 Food & Beverages Rating")

food = (
    filtered_df.groupby("Airline")["Food_Beverages"]
    .mean()
    .reset_index()
)

fig = px.bar(
    food,
    x="Airline",
    y="Food_Beverages",
    color="Food_Beverages",
    text_auto=".2f",
    color_continuous_scale="Oranges"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.subheader("🎬 Inflight Entertainment")

ent = (
    filtered_df.groupby("Airline")["Inflight_Entertainment"]
    .mean()
    .reset_index()
)

fig = px.bar(
    ent,
    x="Airline",
    y="Inflight_Entertainment",
    color="Inflight_Entertainment",
    text_auto=".2f",
    color_continuous_scale="Turbo"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.subheader("👍 Most Recommended Airlines")

recommend = (
    filtered_df.groupby("Airline")["Recommended"]
    .apply(lambda x: (x == "Yes").mean() * 100)
    .reset_index(name="Recommendation")
)

recommend = recommend.sort_values(
    by="Recommendation",
    ascending=False
)

fig = px.bar(
    recommend,
    x="Airline",
    y="Recommendation",
    color="Recommendation",
    text_auto=".1f",
    color_continuous_scale="RdYlGn"
)

fig.update_layout(
    template="plotly_white",
    xaxis_title="Airline",
    yaxis_title="Recommendation (%)"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("⭐ Airline Service Comparison")

compare = (
    filtered_df.groupby("Airline")[
        [
            "Overall_Rating",
            "Seat_Comfort",
            "Cabin_Staff_Service",
            "Food_Beverages",
            "Inflight_Entertainment",
            "Value_For_Money"
        ]
    ]
    .mean()
    .reset_index()
)

fig = px.line(
    compare,
    x="Airline",
    y=[
        "Overall_Rating",
        "Seat_Comfort",
        "Cabin_Staff_Service",
        "Food_Beverages",
        "Inflight_Entertainment",
        "Value_For_Money"
    ],
    markers=True
)

fig.update_layout(
    template="plotly_white",
    yaxis_title="Average Rating"
)

st.plotly_chart(fig, use_container_width=True)

import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.markdown("---")
st.header("🔥 Advanced Analytics")

st.subheader("Correlation Heatmap")

numeric_df = filtered_df.select_dtypes(include="number")

fig, ax = plt.subplots(figsize=(10,6))

sns.heatmap(
    numeric_df.corr(),
    annot=True,
    cmap="RdYlBu",
    linewidths=0.5,
    ax=ax
)

st.pyplot(fig)

filtered_df["Scheduled_Time"] = pd.to_datetime(filtered_df["Scheduled_Time"])

monthly = filtered_df.copy()
monthly["Month"] = monthly["Scheduled_Time"].dt.strftime("%b")

month_order = [
    "Jan","Feb","Mar","Apr","May","Jun",
    "Jul","Aug","Sep","Oct","Nov","Dec"
]

monthly["Month"] = pd.Categorical(
    monthly["Month"],
    categories=month_order,
    ordered=True
)

monthly = (
    monthly.groupby("Month")
    .size()
    .reset_index(name="Flights")
)

st.subheader("📊 Monthly Flight Trends")

fig = px.line(
    monthly,
    x="Month",
    y="Flights",
    markers=True
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

delay = filtered_df.copy()

delay["Month"] = delay["Scheduled_Time"].dt.strftime("%b")

delay["Month"] = pd.Categorical(
    delay["Month"],
    categories=month_order,
    ordered=True
)

delay = (
    delay.groupby("Month")["Delay_Minutes"]
    .mean()
    .reset_index()
)

st.subheader("📉 Monthly Average Delay")

fig = px.line(
    delay,
    x="Month",
    y="Delay_Minutes",
    markers=True
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.subheader("🛫 Top 10 Origin Airports")

top_origin = (
    filtered_df["Origin_Airport"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_origin.columns = ["Airport","Flights"]

fig = px.bar(
    top_origin,
    x="Airport",
    y="Flights",
    text_auto=True,
    color="Flights",
    color_continuous_scale="Viridis"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.subheader("🛬 Top 10 Destination Airports")

top_destination = (
    filtered_df["Destination_Airport"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_destination.columns = ["Airport","Flights"]

fig = px.bar(
    top_destination,
    x="Airport",
    y="Flights",
    text_auto=True,
    color="Flights",
    color_continuous_scale="Plasma"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.subheader("📋 Dataset Preview")

st.dataframe(
    filtered_df,
    use_container_width=True
)

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv,
    file_name="Filtered_Airline_Data.csv",
    mime="text/csv"
)

st.markdown("---")

st.success(f"""
Dashboard Summary

✈ Total Flights : {len(filtered_df)}

⭐ Average Rating : {filtered_df['Overall_Rating'].mean():.2f}

⏱ Average Delay : {filtered_df['Delay_Minutes'].mean():.2f} Minutes

👍 Recommendation Rate : {((filtered_df['Recommended']=="Yes").mean()*100):.1f}%
""")


