import dash
from dash import dcc, html, Input, Output, callback, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from data_processor import SalesDataProcessor, create_sample_data
from visualizations import SalesVisualizer
import os

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Global Sales Performance Dashboard"

# Initialize data processor and visualizer
processor = SalesDataProcessor()
visualizer = SalesVisualizer()

# Load sample data
sample_data_path = os.path.join("..", "data", "sample_sales_data.csv")
if not os.path.exists(sample_data_path):
    sample_data = create_sample_data()
    os.makedirs(os.path.dirname(sample_data_path), exist_ok=True)
    sample_data.to_csv(sample_data_path, index=False)

# Process data
data_dict = processor.process_full_pipeline(sample_data_path)

# App layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("🌍 Global Sales Performance Dashboard", 
                   className="text-center mb-4",
                   style={"color": "#1f77b4", "font-weight": "bold"})
        ])
    ]),
    
    html.Hr(),
    
    # Controls Row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("📊 Dashboard Controls", className="mb-0")),
                dbc.CardBody([
                    # Region filter
                    html.Label("Select Regions:", className="form-label"),
                    dcc.Dropdown(
                        id='region-dropdown',
                        options=[{'label': region, 'value': region} 
                                for region in sorted(data_dict['cleaned_data']['Region'].unique())],
                        value=sorted(data_dict['cleaned_data']['Region'].unique()),
                        multi=True,
                        className="mb-3"
                    ),
                    
                    # Year filter
                    html.Label("Select Years:", className="form-label"),
                    dcc.Dropdown(
                        id='year-dropdown',
                        options=[{'label': str(year), 'value': year} 
                                for year in sorted(data_dict['cleaned_data']['Year'].unique())],
                        value=sorted(data_dict['cleaned_data']['Year'].unique()),
                        multi=True,
                        className="mb-3"
                    ),
                    
                    # Product filter
                    html.Label("Select Product Categories:", className="form-label"),
                    dcc.Dropdown(
                        id='product-dropdown',
                        options=[{'label': product, 'value': product} 
                                for product in sorted(data_dict['cleaned_data']['Product_Category'].unique())],
                        value=sorted(data_dict['cleaned_data']['Product_Category'].unique()),
                        multi=True
                    )
                ])
            ])
        ], width=12)
    ], className="mb-4"),
    
    # KPI Cards Row
    dbc.Row(id='kpi-cards', className="mb-4"),
    
    # Charts Row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("🗺️ Global Sales Map", className="mb-0")),
                dbc.CardBody([
                    dcc.Graph(id='world-map')
                ])
            ])
        ], width=8),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("📊 Sales by Region", className="mb-0")),
                dbc.CardBody([
                    dcc.Graph(id='region-pie-chart')
                ])
            ])
        ], width=4)
    ], className="mb-4"),
    
    # Additional Charts Row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("📈 Sales Trends", className="mb-0")),
                dbc.CardBody([
                    dcc.Graph(id='trend-chart')
                ])
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("🏆 Top Countries", className="mb-0")),
                dbc.CardBody([
                    dcc.Graph(id='top-countries-chart')
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    # Data Table Row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("📋 Regional Summary", className="mb-0")),
                dbc.CardBody([
                    dash_table.DataTable(
                        id='summary-table',
                        style_cell={'textAlign': 'left'},
                        style_header={'backgroundColor': '#1f77b4', 'color': 'white', 'fontWeight': 'bold'},
                        style_data={'backgroundColor': '#f8f9fa'},
                        page_size=10
                    )
                ])
            ])
        ])
    ], className="mb-4"),
    
    # Footer
    html.Hr(),
    html.P("🌍 Global Sales Performance Dashboard | Built with Dash & Plotly", 
           className="text-center text-muted")
], fluid=True)

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

@app.callback(
    [Output('kpi-cards', 'children'),
     Output('world-map', 'figure'),
     Output('region-pie-chart', 'figure'),
     Output('trend-chart', 'figure'),
     Output('top-countries-chart', 'figure'),
     Output('summary-table', 'data'),
     Output('summary-table', 'columns')],
    [Input('region-dropdown', 'value'),
     Input('year-dropdown', 'value'),
     Input('product-dropdown', 'value')]
)
def update_dashboard(selected_regions, selected_years, selected_products):
    # Filter data
    filtered_data = data_dict['cleaned_data'][
        (data_dict['cleaned_data']['Region'].isin(selected_regions)) &
        (data_dict['cleaned_data']['Year'].isin(selected_years)) &
        (data_dict['cleaned_data']['Product_Category'].isin(selected_products))
    ]
    
    if filtered_data.empty:
        # Return empty components
        empty_fig = go.Figure()
        empty_fig.add_annotation(text="No data matches the selected filters", 
                               xref="paper", yref="paper", x=0.5, y=0.5)
        return [], empty_fig, empty_fig, empty_fig, empty_fig, [], []
    
    # Recalculate aggregations
    filtered_continent_data = processor.aggregate_by_continent(filtered_data)
    filtered_country_data = processor.aggregate_by_country(filtered_data)
    filtered_growth_data = processor.calculate_growth_trends(filtered_data)
    
    # Calculate KPIs
    filtered_data_dict = {
        'cleaned_data': filtered_data,
        'continent_data': filtered_continent_data,
        'country_data': filtered_country_data,
        'growth_trends': filtered_growth_data
    }
    kpis = visualizer.create_kpi_cards(filtered_data_dict)
    
    # Create KPI cards
    kpi_cards = dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(format_number(kpis.get('total_sales', 0)), className="card-title"),
                    html.P("Total Sales", className="card-text"),
                    html.Small(f"{kpis.get('growth_rate', 0):.1f}% YoY Growth", 
                             className="text-success" if kpis.get('growth_rate', 0) > 0 else "text-danger")
                ])
            ], color="primary", outline=True)
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(format_number(kpis.get('total_profit', 0)), className="card-title"),
                    html.P("Total Profit", className="card-text"),
                    html.Small(f"{kpis.get('profit_margin', 0):.1f}% Margin", className="text-info")
                ])
            ], color="success", outline=True)
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{kpis.get('total_countries', 0):,}", className="card-title"),
                    html.P("Countries", className="card-text")
                ])
            ], color="info", outline=True)
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(f"{kpis.get('total_regions', 0):,}", className="card-title"),
                    html.P("Regions", className="card-text")
                ])
            ], color="warning", outline=True)
        ], width=3)
    ])
    
    # Create charts
    world_map = visualizer.create_world_map(filtered_country_data)
    pie_chart = visualizer.create_sales_distribution_pie(filtered_continent_data)
    trend_chart = visualizer.create_growth_trend_chart(filtered_growth_data)
    top_countries_chart = visualizer.create_top_performers_chart(
        filtered_country_data.head(10), "Top 10 Countries", "Country", "Total_Sales"
    )
    
    # Prepare table data
    table_data = filtered_continent_data.to_dict('records')
    table_columns = [{"name": col.replace('_', ' ').title(), "id": col} 
                     for col in filtered_continent_data.columns]
    
    return (kpi_cards, world_map, pie_chart, trend_chart, 
            top_countries_chart, table_data, table_columns)

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
