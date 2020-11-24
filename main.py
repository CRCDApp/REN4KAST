from GeneralForecastHandler import get_forecasts_for_today
import pandas as pd
from flask_ngrok import run_with_ngrok
from flask import Flask, make_response

app = Flask(__name__)

run_with_ngrok(app)  # starts ngrok when the app is run


@app.route("/")
def home():
    forecast = get_forecasts_for_today()
    df = pd.DataFrame(forecast, columns=['forecast'])
    df.index.name = "time"
    resp = make_response(df.to_csv(columns=df.columns))
    resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp
    # return jsonify(forecast.values.tolist())

def run_server():
    app.run()
