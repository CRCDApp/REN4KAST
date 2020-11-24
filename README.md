First install the requirements using the following command:
pip install -r requirements.txt

Hyphens

# Usage:

## Flask Server:
```bash
from main import run_server
run_server()
```

# Getting forecasts
```bash
import GeneralForecastHandler
from datetime import datetime,timedelta

forecast = GeneralForecastHandler.get_forecasts_for_today()
forecast.to_csv("/content/drive/My Drive/day-ahead-forecasts/Forecast_{}_AT-{}.csv".format((datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d'),datetime.today().strftime("%Y-%m-%d %H:%M:%S")))
```

Hyphens

## Google Colab:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1kDBQs4LzLiDY4TgQ2f_j2Vn7sGQZo5gi#scrollTo=6j6oKQdiNFnK)

Hyphens

## Day-Ahead Forecasts: 
https://drive.google.com/drive/folders/1cCKBiaA3cE1-ojXtQ35jiX-C2t2GB3NO
