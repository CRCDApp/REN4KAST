from RenewablesEnergyService.GeneralDataHandler import combine_generation_and_exogenous_data
from datetime import datetime as date_time, timedelta
from RenewablesEnergyService.GeneralForecastHandler import run_and_save_S_ARIMAX_model,run_and_save_SARIMA_model
import pandas as pd

start = (date_time.today() - timedelta(days=35)).strftime('%Y-%m-%d')
end = (date_time.today() - timedelta(days=1)).strftime('%Y-%m-%d')
end_entsoe = (date_time.today() + timedelta(days=1)).strftime('%Y-%m-%d')
timezone = "Etc/GMT"  # Europe/Berlin OR Etc/GMT

exog_params, renewables_percentage = combine_generation_and_exogenous_data(start, end, end_entsoe, timezone)

data_frequency_per_day = 96
# sample call
renewables_percentage.index = pd.date_range(start="{} 00:00:00".format(start), periods=len(renewables_percentage), freq='15Min')
exog_params.index = pd.date_range(start="{} 00:00:00".format(start), periods=len(exog_params), freq='15Min')

forecasts = run_and_save_S_ARIMAX_model(renewables_percentage, data_frequency_per_day, exog_params[:-data_frequency_per_day], exog_params[-data_frequency_per_day:], config=[(4, 1, 4), (2, 0, 2, 4), 'n'])

forecasts = run_and_save_SARIMA_model(renewables_percentage, data_frequency_per_day, config=[(4, 1, 4), (2, 0, 2, 4), 'n'])