import logging
from flask import Flask, render_template
import dash
from dash import dcc, html  # Updated for Dash v2+
  
# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize the Flask server
server = Flask(__name__)

# Initialize the Dash app integrated with Flask
app = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix='/dashboard/',
    suppress_callback_exceptions=True
)

# Define the Dash app layout
app.layout = html.Div(
    children=[
        html.H1("📈 Ethereum Market Forecasting Dashboard", style={'textAlign': 'center'}),
        html.Div(
            "Navigate to /dashboard/ to view the live ETH forecasting dashboard.",
            style={'textAlign': 'center'}
        ),
        dcc.Link(
            "Go to Dashboard",
            href="/dashboard/",
            style={'display': 'block', 'textAlign': 'center', 'marginTop': '20px'}
        )
    ]
)

# Define the Flask route for the homepage
@server.route("/")
def home():
    return """
    <h1>Welcome to Ethereum Market Forecasting</h1>
    <p>Navigate to <a href='/dashboard/'>Dashboard</a> to view real-time ETH predictions.</p>
    <p>View the <a href='/portfolio'>Sample Portfolio Dashboard</a> for a learning-mode example.</p>
    """

# Serve the sample portfolio dashboard
@server.route("/portfolio")
def portfolio_dashboard():
    return render_template("portfolio.html")

# Run the server
if __name__ == "__main__":
    logging.info("🚀 Starting Flask & Dash Server...")
    server.run(debug=True, host="0.0.0.0", port=8050)
