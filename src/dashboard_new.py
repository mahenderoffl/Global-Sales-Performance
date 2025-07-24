import streamlit as st
import pandas as pd
import io
import os
from data_processor import SalesDataProcessor, create_sample_data
from visualizations import SalesVisualizer

def detect_device_type():
    """Detect device type based on screen width (simulated)."""
    # In a real app, you could use JavaScript to get actual screen width
    # For now, we'll use a simple heuristic or session state
    if 'device_type' not in st.session_state:
        st.session_state.device_type = 'desktop'  # Default
    return st.session_state.device_type

def toggle_mobile_view():
    """Toggle between mobile and desktop view."""
    if st.session_state.device_type == 'mobile':
        st.session_state.device_type = 'desktop'
    else:
        st.session_state.device_type = 'mobile'

# Page configuration
st.set_page_config(
    page_title="Global Sales Performance Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="auto"
)

# Responsive CSS for all devices
st.markdown("""
<style>
    /* Main container responsive styling */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }
    
    /* Header responsive */
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
        font-size: clamp(1.5rem, 4vw, 2.5rem);
        padding: 0.5rem;
    }
    
    /* Metric cards responsive */
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        text-align: center;
        min-height: 100px;
    }
    
    /* Responsive metrics */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 0.5rem;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    [data-testid="metric-container"] label {
        color: white !important;
        font-weight: 600;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: white !important;
        font-size: clamp(1.2rem, 3vw, 2rem);
        font-weight: bold;
    }
    
    /* Tabs responsive */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        flex-wrap: wrap;
        justify-content: center;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: auto;
        min-height: 50px;
        padding: 8px 16px;
        font-size: clamp(0.8rem, 2vw, 1rem);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    /* Sidebar responsive */
    .css-1d391kg {
        padding-top: 1rem;
    }
    
    /* Charts responsive */
    .js-plotly-plot, .plotly {
        width: 100% !important;
        height: auto !important;
    }
    
    /* Mobile optimizations */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }
        
        .main-header {
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 6px 12px;
            font-size: 0.8rem;
        }
        
        [data-testid="metric-container"] {
            min-height: 100px;
            padding: 0.5rem;
            margin: 0.25rem;
        }
        
        [data-testid="metric-container"] [data-testid="metric-value"] {
            font-size: 1.2rem;
        }
        
        /* Stack columns on mobile */
        .element-container .stColumn {
            width: 100% !important;
            flex: 1 1 100% !important;
        }
    }
    
    /* Tablet optimizations */
    @media (min-width: 769px) and (max-width: 1024px) {
        .main-header {
            font-size: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 8px 14px;
            font-size: 0.9rem;
        }
        
        [data-testid="metric-container"] {
            min-height: 110px;
            padding: 0.75rem;
        }
    }
    
    /* Desktop optimizations */
    @media (min-width: 1025px) {
        .main-header {
            font-size: 2.5rem;
        }
        
        [data-testid="metric-container"] {
            min-height: 120px;
            padding: 1rem;
        }
    }
    
    /* Data table responsive */
    .dataframe {
        font-size: clamp(0.7rem, 1.5vw, 0.9rem);
    }
    
    /* Expander responsive */
    .streamlit-expanderHeader {
        font-size: clamp(0.9rem, 2vw, 1.1rem);
    }
    
    /* Text area responsive */
    .stTextArea textarea {
        font-size: clamp(0.8rem, 1.5vw, 0.9rem);
    }
    
    /* Button responsive */
    .stButton button {
        width: 100%;
        font-size: clamp(0.8rem, 1.5vw, 0.9rem);
        padding: 0.5rem 1rem;
    }
    
    /* Selectbox responsive */
    .stSelectbox {
        font-size: clamp(0.8rem, 1.5vw, 0.9rem);
    }
    
    /* Hide Streamlit menu and footer on mobile */
    @media (max-width: 768px) {
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    }
    
    /* Developer credit footer */
    .developer-credit {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: linear-gradient(45deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
        padding: 8px 0;
        text-align: center;
        z-index: 1000;
        border-top: 2px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
    }
    
    .developer-credit p {
        margin: 0;
        color: #333;
        font-weight: 600;
        font-size: 14px;
    }
    
    .developer-credit a {
        color: #e91e63;
        text-decoration: none;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .developer-credit a:hover {
        color: #ad1457;
        text-shadow: 0 0 5px rgba(233, 30, 99, 0.5);
    }
    
    /* Adjust main content to avoid footer overlap */
    .main .block-container {
        padding-bottom: 50px;
    }
</style>
""", unsafe_allow_html=True)

def load_data():
    """Load or create sample data."""
    processor = SalesDataProcessor()
    visualizer = SalesVisualizer()
    
    # Check if sample data exists, if not create it
    sample_data_path = os.path.join("data", "sample_sales_data.csv")
    if not os.path.exists(sample_data_path):
        sample_data = create_sample_data()
        os.makedirs("data", exist_ok=True)
        sample_data.to_csv(sample_data_path, index=False)
    
    return processor, visualizer, sample_data_path

def format_number(num):
    """Format numbers for display."""
    if num >= 1e9:
        return f"${num/1e9:.2f}B"
    elif num >= 1e6:
        return f"${num/1e6:.2f}M"
    elif num >= 1e3:
        return f"${num/1e3:.0f}K"
    else:
        return f"${num:.0f}"

def main():
    """Main dashboard function."""
    
    # Device type detection and toggle
    device_type = detect_device_type()
    
    # Header with device toggle
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown('<h1 class="main-header">🌍 Global Sales Performance Dashboard</h1>', unsafe_allow_html=True)
    with col2:
        if st.button("📱" if device_type == "desktop" else "💻", help="Toggle mobile/desktop view"):
            toggle_mobile_view()
            st.rerun()
    
    st.markdown("---")
    
    # Initialize components
    processor, visualizer, sample_data_path = load_data()
    
    # Sidebar for controls (collapsible on mobile)
    if device_type == "mobile":
        with st.expander("📊 Dashboard Controls", expanded=False):
            data_source, uploaded_file, csv_text = sidebar_content()
    else:
        st.sidebar.header("📊 Dashboard Controls")
        data_source, uploaded_file, csv_text = sidebar_content()
    
    # Continue with the rest of the main function logic
    display_dashboard_content(processor, visualizer, sample_data_path, data_source, uploaded_file, csv_text, device_type)

def sidebar_content():
    """Sidebar content that can be used in both sidebar and expander."""
    # Data source selection
    st.subheader("📂 Data Source Options")
    
    # Data source radio buttons
    data_source = st.radio(
        "Choose your data source:",
        ["Use Sample Data", "Upload File", "Paste CSV Data"],
        index=0
    )
    
    # File upload option
    uploaded_file = None
    csv_text = None
    
    if data_source == "Upload File":
        uploaded_file = st.file_uploader(
            "Upload your sales data (CSV/Excel)",
            type=['csv', 'xlsx', 'xls'],
            help="Upload a file with columns: Country, Region, Sales, and optionally Profit, Year, Product_Category"
        )
    
    elif data_source == "Paste CSV Data":
        st.markdown("**📋 Paste CSV Data:**")
        
        # Add help section for CSV format
        with st.expander("💡 CSV Format Help & Auto-Transform"):
            st.markdown("""
            **🔄 Auto-Transform Features:**
            - **Column Mapping**: Automatically detects columns like 'revenue' → 'Sales', 'nation' → 'Country'
            - **Currency Conversion**: Removes $, €, £ symbols and converts K/M/B notation
            - **Region Generation**: Auto-generates regions from country names
            - **Data Validation**: Fills missing required fields intelligently
            
            **📝 Supported Formats:**
            ```
            Country,Sales,Region
            USA,50000,North America
            UK,30000,Europe
            ```
            
            **Or paste ANY raw data - the system will auto-transform it!**
            ```
            nation,revenue,continent
            United States,$75K,NA
            Britain,€45M,EU
            ```
            """)
        
        csv_text = st.text_area(
            "Paste your CSV data here:",
            height=200,
            placeholder="Country,Sales,Region\nUSA,50000,North America\nUK,30000,Europe\n...",
            help="Paste CSV data or any raw format - the system will auto-transform it to the required format"
        )
    
    return data_source, uploaded_file, csv_text

def display_dashboard_content(processor, visualizer, sample_data_path, data_source, uploaded_file, csv_text, device_type):
    """Display the main dashboard content with data processing and visualizations."""
    
    # Data processing
    if data_source == "Upload File" and uploaded_file is not None:
        # Process uploaded file
        temp_file = f"temp_{uploaded_file.name}"
        with open(temp_file, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        try:
            data_dict = processor.process_full_pipeline(temp_file)
            st.success("✅ Data uploaded and processed successfully!")
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            data_dict = processor.process_full_pipeline(sample_data_path)
        finally:
            # Clean up temp file
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    elif data_source == "Paste CSV Data" and csv_text:
        # Process pasted CSV data with auto-transformation
        try:
            # Create DataFrame from pasted CSV text
            csv_data = pd.read_csv(io.StringIO(csv_text))
            
            # Show original data preview
            st.info(f"📋 {len(csv_data)} rows loaded with columns: {', '.join(csv_data.columns)}")
            
            # Auto-transform the data to required format
            transformed_data = processor.auto_transform_data(csv_data)
            
            # Clean and process the transformed data
            cleaned_data = processor.clean_data(transformed_data)
            
            # Create aggregations
            continent_data = processor.aggregate_by_continent(cleaned_data)
            country_data = processor.aggregate_by_country(cleaned_data)
            growth_trends = processor.calculate_growth_trends(cleaned_data)
            
            # Get top performers
            top_countries = processor.get_top_performers(country_data, 'Total_Sales', 15)
            top_regions = processor.get_top_performers(continent_data, 'Total_Sales', 10)
            
            data_dict = {
                'raw_data': csv_data,
                'transformed_data': transformed_data,
                'cleaned_data': cleaned_data,
                'continent_data': continent_data,
                'country_data': country_data,
                'growth_trends': growth_trends,
                'top_countries': top_countries,
                'top_regions': top_regions
            }
            
            st.success(f"✅ CSV data auto-transformed and processed! {len(cleaned_data)} records ready for analysis.")
                
        except Exception as e:
            st.error(f"❌ Error processing CSV data: {str(e)}")
            st.info("💡 The system will auto-transform column names and data formats. Any raw data format should work!")
            data_dict = processor.process_full_pipeline(sample_data_path)
    
    else:
        # Use sample data
        data_dict = processor.process_full_pipeline(sample_data_path)
        if data_source == "Use Sample Data":
            st.info("📋 Using sample data. Upload your own file or paste CSV data to analyze real data.")
    
    # Apply filters and display dashboard
    filtered_data_dict = apply_filters(data_dict, device_type)
    display_visualizations(visualizer, filtered_data_dict, data_dict, data_source, device_type)

def apply_filters(data_dict, device_type):
    """Apply filters based on user selections."""
    
    if device_type == "mobile":
        with st.expander("🔍 Filters", expanded=False):
            filter_content = create_filter_content(data_dict)
    else:
        st.sidebar.subheader("🔍 Filters")
        filter_content = create_filter_content(data_dict, use_sidebar=True)
    
    selected_regions, selected_years, selected_products = filter_content
    
    # Apply filters to data
    filtered_data = data_dict['cleaned_data'].copy()
    
    if selected_regions:
        filtered_data = filtered_data[filtered_data['Region'].isin(selected_regions)]
    
    if selected_years and 'Year' in filtered_data.columns:
        filtered_data = filtered_data[filtered_data['Year'].isin(selected_years)]
        
    if selected_products and 'Product_Category' in filtered_data.columns:
        filtered_data = filtered_data[filtered_data['Product_Category'].isin(selected_products)]
    
    # Recalculate aggregations with filtered data
    processor = SalesDataProcessor()
    filtered_continent_data = processor.aggregate_by_continent(filtered_data)
    filtered_country_data = processor.aggregate_by_country(filtered_data)
    filtered_growth_data = processor.calculate_growth_trends(filtered_data)
    
    return {
        'cleaned_data': filtered_data,
        'continent_data': filtered_continent_data,
        'country_data': filtered_country_data,
        'growth_trends': filtered_growth_data
    }

def create_filter_content(data_dict, use_sidebar=False):
    """Create filter controls."""
    widget_func = st.sidebar if use_sidebar else st
    
    # Region filter
    available_regions = sorted(data_dict['cleaned_data']['Region'].unique())
    selected_regions = widget_func.multiselect(
        "Select Regions",
        available_regions,
        default=available_regions,
        key="filter_content_regions"
    )
    
    # Year filter (if available)
    selected_years = []
    if 'Year' in data_dict['cleaned_data'].columns:
        available_years = sorted(data_dict['cleaned_data']['Year'].unique())
        selected_years = widget_func.multiselect(
            "Select Years",
            available_years,
            default=available_years,
            key="filter_content_years"
        )
    
    # Product filter (if available)
    selected_products = []
    if 'Product_Category' in data_dict['cleaned_data'].columns:
        available_products = sorted(data_dict['cleaned_data']['Product_Category'].unique())
        selected_products = widget_func.multiselect(
            "Select Product Categories",
            available_products,
            default=available_products,
            key="filter_content_products"
        )
    
    return selected_regions, selected_years, selected_products

def display_visualizations(visualizer, filtered_data_dict, data_dict, data_source, device_type):
    """Display all visualizations with responsive design."""
    
    # Show data statistics
    total_records = len(filtered_data_dict['cleaned_data'])
    if total_records == 0:
        st.warning("⚠️ No data matches the selected filters. Please adjust your filter selections.")
        return
    
    # KPI Cards
    kpis = visualizer.create_kpi_cards(filtered_data_dict)
    
    # KPI Cards with responsive layout
    st.subheader("📈 Key Performance Indicators")
    
    if device_type == "mobile":
        # Mobile layout - single column
        st.metric("Total Sales", format_number(kpis.get('total_sales', 0)), f"{kpis.get('growth_rate', 0):.1f}% YoY")
        st.metric("Total Profit", format_number(kpis.get('total_profit', 0)), f"{kpis.get('profit_margin', 0):.1f}% margin")
        st.metric("Countries", f"{kpis.get('total_countries', 0):,}")
        st.metric("Regions", f"{kpis.get('total_regions', 0):,}")
    else:
        # Desktop/Tablet layout - adaptive columns
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        with col1:
            st.metric("Total Sales", format_number(kpis.get('total_sales', 0)), f"{kpis.get('growth_rate', 0):.1f}% YoY")
        with col2:
            st.metric("Total Profit", format_number(kpis.get('total_profit', 0)), f"{kpis.get('profit_margin', 0):.1f}% margin")
        with col3:
            st.metric("Countries", f"{kpis.get('total_countries', 0):,}")
        with col4:
            st.metric("Regions", f"{kpis.get('total_regions', 0):,}")
    
    st.markdown("---")
    
    # Show data transformation info if available
    if data_source == "Paste CSV Data" and 'transformed_data' in data_dict:
        with st.expander("🔄 Data Transformation Summary", expanded=False):
            if device_type == "mobile":
                # Mobile layout - single column
                st.markdown("**Original Data Preview:**")
                st.write(data_dict['raw_data'].head(3))
                st.markdown("**Transformed Data Preview:**")
                st.write(data_dict['transformed_data'].head(3))
            else:
                # Desktop layout - two columns
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Original Data Preview:**")
                    st.write(data_dict['raw_data'].head(3))
                
                with col2:
                    st.markdown("**Transformed Data Preview:**")
                    st.write(data_dict['transformed_data'].head(3))
            
            st.info("🔄 Data was automatically transformed to match dashboard requirements!")
    
    # Visualizations with responsive tabs
    if device_type == "mobile":
        tab_labels = ["🗺️ Map", "📊 Regions", "📈 Trends", "🏆 Top"]
    else:
        tab_labels = ["🗺️ World Map", "📊 Regional Analysis", "📈 Growth Trends", "🏆 Top Performers"]
    
    tab1, tab2, tab3, tab4 = st.tabs(tab_labels)
    
    with tab1:
        st.subheader("🗺️ Global Sales Distribution")
        if len(filtered_data_dict['country_data']) > 0:
            world_map = visualizer.create_world_map(filtered_data_dict['country_data'], device_type=device_type)
            st.plotly_chart(world_map, use_container_width=True, key="world_map_main")
        else:
            st.info("No country data available for the selected filters.")
    
    with tab2:
        st.subheader("📊 Regional Performance Analysis")
        
        if len(filtered_data_dict['continent_data']) > 0:
            if device_type == "mobile":
                # Mobile: Stack charts vertically
                bar_chart = visualizer.create_continent_bar_chart(filtered_data_dict['continent_data'], device_type=device_type)
                st.plotly_chart(bar_chart, use_container_width=True, key="regional_bar_mobile")
                
                pie_chart = visualizer.create_sales_distribution_pie(filtered_data_dict['continent_data'], device_type=device_type)
                st.plotly_chart(pie_chart, use_container_width=True, key="regional_pie_mobile")
            else:
                # Desktop: Side by side
                col1, col2 = st.columns(2)
                with col1:
                    bar_chart = visualizer.create_continent_bar_chart(filtered_data_dict['continent_data'], device_type=device_type)
                    st.plotly_chart(bar_chart, use_container_width=True, key="regional_bar_desktop")
                
                with col2:
                    pie_chart = visualizer.create_sales_distribution_pie(filtered_data_dict['continent_data'], device_type=device_type)
                    st.plotly_chart(pie_chart, use_container_width=True, key="regional_pie_desktop")
        else:
            st.info("No regional data available for the selected filters.")
    
    with tab3:
        st.subheader("📈 Growth Trends & Performance")
        
        if len(filtered_data_dict['growth_trends']) > 0 and 'Year' in filtered_data_dict['cleaned_data'].columns:
            growth_chart = visualizer.create_growth_trend_chart(filtered_data_dict['growth_trends'], device_type=device_type)
            st.plotly_chart(growth_chart, use_container_width=True, key="growth_trends_main")
            
            # Additional performance metrics
            if device_type != "mobile":
                st.subheader("📊 Yearly Performance Summary")
                yearly_summary = filtered_data_dict['cleaned_data'].groupby('Year').agg({
                    'Sales': ['sum', 'mean', 'count'],
                    'Profit': ['sum', 'mean'] if 'Profit' in filtered_data_dict['cleaned_data'].columns else ['sum']
                }).round(2)
                st.dataframe(yearly_summary, use_container_width=True)
        else:
            st.info("Growth trends require yearly data. Upload data with 'Year' column to see trends.")
    
    with tab4:
        st.subheader("🏆 Top Performers")
        
        if device_type == "mobile":
            # Mobile: Stack charts vertically
            if len(filtered_data_dict['country_data']) > 0:
                top_countries_chart = visualizer.create_top_performers_chart(
                    filtered_data_dict['country_data'].head(10), 
                    title="Top 10 Countries by Sales",
                    metric='Total_Sales',
                    device_type=device_type
                )
                st.plotly_chart(top_countries_chart, use_container_width=True, key="top_countries_mobile")
                
                profit_scatter = visualizer.create_profit_vs_sales_scatter(filtered_data_dict['country_data'], device_type=device_type)
                st.plotly_chart(profit_scatter, use_container_width=True, key="profit_scatter_mobile")
        else:
            # Desktop: Side by side
            col1, col2 = st.columns(2)
            
            with col1:
                if len(filtered_data_dict['country_data']) > 0:
                    st.markdown("**🥇 Top 10 Countries by Sales**")
                    top_countries_chart = visualizer.create_top_performers_chart(
                        filtered_data_dict['country_data'].head(10), 
                        title="Top 10 Countries by Sales",
                        metric='Total_Sales',
                        device_type=device_type
                    )
                    st.plotly_chart(top_countries_chart, use_container_width=True, key="top_countries_desktop")
            
            with col2:
                if len(filtered_data_dict['country_data']) > 0:
                    st.markdown("**💰 Sales vs Profit Analysis**")
                    profit_scatter = visualizer.create_profit_vs_sales_scatter(filtered_data_dict['country_data'], device_type=device_type)
                    st.plotly_chart(profit_scatter, use_container_width=True, key="profit_scatter_desktop")
    
    # Data table
    with st.expander("📋 View Raw Data", expanded=False):
        st.dataframe(filtered_data_dict['cleaned_data'], use_container_width=True)

# Developer credit footer
st.markdown("""
<div class="developer-credit">
    <p>Developed By <strong>Mahender Banoth (IIT Patna)</strong> | 
    <a href="https://instagram.com/mahender_hustles" target="_blank">@mahender_hustles</a></p>
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
