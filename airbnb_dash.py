import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Sample data loading (assuming you have the dataframe 'df')
df = pd.read_csv("cleaned_airbnb.csv")

# BANs data
min_price = 10
avg_price = 152.7
max_price = 10000

# Create the graphs as before but without titles
avg_price_by_neighbourhood = df.groupby('neighbourhood')['price'].mean().reset_index().sort_values(by='price', ascending=True).head(15)
fig_avg_price = px.bar(avg_price_by_neighbourhood, y='neighbourhood', x='price', color='price', color_continuous_scale=px.colors.sequential.RdBu_r, labels={'price': 'Average Price', 'neighbourhood': 'Neighbourhood'})
fig_avg_price.update_layout(xaxis_title='Average Price', yaxis_title='Neighbourhood', xaxis=dict(range=[40, avg_price_by_neighbourhood['price'].max()]))

room_type_distribution_group = df.groupby(["neighbourhood_group", "room_type"]).size().reset_index(name="count").sort_values(by="count", ascending=False)
fig_room_type_distribution = px.bar(room_type_distribution_group, x="neighbourhood_group", y="count", color="room_type", labels={"neighbourhood_group": "Neighbourhood Group", "count": "Count"})

room_type_counts = df["room_type"].value_counts().reset_index()
room_type_counts.columns = ["room_type", "count"]
fig_room_type_pie = px.pie(room_type_counts, values="count", names="room_type", hole=0.4)

price_bins = [0, 50, 100, 150, 200, 250, 300]
df["price_range"] = pd.cut(df["price"], bins=price_bins, labels=["0-50", "51-100", "101-150", "151-200", "201-250", "251-300"])
price_range_counts = df.groupby(["room_type", "price_range"]).size().reset_index(name="count")
fig_price_range = px.bar(price_range_counts, x="price_range", y="count", color="room_type", labels={"price_range": "Price Range ($)", "count": "Number of Listings"}, barmode="group")

neighbourhood_group_density = df.groupby(["neighbourhood_group", "latitude", "longitude"]).size().reset_index(name="count")
fig_mapbox = px.scatter_mapbox(neighbourhood_group_density, lat="latitude", lon="longitude", color="neighbourhood_group", size="count", size_max=15, zoom=10, mapbox_style="carto-positron")

# Update the layout of graphs
fig_avg_price.update_layout(height=600)
fig_room_type_pie.update_layout(height=300)
fig_mapbox.update_layout(height=300)

# Initialize the Dash app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
# Define the layout of the dashboard
app.layout = dbc.Container(
    [
        dbc.Row([dbc.Col(html.H1("Airbnb Listings Dashboard", className="text-center mb-4", style={'fontSize': '75px', 'fontWeight': 'bold'}), width=12)]),
        dbc.Row([
            dbc.Col(dbc.Card([dbc.CardBody([html.H4("Min Price", className="card-title"), html.H2(f"${min_price}", className="card-text")])]), className="text-center mb-4", width=4),
            dbc.Col(dbc.Card([dbc.CardBody([html.H4("Avg Price", className="card-title"), html.H2(f"${avg_price:.2f}", className="card-text")])]), className="text-center mb-4", width=4),
            dbc.Col(dbc.Card([dbc.CardBody([html.H4("Max Price", className="card-title"), html.H2(f"${max_price}", className="card-text")])]), className="text-center mb-4", width=4),
        ]),
        html.Hr(style={"visibility": "hidden"}),

        # First row: Graphs with titles below
        dbc.Row([
            dbc.Col([dcc.Graph(id="avg-price-bar", figure=fig_avg_price, style={'height': '800px'}), html.H5("Average Price per Night by Neighbourhood", className="text-center")], width=4),
            dbc.Col([dcc.Graph(id="mapbox-chart", figure=fig_mapbox, style={'height': '800px'}), html.H5("Neighbourhood Group Listing Density", className="text-center")], width=4),
            dbc.Col([dcc.Graph(id="room-type-pie", figure=fig_room_type_pie, style={'height': '800px'}), html.H5("Listings Count by Room Type", className="text-center")], width=4),
        ], className="mb-4"),
        html.Hr(style={"visibility": "hidden"}),

        # Second row: Graphs with titles below
        dbc.Row([
            dbc.Col([dcc.Graph(id="room-type-bar", figure=fig_room_type_distribution, style={'height': '600px'}), html.H5("Room Type Distribution Across Neighbourhood Groups", className="text-center")], width=6),
            dbc.Col([dcc.Graph(id="price-range-bar", figure=fig_price_range, style={'height': '600px'}), html.H5("Most Common Price Ranges for Different Room Types", className="text-center")], width=6),
        ]),
        html.Hr(style={"visibility": "hidden"}),
    ],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)
