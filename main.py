from GeneralForecastHandler import get_forecasts_for_today
from flask_ngrok import run_with_ngrok
from flask import Flask, make_response

app = Flask(__name__)

run_with_ngrok(app)  # starts ngrok when the app is run


@app.route("/")
def home():
    forecast = get_forecasts_for_today()
    resp = make_response(forecast.to_csv(columns=forecast.columns))
    resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp
    # return jsonify(forecast.values.tolist())

def run_server():
    app.run()
