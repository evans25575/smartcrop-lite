"""
SmartCrop Lite — Geospatial Agricultural Decision-Support System
Built by Evans Kiplangat | github.com/evans25575

Integrates:
- Real-time market price data by county
- CHIRPS-style rainfall monitoring & planting window analysis
- iSDA-style soil data with fertiliser & lime recommendations
- Geospatial price & rainfall maps using Plotly
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SmartCrop Lite",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #2E7D32;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1rem;
        color: #555;
        margin-top: 0;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #f1f8f1;
        border-left: 4px solid #2E7D32;
        padding: 0.8rem 1rem;
        border-radius: 6px;
        margin-bottom: 0.5rem;
    }
    .alert-plant {
        background: #e8f5e9;
        border-left: 4px solid #43A047;
        padding: 0.6rem 1rem;
        border-radius: 4px;
        color: #1B5E20;
        font-weight: 600;
    }
    .alert-watch {
        background: #fff8e1;
        border-left: 4px solid #FFB300;
        padding: 0.6rem 1rem;
        border-radius: 4px;
        color: #7B5800;
        font-weight: 600;
    }
    .alert-delay {
        background: #fce4ec;
        border-left: 4px solid #E53935;
        padding: 0.6rem 1rem;
        border-radius: 4px;
        color: #7B0000;
        font-weight: 600;
    }
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #2E7D32;
        border-bottom: 2px solid #A5D6A7;
        padding-bottom: 4px;
        margin-bottom: 1rem;
    }
    .stSelectbox label { font-weight: 600; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── Data Loaders ─────────────────────────────────────────────────────────────
@st.cache_data
def load_prices():
    df = pd.read_csv("data/prices.csv", parse_dates=["date"])
    return df

@st.cache_data
def load_rainfall():
    return pd.read_csv("data/rainfall.csv")

@st.cache_data
def load_soil():
    return pd.read_csv("data/soil.csv")

prices_df = load_prices()
rainfall_df = load_rainfall()
soil_df = load_soil()

COUNTIES = sorted(prices_df["county"].unique().tolist())
CROPS = sorted(prices_df["crop"].unique().tolist())
MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://raw.githubusercontent.com/evans25575/smartcrop-lite/main/images/dashboard.png",
             use_column_width=True)
    st.markdown("### 🌱 SmartCrop Lite")
    st.markdown("*Geospatial Agricultural Decision-Support*")
    st.markdown("---")
    selected_county = st.selectbox("📍 Select Your County", COUNTIES)
    selected_crop = st.selectbox("🌾 Select Crop", CROPS)
    selected_month = st.selectbox("📅 Select Month", MONTHS,
                                   index=MONTHS.index("April"))
    st.markdown("---")
    st.markdown("**Data Sources**")
    st.markdown("- Market: County price surveys")
    st.markdown("- Rainfall: CHIRPS-style monitoring")
    st.markdown("- Soil: iSDA Africa soil layers")
    st.markdown("---")
    st.markdown("👨‍💻 **Evans Kiplangat**")
    st.markdown("[GitHub](https://github.com/evans25575/smartcrop-lite) · [LinkedIn](https://www.linkedin.com/in/evans-kiplangat-375646179)")

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown('<p class="main-header">🌱 SmartCrop Lite</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Geospatial Agricultural Decision-Support for Smallholder Farmers · Kenya</p>',
            unsafe_allow_html=True)

# ─── Top KPI Row ──────────────────────────────────────────────────────────────
county_prices = prices_df[
    (prices_df["county"] == selected_county) &
    (prices_df["crop"] == selected_crop)
].sort_values("date")

county_rain = rainfall_df[
    (rainfall_df["county"] == selected_county) &
    (rainfall_df["month"] == selected_month)
]

county_soil = soil_df[soil_df["county"] == selected_county]

col1, col2, col3, col4 = st.columns(4)

with col1:
    if not county_prices.empty:
        latest_price = county_prices.iloc[-1]["price_ksh_per_kg"]
        prev_price = county_prices.iloc[-2]["price_ksh_per_kg"] if len(county_prices) > 1 else latest_price
        delta = latest_price - prev_price
        st.metric(f"💰 {selected_crop} Price", f"KSh {latest_price}/kg",
                  delta=f"{delta:+.0f} vs last month")
    else:
        st.metric("💰 Price", "N/A", delta="No data")

with col2:
    if not county_rain.empty:
        rain_val = county_rain.iloc[0]["rainfall_mm"]
        avg_val = county_rain.iloc[0]["long_term_avg_mm"]
        anomaly = county_rain.iloc[0]["anomaly_pct"]
        st.metric("🌧️ Rainfall", f"{rain_val} mm",
                  delta=f"{anomaly:+.1f}% vs 20yr avg")
    else:
        st.metric("🌧️ Rainfall", "N/A")

with col3:
    if not county_soil.empty:
        ph = county_soil.iloc[0]["ph"]
        fertility = county_soil.iloc[0]["fertility_rating"]
        st.metric("🌍 Soil pH", f"{ph}", delta=f"Fertility: {fertility}")
    else:
        st.metric("🌍 Soil pH", "N/A")

with col4:
    if not county_rain.empty:
        signal = county_rain.iloc[0]["planting_signal"]
        signal_map = {"Plant": "✅ PLANT NOW", "Watch": "⚠️ MONITOR", "Delay": "❌ DELAY"}
        st.metric("🌱 Planting Signal", signal_map.get(signal, signal))

st.markdown("---")

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Geospatial Maps",
    "📈 Price Analytics",
    "🌧️ Rainfall & Planting Windows",
    "🌍 Soil & Input Recommendations"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — GEOSPATIAL MAPS
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<p class="section-title">🗺️ Geospatial Analysis — Kenya County-Level View</p>',
                unsafe_allow_html=True)

    map_col1, map_col2 = st.columns(2)

    # Map 1 — Crop Price by County
    with map_col1:
        st.markdown(f"**{selected_crop} Price Distribution (KSh/kg)**")
        latest_prices = (
            prices_df[prices_df["crop"] == selected_crop]
            .sort_values("date")
            .groupby("county")
            .last()
            .reset_index()
        )
        fig_price_map = px.scatter_mapbox(
            latest_prices,
            lat="latitude", lon="longitude",
            size="price_ksh_per_kg",
            color="price_ksh_per_kg",
            hover_name="county",
            hover_data={"price_ksh_per_kg": True, "market": True,
                        "latitude": False, "longitude": False},
            color_continuous_scale="YlGn",
            size_max=35,
            zoom=5.5,
            center={"lat": 0.2, "lon": 37.5},
            mapbox_style="carto-positron",
            title=f"{selected_crop} Prices by County",
            labels={"price_ksh_per_kg": "Price (KSh/kg)"}
        )
        fig_price_map.update_layout(
            height=420, margin={"r": 0, "t": 30, "l": 0, "b": 0},
            coloraxis_colorbar=dict(title="KSh/kg")
        )
        st.plotly_chart(fig_price_map, use_container_width=True)
        st.caption("💡 Larger bubbles = higher prices. Use this to identify best selling markets.")

    # Map 2 — Rainfall Anomaly by County
    with map_col2:
        st.markdown(f"**Rainfall Anomaly — {selected_month} 2026 (% vs 20-yr avg)**")
        month_rain = rainfall_df[rainfall_df["month"] == selected_month]
        color_scale = [
            [0.0, "#D32F2F"],   # red = severe deficit
            [0.3, "#FF8F00"],   # orange = deficit
            [0.5, "#FFF9C4"],   # yellow = near normal
            [0.7, "#81C784"],   # light green = surplus
            [1.0, "#1B5E20"],   # dark green = high surplus
        ]
        fig_rain_map = px.scatter_mapbox(
            month_rain,
            lat="latitude", lon="longitude",
            size=month_rain["rainfall_mm"].apply(lambda x: max(x, 10)),
            color="anomaly_pct",
            hover_name="county",
            hover_data={"rainfall_mm": True, "long_term_avg_mm": True,
                        "anomaly_pct": True, "planting_signal": True,
                        "latitude": False, "longitude": False},
            color_continuous_scale=color_scale,
            size_max=35,
            zoom=5.5,
            center={"lat": 0.2, "lon": 37.5},
            mapbox_style="carto-positron",
            title=f"Rainfall Anomaly — {selected_month}",
            labels={"anomaly_pct": "Anomaly (%)"}
        )
        fig_rain_map.update_layout(
            height=420, margin={"r": 0, "t": 30, "l": 0, "b": 0},
            coloraxis_colorbar=dict(title="Anomaly %")
        )
        st.plotly_chart(fig_rain_map, use_container_width=True)
        st.caption("💡 Green = above-average rainfall (good for planting). Red = deficit (delay planting).")

    # Map 3 — Soil Fertility
    st.markdown("**Soil Fertility & pH — County Overview**")
    fertility_colors = {"High": "#2E7D32", "Medium": "#F9A825", "Low": "#C62828"}
    soil_df["fertility_color"] = soil_df["fertility_rating"].map(fertility_colors)
    fig_soil_map = px.scatter_mapbox(
        soil_df,
        lat="latitude", lon="longitude",
        color="fertility_rating",
        size="ph",
        hover_name="county",
        hover_data={"soil_type": True, "ph": True, "fertility_rating": True,
                    "nitrogen_pct": True, "lime_recommendation_tonnes_ha": True,
                    "fertiliser_recommendation": True,
                    "latitude": False, "longitude": False},
        color_discrete_map={"High": "#2E7D32", "Medium": "#F9A825", "Low": "#C62828"},
        size_max=30,
        zoom=5.5,
        center={"lat": 0.2, "lon": 37.5},
        mapbox_style="carto-positron",
        title="Soil Fertility by County (sized by pH)",
    )
    fig_soil_map.update_layout(height=420, margin={"r": 0, "t": 30, "l": 0, "b": 0})
    st.plotly_chart(fig_soil_map, use_container_width=True)
    st.caption("💡 Green = High fertility. Red = Low fertility requiring lime & fertiliser inputs. Size = soil pH.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — PRICE ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<p class="section-title">📈 Market Price Analytics</p>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        # Price trend over time for selected county + crop
        st.markdown(f"**{selected_crop} Price Trend — {selected_county}**")
        if not county_prices.empty:
            fig_trend = px.line(
                county_prices, x="date", y="price_ksh_per_kg",
                markers=True,
                labels={"price_ksh_per_kg": "Price (KSh/kg)", "date": "Month"},
                color_discrete_sequence=["#2E7D32"]
            )
            fig_trend.update_traces(line_width=2.5, marker_size=8)
            fig_trend.update_layout(height=320, margin={"t": 10, "b": 10})
            st.plotly_chart(fig_trend, use_container_width=True)

            # Price trend insight
            if len(county_prices) >= 2:
                trend = county_prices["price_ksh_per_kg"].iloc[-1] - county_prices["price_ksh_per_kg"].iloc[0]
                if trend > 0:
                    st.markdown(f'<div class="alert-plant">📈 Price rising +KSh {trend:.0f}/kg over tracked period — consider holding stock.</div>', unsafe_allow_html=True)
                elif trend < 0:
                    st.markdown(f'<div class="alert-delay">📉 Price falling KSh {abs(trend):.0f}/kg — consider selling now.</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="alert-watch">➡️ Price stable — monitor market before deciding.</div>', unsafe_allow_html=True)
        else:
            st.info("No price trend data available for this selection.")

    with col_b:
        # Cross-county price comparison for selected crop
        st.markdown(f"**{selected_crop} Price Comparison — All Counties**")
        latest_all = (
            prices_df[prices_df["crop"] == selected_crop]
            .sort_values("date")
            .groupby("county")
            .last()
            .reset_index()
            .sort_values("price_ksh_per_kg", ascending=True)
        )
        fig_bar = px.bar(
            latest_all, x="price_ksh_per_kg", y="county",
            orientation="h",
            color="price_ksh_per_kg",
            color_continuous_scale="YlGn",
            labels={"price_ksh_per_kg": "Price (KSh/kg)", "county": "County"},
            text="price_ksh_per_kg"
        )
        fig_bar.update_traces(texttemplate="KSh %{text}", textposition="outside")
        fig_bar.update_layout(height=320, margin={"t": 10, "b": 10},
                              showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_bar, use_container_width=True)

        if not latest_all.empty:
            best_county = latest_all.iloc[-1]["county"]
            best_price = latest_all.iloc[-1]["price_ksh_per_kg"]
            st.markdown(f'<div class="alert-plant">💰 Best price for {selected_crop}: <b>{best_county}</b> at KSh {best_price}/kg</div>',
                        unsafe_allow_html=True)

    # All crops price table
    st.markdown("**Current Prices — All Crops in Selected County**")
    latest_county_all_crops = (
        prices_df[prices_df["county"] == selected_county]
        .sort_values("date")
        .groupby("crop")
        .last()
        .reset_index()[["crop", "price_ksh_per_kg", "market", "date"]]
        .rename(columns={"crop": "Crop", "price_ksh_per_kg": "Price (KSh/kg)",
                          "market": "Market", "date": "Date"})
    )
    st.dataframe(latest_county_all_crops, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — RAINFALL & PLANTING WINDOWS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<p class="section-title">🌧️ Rainfall Analysis & Planting Window Recommendations</p>',
                unsafe_allow_html=True)

    # County planting signal
    if not county_rain.empty:
        signal = county_rain.iloc[0]["planting_signal"]
        rain_val = county_rain.iloc[0]["rainfall_mm"]
        avg_val = county_rain.iloc[0]["long_term_avg_mm"]
        anomaly = county_rain.iloc[0]["anomaly_pct"]

        signal_css = {"Plant": "alert-plant", "Watch": "alert-watch", "Delay": "alert-delay"}
        signal_msg = {
            "Plant": f"✅ PLANT NOW — {selected_month} rainfall ({rain_val}mm) is {anomaly:+.1f}% above long-term average. Soil moisture conditions are favourable.",
            "Watch": f"⚠️ MONITOR — {selected_month} rainfall ({rain_val}mm) is {anomaly:+.1f}% vs average. Wait for confirmation of adequate soil moisture before planting.",
            "Delay": f"❌ DELAY PLANTING — {selected_month} rainfall ({rain_val}mm) is {anomaly:+.1f}% below average. Risk of crop failure is high. Wait for improvement."
        }
        st.markdown(f'<div class="{signal_css[signal]}">{signal_msg[signal]}</div>',
                    unsafe_allow_html=True)
        st.markdown("")

    col_r1, col_r2 = st.columns(2)

    with col_r1:
        # Rainfall bar chart — all months for selected county
        st.markdown(f"**Monthly Rainfall vs Long-Term Average — {selected_county}**")
        county_rain_all = rainfall_df[rainfall_df["county"] == selected_county].copy()
        county_rain_all["month_order"] = county_rain_all["month"].apply(
            lambda m: MONTHS.index(m) if m in MONTHS else 99
        )
        county_rain_all = county_rain_all.sort_values("month_order")

        fig_rain = go.Figure()
        fig_rain.add_trace(go.Bar(
            x=county_rain_all["month"], y=county_rain_all["rainfall_mm"],
            name="2026 Rainfall", marker_color="#42A5F5"
        ))
        fig_rain.add_trace(go.Scatter(
            x=county_rain_all["month"], y=county_rain_all["long_term_avg_mm"],
            name="20-yr Average", line=dict(color="#E53935", width=2, dash="dash"),
            mode="lines+markers"
        ))
        fig_rain.update_layout(
            height=320, margin={"t": 10, "b": 10},
            yaxis_title="Rainfall (mm)", xaxis_title="Month",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            barmode="group"
        )
        st.plotly_chart(fig_rain, use_container_width=True)

    with col_r2:
        # Planting signal heatmap across all counties and months
        st.markdown("**Planting Signal Calendar — All Counties**")
        signal_num = {"Plant": 2, "Watch": 1, "Delay": 0}
        rainfall_df["signal_num"] = rainfall_df["planting_signal"].map(signal_num)
        pivot = rainfall_df.pivot_table(
            index="county", columns="month", values="signal_num", aggfunc="first"
        )
        # Reorder months
        ordered_months = [m for m in MONTHS if m in pivot.columns]
        pivot = pivot[ordered_months]

        fig_heat = px.imshow(
            pivot,
            color_continuous_scale=["#EF5350", "#FFB300", "#66BB6A"],
            aspect="auto",
            labels=dict(color="Signal"),
            zmin=0, zmax=2
        )
        fig_heat.update_coloraxes(
            colorbar=dict(
                tickvals=[0, 1, 2],
                ticktext=["Delay", "Watch", "Plant"]
            )
        )
        fig_heat.update_layout(height=320, margin={"t": 10, "b": 10})
        st.plotly_chart(fig_heat, use_container_width=True)
        st.caption("💡 Green = Plant | Yellow = Watch | Red = Delay. Use this to plan your season.")

    # Rainfall anomaly table
    st.markdown("**Rainfall Anomaly Summary — All Counties**")
    rain_summary = rainfall_df[rainfall_df["month"] == selected_month][
        ["county", "rainfall_mm", "long_term_avg_mm", "anomaly_pct", "planting_signal"]
    ].rename(columns={
        "county": "County", "rainfall_mm": "Rainfall (mm)",
        "long_term_avg_mm": "20-yr Avg (mm)", "anomaly_pct": "Anomaly (%)",
        "planting_signal": "Signal"
    }).sort_values("Anomaly (%)", ascending=False)
    st.dataframe(rain_summary, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — SOIL & INPUT RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<p class="section-title">🌍 Soil Analysis & Input Recommendations</p>',
                unsafe_allow_html=True)

    if not county_soil.empty:
        soil = county_soil.iloc[0]

        # Recommendation card
        lime = soil["lime_recommendation_tonnes_ha"]
        fert = soil["fertiliser_recommendation"]
        fertility = soil["fertility_rating"]
        ph = soil["ph"]

        if lime > 0:
            st.markdown(
                f'<div class="alert-watch">⚠️ Soil pH {ph} — Apply {lime} tonnes/ha of lime before planting to correct acidity. '
                f'Then apply: {fert}</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="alert-plant">✅ Soil pH {ph} is within optimal range. Recommended inputs: {fert}</div>',
                unsafe_allow_html=True)
        st.markdown("")

        col_s1, col_s2 = st.columns(2)

        with col_s1:
            st.markdown(f"**Soil Profile — {selected_county}**")
            soil_metrics = {
                "Soil Type": soil["soil_type"],
                "pH": soil["ph"],
                "Texture": soil["texture"],
                "Drainage": soil["drainage"],
                "Fertility Rating": soil["fertility_rating"],
                "Organic Carbon (%)": soil["organic_carbon_pct"],
                "Nitrogen (%)": soil["nitrogen_pct"],
                "Phosphorus (ppm)": soil["phosphorus_ppm"],
                "Potassium (ppm)": soil["potassium_ppm"],
            }
            for k, v in soil_metrics.items():
                st.markdown(f'<div class="metric-card"><b>{k}:</b> {v}</div>',
                            unsafe_allow_html=True)

        with col_s2:
            # Nutrient radar chart
            st.markdown("**Nutrient Profile Radar**")
            categories = ["Nitrogen", "Phosphorus", "Potassium", "Organic Carbon", "pH Score"]
            # Normalise to 0-100 scale for radar
            values = [
                min(soil["nitrogen_pct"] / 0.30 * 100, 100),
                min(soil["phosphorus_ppm"] / 35 * 100, 100),
                min(soil["potassium_ppm"] / 350 * 100, 100),
                min(soil["organic_carbon_pct"] / 3.5 * 100, 100),
                min((soil["ph"] - 4.0) / (7.5 - 4.0) * 100, 100),
            ]
            fig_radar = go.Figure(go.Scatterpolar(
                r=values + [values[0]],
                theta=categories + [categories[0]],
                fill="toself",
                fillcolor="rgba(46,125,50,0.2)",
                line_color="#2E7D32",
                name=selected_county
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100],
                                   ticktext=["0", "25", "50", "75", "100"],
                                   tickvals=[0, 25, 50, 75, 100])
                ),
                height=350, margin={"t": 20, "b": 20},
                showlegend=False
            )
            st.plotly_chart(fig_radar, use_container_width=True)
            st.caption("💡 Higher scores = more fertile. Aim for balanced profile across all nutrients.")

        # All-county soil comparison table
        st.markdown("**Soil Fertility Comparison — All Counties**")
        soil_compare = soil_df[[
            "county", "soil_type", "ph", "fertility_rating",
            "lime_recommendation_tonnes_ha", "fertiliser_recommendation"
        ]].rename(columns={
            "county": "County", "soil_type": "Soil Type", "ph": "pH",
            "fertility_rating": "Fertility", "lime_recommendation_tonnes_ha": "Lime (t/ha)",
            "fertiliser_recommendation": "Fertiliser Recommendation"
        })
        st.dataframe(soil_compare, use_container_width=True, hide_index=True)

    else:
        st.info(f"No soil data available for {selected_county}. More counties coming soon.")

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "🌱 **SmartCrop Lite v2.0** · Built by [Evans Kiplangat](https://github.com/evans25575) · "
    "Data: CHIRPS (rainfall), iSDA Africa (soil), County Market Surveys (prices) · "
    "For One Acre Fund R&D alignment and smallholder farmer decision support"
)
