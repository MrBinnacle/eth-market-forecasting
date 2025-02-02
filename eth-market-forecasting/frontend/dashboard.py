import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import logging
from backend.ai_model.predict import predict_eth_price

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1("📈 Ethereum Market Forecasting Dashboard", style={'textAlign': 'center'}),

    dcc.Graph(id='eth-prediction-graph'),

    dcc.Interval(
        id='interval-update',
        interval=60000,  # Refresh every 60 seconds
        n_intervals=0
    ),

    html.Div(id='prediction-output', style={'textAlign': 'center', 'fontSize': 24, 'marginTop': 20})
])


### 📌 Callback to Update the Graph in Real Time
@app.callback(
    Output('eth-prediction-graph', 'figure'),
    Output('prediction-output', 'children'),
    [Input('interval-update', 'n_intervals')]
)
def update_graph(n):
    """
    Updates the dashboard with real-time ETH price predictions.
    """
    logging.info("🔄 Fetching latest ETH price prediction...")
    
    # Predict ETH Price using live data
    predicted_price = predict_eth_price()

    if predicted_price is None:
        logging.error("❌ Failed to generate prediction.")
        return {
            'data': [],
            'layout': go.Layout(title="Error: No prediction available")
        }, "❌ Prediction Unavailable"

    # Create a simple bar graph to display predicted ETH price
    figure = {
        'data': [
            go.Bar(
                x=['Now'],
                y=[predicted_price],
                marker=dict(color='blue'),
                name='Predicted ETH Price'
            )
        ],
        'layout': go.Layout(
            title='📊 Real-Time ETH Price Forecast',
            xaxis={'title': 'Time'},
            yaxis={'title': 'Predicted ETH Price (USD)'},
            template="plotly_dark"
        )
    }

    return figure, f"📊 Predicted ETH Price: ${predicted_price:.2f}"


if __name__ == '__main__':
    app.run_server(debug=True)
