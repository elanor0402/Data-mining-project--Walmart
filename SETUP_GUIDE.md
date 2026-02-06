# Walmart Supply Chain Command Center — v2.0

## Quick Start

### Prerequisites
- Python 3.9+

### Installation

```bash
cd walmart-dashboard
python -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows
pip install -r requirements.txt
streamlit run app.py
```

Opens at **http://localhost:8501**

## Dashboard Tabs

| Tab | Description |
|-----|-------------|
| 📊 Overview | Weekly demand trends, revenue at risk, category/regional snapshots |
| 🗺️ Geographic | Interactive US map with bubble markers, store cards, heatmap |
| ⚡ Performance | Location & category breakdown, regional comparison |
| 🌦️ Weather | Stockout rates by weather, variance trends, radar profiles |
| 🔍 Anomalies | 3,097 anomalies — scatter plots, top revenue-at-risk table |
| 🎯 Action Deck | 4,003 AI recommendations, priority distribution, critical actions |
| 🤖 ML Insights | 5-model comparison, feature importance, cross-validation |
| 💾 Data Explorer | Browse all 14 datasets with download |

## Data Files (in data/)
- walmart_sccc_enriched_data.csv — 5,000 transactions (64 cols)
- walmart_sccc_action_deck.csv — 4,003 AI recommendations
- walmart_sccc_anomaly_watchlist.csv — 3,097 detected anomalies
- action_deck.csv — 4,015 full action deck entries
- kpi_metrics.csv, location_stats.csv, category_stats.csv
- regional_stats.csv, weather_impact.csv, weekly_trends.csv
- weather_variance.csv, weather_alerts.csv

## Troubleshooting
- ModuleNotFoundError → activate venv + pip install
- FileNotFoundError → verify data/ folder exists
- Port in use → streamlit run app.py --server.port 8502
