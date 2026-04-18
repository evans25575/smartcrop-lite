# 🌱 SmartCrop Lite v2.0
### Geospatial Agricultural Decision-Support System for Smallholder Farmers

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Built for OAF R&D](https://img.shields.io/badge/Built%20for-Agricultural%20R%26D-brightgreen)](https://oneacrefund.org)

---

## 📌 Overview

SmartCrop Lite is a **geospatial agricultural decision-support system** that integrates market price data, rainfall monitoring (CHIRPS-style), and soil analysis (iSDA-style) to generate localised, data-driven recommendations for smallholder farmers across Kenya.

The platform enables farmers, agronomists, and field programme teams to make informed decisions on:
- **When to plant** — based on rainfall anomalies vs 20-year averages
- **Where to sell** — based on county-level market price comparisons
- **What inputs to apply** — based on soil pH, fertility, and nutrient profiles

> *"Built to demonstrate geospatial agricultural analytics for smallholder farmer decision-support — directly aligned with One Acre Fund R&D analytical methods."*

---

## 🚀 Features (v2.0)

### 🗺️ Geospatial Maps
- **Crop price bubble map** — county-level price distribution across Kenya (Plotly Mapbox)
- **Rainfall anomaly map** — % deviation from 20-year average by county and month
- **Soil fertility map** — county soil fertility and pH distribution

### 📈 Price Analytics
- Price trend analysis over time (county + crop)
- Cross-county price comparison bar chart
- Automated buy/sell/hold recommendations based on price trend direction

### 🌧️ Rainfall & Planting Windows
- Monthly rainfall vs long-term average (CHIRPS-style data)
- **Planting signal heatmap** — county × month matrix showing Plant / Watch / Delay signals
- Automated planting window recommendation with agronomic rationale

### 🌍 Soil & Input Recommendations
- Soil profile: pH, texture, drainage, organic carbon, N/P/K
- **Nutrient radar chart** — visual soil health profile
- **Lime and fertiliser recommendations** (e.g., CAN, DAP application rates)
- iSDA-style soil data integration

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Frontend | Streamlit |
| Data Manipulation | Python, Pandas, NumPy |
| Geospatial | GeoPandas, Plotly Mapbox |
| Visualisation | Plotly Express, Plotly Graph Objects |
| Data Sources | CHIRPS (rainfall), iSDA Africa (soil), County market surveys |
| Version Control | Git / GitHub |

---

## 📂 Project Structure

```
smartcrop-lite/
│── app.py                  # Main Streamlit application
│── requirements.txt        # Dependencies
│── README.md
│── data/
│   ├── prices.csv          # County crop market price data (lat/lon enabled)
│   ├── rainfall.csv        # CHIRPS-style monthly rainfall + planting signals
│   └── soil.csv            # iSDA-style soil profiles + input recommendations
└── images/
    └── dashboard.png       # Sample dashboard screenshot
```

---

## ▶️ How to Run

```bash
git clone https://github.com/evans25575/smartcrop-lite.git
cd smartcrop-lite
pip install -r requirements.txt
streamlit run app.py
```

---

## 📊 Data Sources & Methodology

| Dataset | Source | Description |
|---|---|---|
| Rainfall | CHIRPS (Climate Hazards Group) | Monthly precipitation, anomaly vs 20-year baseline |
| Soil | iSDA Africa | pH, N/P/K, organic carbon, soil texture by county |
| Prices | County market surveys | Weekly crop prices across major Kenyan markets |

### Planting Signal Logic
| Signal | Condition | Recommendation |
|---|---|---|
| ✅ PLANT | Rainfall ≥ long-term average (anomaly ≥ 0%) | Proceed — moisture conditions favourable |
| ⚠️ WATCH | Rainfall within -15% of average | Monitor — wait for further rainfall before planting |
| ❌ DELAY | Rainfall < -15% of average | Delay — high risk of crop failure under current conditions |

### Fertiliser Recommendation Logic
- Soil pH < 5.5 → Lime application (tonnes/ha) calculated before fertiliser
- N-deficient soils → Higher CAN rates recommended
- All recommendations follow Kenya Ministry of Agriculture guidelines

---

## 🎯 Use Case

Built for:
- **Smallholder farmers** — making planting and selling decisions
- **Agronomists & field officers** — county-level programme targeting
- **Agricultural R&D teams** — integrating spatial data into decision-support tools
- **Programme managers** — monitoring seasonal conditions across geographies

---

## 🌍 Impact

SmartCrop Lite v2.0 contributes to:
- 📉 Reduced crop failure risk through data-driven planting window guidance
- 💰 Increased farmer income through market arbitrage price awareness
- 🌱 Improved soil health through localised input recommendations
- 🗺️ Geospatially targeted programme design and farmer support

---

## 🔮 Roadmap

- [ ] CHIRPS API live integration (real-time rainfall data)
- [ ] iSDA Africa API integration (live soil layers)
- [ ] NDVI vegetation index integration (Sentinel-2 / Google Earth Engine)
- [ ] Sowing date optimisation model (Growing Degree Days)
- [ ] SMS alert integration for low-connectivity users
- [ ] Expansion to Uganda, Rwanda, Tanzania, Ethiopia (OAF countries of operation)
- [ ] GxE interaction modelling for variety × environment recommendations

---

## 👨‍💻 Author

**Evans Kiplangat** — Data Analyst | Agricultural Analytics | Geospatial Data Systems

- 🌐 [GitHub](https://github.com/evans25575)
- 💼 [LinkedIn](https://www.linkedin.com/in/evans-kiplangat-375646179)
- 📧 kiplaevans2018@gmail.com

---

## 📄 License

MIT License — open for research collaboration and adaptation.

---

*SmartCrop Lite is an open-source agricultural analytics project. Data used is for demonstration purposes. For production deployment, connect live CHIRPS, iSDA, and market price API feeds.*
