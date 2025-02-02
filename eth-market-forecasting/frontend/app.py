from flask import Flask, render_template
import dash
import dash_core_components as dcc
import dash_html_components as html
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize Flask app
server = Flask(__name__)

# Initialize Dash app inside Flask
app = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix='/dashboard/',
    suppress_callback_exceptions=True
)

# Dash App Layout
app.layout = html.Div([
    html.H1("📈 Ethereum Market Forecasting Dashboard", style={'textAlign': 'center'}),
    html.Div("Navigate to /dashboard/ to view the live ETH forecasting dashboard.", style={'textAlign': 'center'}),
    dcc.Link("Go to Dashboard", href="/dashboard/", style={'display': 'block', 'textAlign': 'center', 'marginTop': '20px'})
])

# Flask Route for Homepage
@server.route("/")
def home():
    return """
    <h1>Welcome to Ethereum Market Forecasting</h1>
    <p>Navigate to <a href='/dashboard/'>Dashboard</a> to view real-time ETH predictions.</p>
    """

# Run Flask Server
if __name__ == "__main__":
    logging.info("🚀 Starting Flask & Dash Server...")
    server.run(debug=True, host="0.0.0.0", port=8050)
