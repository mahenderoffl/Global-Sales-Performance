# 🌍 Global Sales Performance Dashboard

A comprehensive, responsive Streamlit-based interactive dashboard for visualizing and analyzing global sales data with support for multiple real datasets, advanced data transformations, and mobile-optimized design.

![Dashboard Preview](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)

## ✨ Features

### 📊 **Multi-Dataset Support**
- **Real Dataset 1**: Global Tech Gadget Consumption Data (2015-2025)
- **Real Dataset 2**: Global Chocolate Sales Data (2022)
- **Sample Data**: Built-in demo data for testing
- **File Upload**: Support for CSV/Excel files
- **Paste CSV**: Direct data input with auto-transformation

### 🎨 **Interactive Visualizations**
- **World Map**: Interactive global sales distribution
- **Regional Analysis**: Bar charts and pie charts for continent-wise data
- **Growth Trends**: Time-series analysis with yearly performance
- **Top Performers**: Country rankings and sales vs profit analysis
- **KPI Cards**: Real-time metrics with growth indicators

### 📱 **Responsive Design**
- **Mobile-Optimized**: Touch-friendly interface for smartphones
- **Tablet Support**: Adaptive layout for medium screens
- **Desktop View**: Full-featured experience for large screens
- **Device Toggle**: Switch between mobile/desktop views

### 🔄 **Smart Data Processing**
- **Auto-Transformation**: Intelligent column mapping and data cleaning
- **Currency Conversion**: Automatic handling of $, €, £ symbols and K/M/B notation
- **Region Generation**: Auto-assignment of regions from country names
- **Data Validation**: Robust error handling and data quality checks

### 🎛️ **Advanced Filtering**
- **Multi-Region Selection**: Filter by continents and regions
- **Year-based Filtering**: Time-range selection for historical data
- **Product Categories**: Filter by product types and categories
- **Real-time Updates**: Instant visualization updates

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mahenderoffl/Global-Sales-Performance.git
   cd Global-Sales-Performance
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the dashboard**
   ```bash
   streamlit run src/dashboard.py
   ```

5. **Access the dashboard**
   - Open your browser and go to `http://localhost:8501`

### 🎯 **Quick Launch Options**

**Windows Users:**
- Double-click `run_dashboard.bat` for instant launch
- Or run `.\run_dashboard.ps1` in PowerShell

## 💻 Usage

### 🔢 **Data Sources**
1. **Use Sample Data**: Start with built-in demo data
2. **Use Real Data**: Load Global Tech Gadget Consumption dataset
3. **Use Real Dataset 2**: Load Global Chocolate Sales dataset
4. **Upload File**: Upload your own CSV/Excel files
5. **Paste CSV Data**: Direct input with auto-transformation

### 📈 **Dashboard Sections**
- **KPI Cards**: Overview of total sales, profit, countries, and regions
- **World Map**: Geographic distribution of sales data
- **Regional Analysis**: Continent-wise performance comparison
- **Growth Trends**: Yearly sales and profit trends
- **Top Performers**: Best performing countries and regions

### 🎯 **Filtering Options**
- Select specific regions for focused analysis
- Filter by years for historical trends
- Choose product categories for targeted insights

## 🛠️ Technologies Used

### **Frontend & Visualization**
- **Streamlit**: Web application framework
- **Plotly**: Interactive charts and maps
- **HTML/CSS**: Custom styling and responsive design

### **Data Processing**
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Python**: Core programming language

### **Data Sources**
- **Local CSV Files**: Real datasets stored locally
- **Excel Support**: .xlsx and .xls file formats
- **Auto-transformation**: Intelligent data cleaning

## 📁 Project Structure

```
visualization-project/
├── src/
│   ├── dashboard.py           # Main dashboard application
│   ├── data_processor.py      # Data processing and transformation
│   ├── visualizations.py      # Chart creation and styling
│   └── data/                  # Source data files
├── data/
│   ├── Global_Tech_Gadget_Consumption.csv
│   ├── Real_Dataset_2.csv
│   └── sample_sales_data.csv
├── assets/
│   └── style.css             # Additional styling
├── requirements.txt          # Python dependencies
├── run_dashboard.bat         # Windows launcher
├── run_dashboard.ps1         # PowerShell launcher
├── README.md                # Project documentation
└── .gitignore               # Git ignore rules
```

## 🎨 Key Features Explained

### **Responsive Design System**
- Automatic device detection
- Adaptive layouts for different screen sizes
- Mobile-first design approach
- Touch-optimized controls

### **Data Auto-Transformation**
- Intelligent column mapping (e.g., 'revenue' → 'Sales')
- Currency symbol removal and conversion
- Region assignment from country names
- Missing data handling

### **Performance Optimizations**
- Streamlit caching for faster data loading
- Efficient data processing pipelines
- Optimized chart rendering
- Memory-efficient operations

## 📸 Screenshots

### Desktop View
- Full-featured dashboard with side-by-side charts
- Advanced filtering options in sidebar
- Comprehensive KPI metrics

### Mobile View
- Touch-optimized interface
- Collapsible controls
- Stacked chart layouts

### Interactive Features
- Hover details on world map
- Zoom and pan functionality
- Real-time filter updates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues
- **Port already in use**: Change port with `streamlit run src/dashboard.py --server.port 8502`
- **Missing dependencies**: Run `pip install -r requirements.txt`
- **Data loading errors**: Ensure CSV files are in the correct format

### Performance Tips
- Use filtered data for large datasets
- Clear browser cache if charts don't load
- Close unused browser tabs for better performance

## 🔮 Future Enhancements

- [ ] Real-time data streaming
- [ ] Advanced analytics and forecasting
- [ ] Multi-language support
- [ ] Custom theme options
- [ ] Data export functionality
- [ ] User authentication
- [ ] Advanced filtering UI

## 👨‍💻 Developer

**Mahender Banoth (IIT Patna)**
- 📷 Instagram: [@mahender_hustles](https://instagram.com/mahender_hustles)
- 💼 Built using Streamlit • Python • Pandas • Plotly • NumPy

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- Plotly for powerful visualization capabilities
- Pandas community for data processing tools
- Open source community for inspiration and support

---

⭐ **Star this repository if you find it helpful!** ⭐

*Made with ❤️ by Mahender Banoth*
