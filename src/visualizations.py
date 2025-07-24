import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Dict

class SalesVisualizer:
    """
    A class to create various visualizations for the sales dashboard.
    """
    
    def __init__(self):
        self.color_palette = px.colors.qualitative.Set3
        self.continent_colors = {
            'North America': '#1f77b4',
            'South America': '#ff7f0e', 
            'Europe': '#2ca02c',
            'Asia': '#d62728',
            'Africa': '#9467bd',
            'Oceania': '#8c564b'
        }
        
        # Responsive layout configurations
        self.mobile_config = {
            'height': 400,
            'font_size': 12,
            'title_font_size': 14,
            'margin': dict(l=20, r=20, t=60, b=20)
        }
        
        self.tablet_config = {
            'height': 500,
            'font_size': 14,
            'title_font_size': 16,
            'margin': dict(l=40, r=40, t=80, b=40)
        }
        
        self.desktop_config = {
            'height': 600,
            'font_size': 16,
            'title_font_size': 20,
            'margin': dict(l=60, r=60, t=100, b=60)
        }
    
    def get_responsive_config(self, device_type: str = 'desktop') -> dict:
        """Get responsive configuration based on device type."""
        configs = {
            'mobile': self.mobile_config,
            'tablet': self.tablet_config,
            'desktop': self.desktop_config,
            'responsive': {  # Auto-responsive config
                'height': 500,  # Medium height that works well for all devices
                'font_size': 14,
                'title_font_size': 18,
                'margin': dict(l=30, r=30, t=70, b=30)
            }
        }
        return configs.get(device_type, self.desktop_config)
    
    def create_world_map(self, country_data: pd.DataFrame, metric: str = 'Total_Sales', device_type: str = 'desktop') -> go.Figure:
        """
        Create an interactive world map showing sales by country.
        
        Args:
            country_data (pd.DataFrame): Aggregated country data
            metric (str): Metric to display on the map
            device_type (str): Device type for responsive design
            
        Returns:
            go.Figure: Plotly figure object
        """
        config = self.get_responsive_config(device_type)
        
        # Country code mapping for better map visualization
        country_codes = {
            'United States': 'USA', 'United Kingdom': 'GBR', 'Germany': 'DEU',
            'France': 'FRA', 'Italy': 'ITA', 'Spain': 'ESP', 'Canada': 'CAN',
            'Brazil': 'BRA', 'Argentina': 'ARG', 'Chile': 'CHL', 'Mexico': 'MEX',
            'China': 'CHN', 'Japan': 'JPN', 'India': 'IND', 'South Korea': 'KOR',
            'Australia': 'AUS', 'New Zealand': 'NZL', 'South Africa': 'ZAF',
            'Nigeria': 'NGA', 'Egypt': 'EGY'
        }
        
        # Add country codes to data
        map_data = country_data.copy()
        map_data['iso_alpha'] = map_data['Country'].map(country_codes)
        
        # Create choropleth map
        fig = px.choropleth(
            map_data,
            locations='iso_alpha',
            color=metric,
            hover_name='Country',
            hover_data=['Region', metric],
            color_continuous_scale='Viridis',
            title=f'Global {metric.replace("_", " ")} Distribution'
        )
        
        fig.update_layout(
            title_font_size=config['title_font_size'],
            font_size=config['font_size'],
            height=config['height'],
            margin=config['margin'],
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular'
            )
        )
        
        return fig
    
    def create_continent_bar_chart(self, continent_data: pd.DataFrame, metric: str = 'Total_Sales', device_type: str = 'desktop') -> go.Figure:
        """
        Create a bar chart showing sales by continent.
        
        Args:
            continent_data (pd.DataFrame): Aggregated continent data
            metric (str): Metric to display
            device_type (str): Device type for responsive design
            
        Returns:
            go.Figure: Plotly figure object
        """
        config = self.get_responsive_config(device_type)
        
        # Sort data for better visualization
        sorted_data = continent_data.sort_values(metric, ascending=True)
        
        fig = px.bar(
            sorted_data,
            x=metric,
            y='Region',
            orientation='h',
            color='Region',
            color_discrete_map=self.continent_colors,
            title=f'{metric.replace("_", " ")} by Continent',
            text=metric
        )
        
        fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig.update_layout(
            title_font_size=config['title_font_size'],
            font_size=config['font_size'],
            height=config['height'],
            margin=config['margin'],
            xaxis_title=metric.replace('_', ' '),
            yaxis_title='Continent',
            showlegend=False
        )
        
        return fig
    
    def create_growth_trend_chart(self, growth_data: pd.DataFrame, device_type: str = 'desktop') -> go.Figure:
        """
        Create a line chart showing growth trends over time.
        
        Args:
            growth_data (pd.DataFrame): Growth trends data
            device_type (str): Device type for responsive design
            
        Returns:
            go.Figure: Plotly figure object
        """
        config = self.get_responsive_config(device_type)
        
        if growth_data.empty:
            # Create empty figure with message
            fig = go.Figure()
            fig.add_annotation(
                text="No time series data available for growth analysis",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font_size=config['font_size']
            )
            fig.update_layout(
                title="Sales Growth Trends Over Time", 
                height=config['height'],
                font_size=config['font_size'],
                title_font_size=config['title_font_size'],
                margin=config['margin']
            )
            return fig
        
        fig = px.line(
            growth_data,
            x='Year',
            y='Sales',
            color='Region',
            color_discrete_map=self.continent_colors,
            title='Sales Trends by Region Over Time',
            markers=True
        )
        
        fig.update_layout(
            title_font_size=config['title_font_size'],
            font_size=config['font_size'],
            height=config['height'],
            margin=config['margin'],
            xaxis_title='Year',
            yaxis_title='Total Sales',
            legend_title='Region'
        )
        
        return fig
    
    def create_top_performers_chart(self, top_data: pd.DataFrame, title: str = "Top Performers", 
                                  metric: str = 'Total_Sales', device_type: str = 'desktop') -> go.Figure:
        """
        Create a bar chart for top performers.
        
        Args:
            top_data (pd.DataFrame): Top performers data
            title (str): Chart title
            metric (str): Metric to display
            device_type (str): Device type for responsive design
            
        Returns:
            go.Figure: Plotly figure object
        """
        config = self.get_responsive_config(device_type)
        
        # Sort data for better visualization
        sorted_data = top_data.sort_values(metric, ascending=True)
        
        fig = px.bar(
            sorted_data.tail(10),  # Show top 10
            x=metric,
            y='Country',
            orientation='h',
            color=metric,
            color_continuous_scale='Blues',
            title=title,
            text=metric
        )
        
        fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig.update_layout(
            title_font_size=config['title_font_size'],
            font_size=config['font_size'],
            height=config['height'],
            margin=config['margin'],
            xaxis_title=metric.replace('_', ' '),
            yaxis_title='Country',
            showlegend=False
        )
        
        return fig
    
    def create_profit_vs_sales_scatter(self, data: pd.DataFrame, device_type: str = 'desktop') -> go.Figure:
        """
        Create a scatter plot showing profit vs sales relationship.
        
        Args:
            data (pd.DataFrame): Data with sales and profit columns
            device_type (str): Device type for responsive design
            
        Returns:
            go.Figure: Plotly figure object
        """
        config = self.get_responsive_config(device_type)
        
        if 'Total_Profit' not in data.columns or 'Total_Sales' not in data.columns:
            # Create empty figure with message
            fig = go.Figure()
            fig.add_annotation(
                text="Profit data not available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font_size=config['font_size']
            )
            fig.update_layout(
                title="Sales vs Profit Analysis", 
                height=config['height'],
                font_size=config['font_size'],
                title_font_size=config['title_font_size'],
                margin=config['margin']
            )
            return fig
        
        fig = px.scatter(
            data,
            x='Total_Sales',
            y='Total_Profit',
            color='Region' if 'Region' in data.columns else None,
            size='Total_Sales',
            hover_name='Country' if 'Country' in data.columns else 'Region',
            title='Sales vs Profit Relationship',
            color_discrete_map=self.continent_colors
        )
        
        # Add trend line
        if len(data) > 1:
            fig.add_trace(
                go.Scatter(
                    x=data['Total_Sales'],
                    y=np.poly1d(np.polyfit(data['Total_Sales'], data['Total_Profit'], 1))(data['Total_Sales']),
                    mode='lines',
                    name='Trend Line',
                    line=dict(dash='dash', color='red')
                )
            )
        
        fig.update_layout(
            title_font_size=config['title_font_size'],
            font_size=config['font_size'],
            height=config['height'],
            margin=config['margin'],
            xaxis_title='Total Sales',
            yaxis_title='Total Profit'
        )
        
        return fig
    
    def create_sales_distribution_pie(self, continent_data: pd.DataFrame, metric: str = 'Total_Sales', device_type: str = 'desktop') -> go.Figure:
        """
        Create a pie chart showing sales distribution by continent.
        
        Args:
            continent_data (pd.DataFrame): Aggregated continent data
            metric (str): Metric to display
            device_type (str): Device type for responsive design
            
        Returns:
            go.Figure: Plotly figure object
        """
        config = self.get_responsive_config(device_type)
        
        fig = px.pie(
            continent_data,
            values=metric,
            names='Region',
            title=f'{metric.replace("_", " ")} Distribution by Region',
            color='Region',
            color_discrete_map=self.continent_colors
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            title_font_size=config['title_font_size'],
            font_size=config['font_size'],
            height=config['height'],
            margin=config['margin'],
            showlegend=True,
            legend=dict(
                orientation="h" if device_type == "mobile" else "v",
                yanchor="bottom" if device_type == "mobile" else "middle",
                y=-0.2 if device_type == "mobile" else 0.5,
                xanchor="center" if device_type == "mobile" else "left",
                x=0.5 if device_type == "mobile" else 1.02
            )
        )
        
        return fig
    
    def create_kpi_cards(self, data: Dict[str, pd.DataFrame]) -> Dict[str, float]:
        """
        Calculate key performance indicators for dashboard cards.
        
        Args:
            data (Dict[str, pd.DataFrame]): Processed data dictionary
            
        Returns:
            Dict[str, float]: KPI values
        """
        kpis = {}
        
        if 'cleaned_data' in data and not data['cleaned_data'].empty:
            cleaned_data = data['cleaned_data']
            
            # Total sales
            kpis['total_sales'] = cleaned_data['Sales'].sum()
            
            # Total profit
            if 'Profit' in cleaned_data.columns:
                kpis['total_profit'] = cleaned_data['Profit'].sum()
                # Protect against division by zero
                if kpis['total_sales'] > 0:
                    kpis['profit_margin'] = (kpis['total_profit'] / kpis['total_sales']) * 100
                else:
                    kpis['profit_margin'] = 0
            else:
                kpis['total_profit'] = 0
                kpis['profit_margin'] = 0
            
            # Number of countries
            kpis['total_countries'] = cleaned_data['Country'].nunique()
            
            # Number of regions
            kpis['total_regions'] = cleaned_data['Region'].nunique()
            
            # Average sales per country
            if kpis['total_countries'] > 0:
                kpis['avg_sales_per_country'] = kpis['total_sales'] / kpis['total_countries']
            else:
                kpis['avg_sales_per_country'] = 0
            
            # Growth rate (if year data available)
            if 'Year' in cleaned_data.columns:
                yearly_sales = cleaned_data.groupby('Year')['Sales'].sum()
                if len(yearly_sales) > 1 and yearly_sales.iloc[-2] > 0:
                    kpis['growth_rate'] = ((yearly_sales.iloc[-1] - yearly_sales.iloc[-2]) / yearly_sales.iloc[-2]) * 100
                else:
                    kpis['growth_rate'] = 0
            else:
                kpis['growth_rate'] = 0
        
        return kpis
    
    def create_comprehensive_dashboard(self, data: Dict[str, pd.DataFrame]) -> Dict[str, go.Figure]:
        """
        Create all visualizations for the dashboard.
        
        Args:
            data (Dict[str, pd.DataFrame]): Processed data dictionary
            
        Returns:
            Dict[str, go.Figure]: Dictionary of all figures
        """
        figures = {}
        
        # World map
        if 'country_data' in data and not data['country_data'].empty:
            figures['world_map'] = self.create_world_map(data['country_data'])
        
        # Continent bar chart
        if 'continent_data' in data and not data['continent_data'].empty:
            figures['continent_bar'] = self.create_continent_bar_chart(data['continent_data'])
            figures['continent_pie'] = self.create_sales_distribution_pie(data['continent_data'])
        
        # Growth trends
        if 'growth_trends' in data and not data['growth_trends'].empty:
            figures['growth_trends'] = self.create_growth_trend_chart(data['growth_trends'])
        
        # Top performers
        if 'top_countries' in data and not data['top_countries'].empty:
            figures['top_countries'] = self.create_top_performers_chart(
                data['top_countries'], 
                'Top 10 Countries by Sales', 
                'Country', 
                'Total_Sales'
            )
        
        if 'top_regions' in data and not data['top_regions'].empty:
            figures['top_regions'] = self.create_top_performers_chart(
                data['top_regions'], 
                'Top Regions by Sales', 
                'Region', 
                'Total_Sales'
            )
        
        # Profit vs Sales scatter
        if 'country_data' in data and not data['country_data'].empty:
            figures['profit_vs_sales'] = self.create_profit_vs_sales_scatter(data['country_data'])
        
        return figures
