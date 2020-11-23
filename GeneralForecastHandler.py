from datetime import datetime, timedelta

import tensorflow as tf
import multiprocessing as mp
from statsmodels.tsa.statespace.sarimax import SARIMAX

monthly_config = [
    [(2, 0, 2), (2, 1, 1, 4), 'n'],  # January
    [(2, 0, 4), (0, 0, 0, 0), 'n'],  # February
    [(4, 0, 3), (0, 0, 0, 0), 'n'],  # March
    [(4, 1, 3), (2, 0, 2, 4), 'n'],  # April
    [(4, 1, 4), (0, 0, 0, 0), 'n'],  # May
    [(4, 1, 3), (2, 0, 2, 4), 'n'],  # June
    [(4, 1, 4), (1, 0, 1, 4), 'n'],  # July
    [(3, 1, 3), (2, 0, 2, 4), 'n'],  # August
    [(3, 1, 1), (2, 0, 2, 4), 'n'],  # September
    [(4, 1, 3), (2, 0, 2, 4), 'n'],  # October
    [(3, 1, 3), (2, 0, 2, 4), 'n'],  # November
    [(3, 1, 4), (2, 0, 2, 4), 'n']  # December
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
