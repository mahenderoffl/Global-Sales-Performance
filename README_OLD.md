# Global Sales Performance Dashboard

A comprehensive interactive dashboard for analyzing global sales performance across continents and regions, built with Python, Streamlit, and Plotly.

## 🌟 Features

- **📊 Interactive Geographic Visualization**: World map showing sales distribution by country with hover details
- **📈 Trend Analysis**: Line charts displaying sales growth over time by region
- **🏆 Performance Analytics**: Identify top-performing countries and regions
- **🔍 Advanced Filtering**: Filter by regions, years, and product categories
- **💰 Financial Metrics**: Sales, profit, and margin analysis
- **📋 Data Export**: Export filtered results to CSV/Excel
- **🎨 Multiple Dashboard Options**: Streamlit, Dash, and Jupyter Notebook versions

## 🚀 Quick Start

### Option 1: Using the Automated Launcher (Recommended)

1. **Windows Batch File**:
   ```cmd
   run_dashboard.bat
   ```

2. **PowerShell Script**:
   ```powershell
   .\run_dashboard.ps1
   ```

3. **Open your browser** and navigate to: `http://localhost:8501`

### Option 2: Manual Setup

1. **Clone or download** this project to your computer

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit dashboard**:
   ```bash
   cd src
   streamlit run dashboard.py
   ```

4. **Alternative: Run the Dash version**:
   ```bash
   cd src
   python dashboard_dash.py
   ```

5. **Or use the Jupyter Notebook**:
   ```bash
   jupyter notebook Sales_Dashboard_Analysis.ipynb
   ```

## 📁 Project Structure

```
visualization project/
├── 📁 data/                          # Dataset files
│   ├── sample_sales_data.csv         # Sample dataset (auto-generated)
│   ├── regional_summary.csv          # Exported regional summary
│   └── country_summary.csv           # Exported country summary
├── 📁 src/                           # Source code
│   ├── dashboard.py                  # Main Streamlit dashboard
│   ├── dashboard_dash.py             # Alternative Dash dashboard
│   ├── data_processor.py             # Data processing utilities
│   └── visualizations.py            # Chart and map creation functions
├── 📁 assets/                        # Static assets
│   └── style.css                     # Custom styling
├── Sales_Dashboard_Analysis.ipynb    # Jupyter notebook version
├── requirements.txt                  # Python dependencies
├── config.py                        # Configuration settings
├── run_dashboard.bat                 # Windows launcher
├── run_dashboard.ps1                 # PowerShell launcher
└── README.md                         # This file
```

## 📊 Data Requirements

### Required Columns
- `Country`: Country name (e.g., "United States", "Germany")
- `Region`: Geographic region/continent (e.g., "North America", "Europe")
- `Sales`: Sales amount (numeric)

### Optional Columns
- `Profit`: Profit amount (numeric) - enables profit analysis
- `Year`: Year (numeric) - enables trend analysis
- `Date`: Date (datetime) - enables time-based analysis
- `Product_Category`: Product category - enables product filtering

### Sample Data Format
```csv
Country,Region,Product_Category,Year,Sales,Profit
United States,North America,Electronics,2024,75000,22500
Germany,Europe,Clothing,2024,68000,20400
Japan,Asia,Electronics,2024,82000,24600
```

## 🎯 Dashboard Features

### 1. Key Performance Indicators (KPIs)
- **Total Sales**: Sum of all sales across selected filters
- **Total Profit**: Sum of all profit (if available)
- **Profit Margin**: Calculated profit percentage
- **Growth Rate**: Year-over-year growth (if time data available)
- **Geographic Coverage**: Number of countries and regions

### 2. Geographic Analysis
- **Interactive World Map**: Choropleth map showing sales distribution
- **Country Performance**: Detailed country-level analysis
- **Regional Comparison**: Side-by-side regional performance

### 3. Trend Analysis
- **Time Series Charts**: Sales trends over time by region
- **Growth Patterns**: Identify growing and declining markets
- **Seasonal Analysis**: Spot seasonal patterns (if monthly data available)

### 4. Top Performers
- **Top Countries**: Ranking by sales, profit, or growth
- **Regional Leaders**: Best performing regions
- **Performance Correlation**: Sales vs. profit relationship analysis

### 5. Interactive Filters
- **Region Selection**: Multi-select region filtering
- **Time Range**: Year or date range selection
- **Product Categories**: Filter by product types
- **Real-time Updates**: All charts update automatically

## 🛠️ Customization

### Adding Your Own Data

1. **Prepare your CSV/Excel file** with the required columns
2. **Use the file upload feature** in the dashboard sidebar
3. **Or replace** `data/sample_sales_data.csv` with your data
4. **Restart the dashboard** to load new data

### Modifying Visualizations

1. **Edit** `src/visualizations.py` to customize charts
2. **Update** `src/dashboard.py` to modify the layout
3. **Adjust** `config.py` for color schemes and settings

### Custom Analysis

1. **Use the Jupyter notebook** for custom analysis
2. **Import the data processor**: `from data_processor import SalesDataProcessor`
3. **Create custom visualizations**: Use the `SalesVisualizer` class
4. **Export results**: Built-in export functions available

## 📈 Sample Analysis Results

Using the included sample data, you can expect to see:

- **500+ data points** across 20 countries and 6 regions
- **5-year time series** (2020-2024) for trend analysis
- **5 product categories** for detailed segmentation
- **Geographic distribution** showing North America and Europe as top performers
- **Growth trends** indicating overall positive trajectory

## 🔧 Technical Details

### Technologies Used
- **Python 3.8+**: Core programming language
- **Streamlit**: Main dashboard framework
- **Plotly**: Interactive visualizations
- **Pandas**: Data processing and analysis
- **NumPy**: Numerical computations
- **Dash**: Alternative dashboard framework
- **Jupyter**: Notebook-based analysis

### Performance Optimizations
- **Data caching**: Reduces load times
- **Efficient aggregations**: Fast data processing
- **Lazy loading**: Charts load as needed
- **Memory management**: Optimized for large datasets

### Browser Compatibility
- **Chrome/Edge**: Fully supported
- **Firefox**: Fully supported
- **Safari**: Fully supported
- **Mobile**: Responsive design included

## 🎨 Dashboard Versions

### 1. Streamlit Dashboard (`dashboard.py`)
- **Best for**: General users, quick deployment
- **Features**: Full feature set, easy customization
- **URL**: `http://localhost:8501`

### 2. Dash Dashboard (`dashboard_dash.py`)
- **Best for**: Advanced users, enterprise deployment
- **Features**: More customizable, production-ready
- **URL**: `http://localhost:8050`

### 3. Jupyter Notebook (`Sales_Dashboard_Analysis.ipynb`)
- **Best for**: Data scientists, custom analysis
- **Features**: Step-by-step analysis, exportable results
- **Usage**: Open with Jupyter Lab/Notebook

## 📤 Export Options

### Available Formats
- **CSV**: Regional and country summaries
- **Excel**: Multi-sheet workbooks
- **PNG/PDF**: Chart exports (via Plotly)
- **JSON**: Raw data exports

### Export Locations
- Regional summary: `data/regional_summary.csv`
- Country summary: `data/country_summary.csv`
- Growth trends: `data/growth_trends.csv`

## 🤝 Contributing

### Adding Features
1. **Fork the project**
2. **Create a feature branch**
3. **Add your enhancement**
4. **Test thoroughly**
5. **Submit a pull request**

### Reporting Issues
1. **Check existing issues** first
2. **Provide detailed description**
3. **Include sample data** if relevant
4. **Specify environment details**

## 📞 Support

### Getting Help
- **Documentation**: Check this README first
- **Sample Data**: Use the included sample dataset for testing
- **Configuration**: Modify `config.py` for customizations
- **Troubleshooting**: Check the console output for errors

### Common Issues
- **Import errors**: Run `pip install -r requirements.txt`
- **Port conflicts**: Change port in `config.py`
- **Data format**: Ensure CSV has required columns
- **Memory issues**: Reduce dataset size or increase system memory

## 📄 License

This project is open source and available under the MIT License.

## 🎉 Acknowledgments

- **Plotly**: For excellent visualization capabilities
- **Streamlit**: For the intuitive dashboard framework
- **Pandas**: For powerful data processing
- **The open-source community**: For continuous inspiration

---

**Ready to explore your sales data? Start with the quick launch options above! 🚀**
