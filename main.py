from FileManager import connect_drive
from GeneralDataHandler import combine_generation_and_exogenous_data
from datetime import datetime as date_time, timedelta

connect_drive()

start = (date_time.today() - timedelta(days=35)).strftime('%Y-%m-%d')
end = (date_time.today() - timedelta(days=1)).strftime('%Y-%m-%d')
end_entsoe = (date_time.today() + timedelta(days=1)).strftime('%Y-%m-%d')
timezone = "Etc/GMT"  # Europe/Berlin OR Etc/GMT

exog_params, renewables_percentage = combine_generation_and_exogenous_data(start, end, end_entsoe, timezone)

data_frequency_per_day = 96
# sample call
# forecasts = run_and_save_S_ARIMAX_model(renewables_percentage, data_frequency_per_day, [param[:-data_frequency_per_day] for param in exog_params], [param[-data_frequency_per_day:] for param in exog_params], config=[(4, 1, 4), (2, 0, 2, 4), 'n'])
