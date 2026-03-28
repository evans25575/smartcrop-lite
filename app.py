import streamlit as st
import pandas as pd

st.set_page_config(page_title="SmartCrop Lite", layout="centered")

st.title("🌱 SmartCrop Lite Dashboard")
st.write("Real-time Market & Climate Insights for Farmers")

# Load data
data = pd.read_csv("data/prices.csv")

st.subheader("📊 Current Market Prices")
st.bar_chart(data.set_index("Crop"))

# Insights
st.subheader("📈 Insights")
highest = data.loc[data["Price_KSh"].idxmax()]
lowest = data.loc[data["Price_KSh"].idxmin()]

st.write(f"💰 Highest Price Crop: **{highest['Crop']}** (KSh {highest['Price_KSh']})")
st.write(f"📉 Lowest Price Crop: **{lowest['Crop']}** (KSh {lowest['Price_KSh']})")

# Recommendations
st.subheader("🧠 Recommendation")
st.info("Farmers are advised to sell high-value crops this week and monitor weather conditions before planting.")

# Weather alert
st.subheader("🌦️ Weather Alert")
st.warning("Moderate rainfall expected this week. Plan planting accordingly.")
