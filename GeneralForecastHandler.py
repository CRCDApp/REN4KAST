from datetime import datetime, timedelta
from RenewablesEnergyService.GeneralForecastHandler import run_and_save_S_ARIMAX_model, run_and_save_SARIMA_model

from statsmodels.tsa.statespace.sarimax import SARIMAX
import pandas as pd

from RenewablesEnergyService.GenerationDataController import calculate_percentage_and_combine_data
from RenewablesEnergyService.GeneralDataHandler import get_and_clean_historical_data

monthly_config = [
    [[(2, 0, 2), (2, 1, 1, 4), 'n'], "SARIMA"],  # January
    [[(2, 0, 4), (0, 0, 0, 0), 'n'], "ARIMAX"],  # February
    [[(4, 0, 3), (0, 0, 0, 0), 'n'], "ARIMAX"],  # March
    [[(4, 1, 3), (2, 0, 2, 4), 'n'], "SARIMAX"],  # April
    [[(4, 1, 4), (0, 0, 0, 0), 'n'], "ARIMAX"],  # May
    [[(4, 1, 3), (2, 0, 2, 4), 'n'], "SARIMA"],  # June
    [[(4, 1, 4), (1, 0, 1, 4), 'n'], "SARIMAX"],  # July
    [[(3, 1, 3), (2, 0, 2, 4), 'n'], "SARIMA"],  # August
    [[(3, 1, 1), (2, 0, 2, 4), 'n'], "SARIMAX"],  # September
    [[(4, 1, 3), (2, 0, 2, 4), 'n'], "SARIMA"],  # October
    [[(3, 1, 3), (2, 0, 2, 4), 'n'], "SARIMA"],  # November
    [[(3, 1, 4), (2, 0, 2, 4), 'n'], "SARIMA"]  # December
]


def run_and_save_S_ARIMAX_model(train, test_length, exog_train, exog_test, config=[(4, 1, 4), (2, 0, 2, 4), 'n']):
    order, sorder, trend = config
    model = SARIMAX(train, order=order, seasonal_order=sorder, trend=trend, exog=exog_train)
    model_fit = model.fit()
    predict = model_fit.forecast(test_length, exog=exog_test)
    return predict


def run_and_save_SARIMA_model(train, test_length, config=[(4, 1, 4), (2, 0, 2, 4), 'n']):
    order, sorder, trend = config
    model = SARIMAX(train, order=order, seasonal_order=sorder, trend=trend)
    model_fit = model.fit()
    predict = model_fit.forecast(test_length)
    return predict


def model_picker():
    start = (datetime.today() - timedelta(days=35)).strftime('%Y-%m-%d')
    end = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    end_entsoe = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    timezone = "Etc/GMT"  # Europe/Berlin OR Etc/GMT

    renewables_percentage = calculate_percentage_and_combine_data(
        pd.Timestamp(start, tz='Etc/GMT'), pd.Timestamp(end_entsoe, tz='Etc/GMT'),
        ((
             datetime.strptime(
                 end_entsoe,
                 '%Y-%m-%d') - datetime.strptime(
                 start,
                 '%Y-%m-%d')).days) * 96)

    renewables_percentage = renewables_percentage.apply(pd.to_numeric)

    data_frequency_per_day = 96
    # sample call
    renewables_percentage.index = pd.date_range(start="{} 00:00:00".format(start), periods=len(renewables_percentage),
                                                freq='15Min')

    config, model = monthly_config[renewables_percentage.index[-1].month - 1]
    if model == "SARIMA":
        print("sarima", config)
        return run_and_save_SARIMA_model(renewables_percentage, data_frequency_per_day, config)
    else:  # SARIMAX or ARIMAX
        exog_params = get_and_clean_historical_data(start, end, timezone)
        exog_params.index = pd.date_range(start="{} 00:00:00".format(start), periods=len(exog_params), freq='15Min')
        print("(S)arimax", config)
        exog_params = exog_params.apply(pd.to_numeric)
        return run_and_save_S_ARIMAX_model(renewables_percentage, data_frequency_per_day,
                                           exog_params[:-data_frequency_per_day], exog_params[-data_frequency_per_day:],
                                           config)
