# Percentage of Renewables Energy Generation Day-Ahead Forecasting Service 
## Descrioption
Forecasting generation of renewables for the Day-Ahead for Germany.
Author: Amirhossein Shaafieyoun [Email Address](amirhoseinshafieyoun@gmail.com)

## Requirements:
Install requirements using the following command
```bash
pip install -r requirements.txt
```


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

## Google Colab:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1r8YfXX_WGrFXnIG-pOuqVZ0Ch4o4X6n2)

Hyphens

## Day-Ahead Forecasts: 
https://drive.google.com/drive/folders/1cCKBiaA3cE1-ojXtQ35jiX-C2t2GB3NO
