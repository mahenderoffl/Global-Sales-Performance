# Global Sales Performance Dashboard Configuration

## Project Overview
PROJECT_NAME = "Global Sales Performance Dashboard"
VERSION = "1.0.0"
AUTHOR = "Dashboard Generator"
DESCRIPTION = "Interactive dashboard for analyzing global sales performance across continents and regions"

## Dashboard Configuration
DASHBOARD_TITLE = "🌍 Global Sales Performance Dashboard"
DASHBOARD_PORT = 8501
DASHBOARD_HOST = "localhost"

## Data Configuration
DEFAULT_DATA_PATH = "data/sample_sales_data.csv"
REQUIRED_COLUMNS = ["Country", "Region", "Sales"]
OPTIONAL_COLUMNS = ["Profit", "Year", "Date", "Product_Category"]

## Visualization Configuration
CHART_HEIGHT = 500
MAP_HEIGHT = 600
KPI_CARD_HEIGHT = 150

## Color Schemes
CONTINENT_COLORS = {
    'North America': '#1f77b4',
    'South America': '#ff7f0e', 
    'Europe': '#2ca02c',
    'Asia': '#d62728',
    'Africa': '#9467bd',
    'Oceania': '#8c564b'
}

## Number Formatting
CURRENCY_SYMBOL = "$"
DECIMAL_PLACES = 2

## Export Configuration
EXPORT_FORMATS = ["CSV", "Excel", "JSON"]
EXPORT_DIRECTORY = "exports"

## Performance Settings
MAX_ROWS_DISPLAY = 10000
CACHE_TTL = 3600  # seconds

## Feature Flags
ENABLE_MAP_VISUALIZATION = True
ENABLE_TREND_ANALYSIS = True
ENABLE_PROFIT_ANALYSIS = True
ENABLE_EXPORT_FEATURES = True
ENABLE_FILTERS = True
