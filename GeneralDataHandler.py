import pandas as pd
from RadiationDataController import bulk_get_radiation_data
from WeatherDataController import bulk_get_weather_data

from GenerationDataController import calculate_percentage_and_combine_data


def merge_datasets_by_taking_average(df, target_columns):
    assert_on_number_of_rows(df)
    output = []
    for row in range(len(df[0])):
        output.append([])
        for col in target_columns:
            sum = 0
            for i in range(len(df)):
                sum = sum + float(df[i][col][row])
            mean = sum / (len(df))
            output[row].append(mean)
            # print(output[row])
    return pd.DataFrame([x for x in output], columns=target_columns, index=df[0].index)


def assert_on_number_of_rows(df):
    for i in df:
        assert len(i) == len(df[0]), "Oh no! Number of rows did NOT match! {} vs. {}".format(len(df[0]), len(i))
        # if len(i) != len(df[0]):
        #  print(len(df[0]), "vs.",len(i))
        #  raise Exception("Sorry, number of rows in between different cities do not match.")


def get_and_clean_historical_data(start, end, timezone):
    columns = ["time", "time_local", "temperature", "dewpoint", "humidity", "precipitation", "precipitation_3",
               "precipitation_6", "snowdepth", "windspeed", "peakgust", "winddirection", "pressure", "condition"]

    cities = ["memmingen", "Rostock Warnem-u00fcnde"]
    station_ids = ["10947", "10170"]
    latitude = ["47.9833", "54.1833"]
    longitude = ["10.2333", "12.0833"]
    altitude = ["634", "4"]

    # cities=["memmingen","Rostock Warnem-u00fcnde","Osnabrueck","Braunschweig","Cuxhaven","Luebeck","Berlin","Bonn","Hof","Freudenstadt","München","Meiningen"]
    # station_Ids = ["10947","10170" ,    "10315"   ,"10348"  ,"10131"  ,"10156"  ,"10382"  ,"10513"  ,"10685"  ,"10815"  ,"10865"  ,"10548"]
    # latitude=     ["47.9833","54.1833" ,"52.1333" ,"52.3"   ,"53.8667","53.8167","52.5667","50.8667","50.3167","48.45"  ,"48.1333","50.5667"]
    # longitude=    ["10.2333","12.0833" ,"7.7"     ,"10.45"  ,"8.7"    ,"10.7"   ,"13.3167","7.1667" ,"11.8833","8.4167" ,"11.55"  ,"10.3833"]
    # altitude=     ["634",   "4" ,        "48"     ,"81"     ,"5"      ,"14"     ,"37"     ,"91"     ,"565"    ,"797"    ,"520"    ,"450"]

    altitude = -999

    # cities=["Bon"]
    # station_Ids = ["10513"]
    # start="2017-12-30"
    # end="2020-07-11"


    windspeed_data = bulk_get_weather_data(cities, station_ids, start, end, timezone)
    ghi_data = bulk_get_radiation_data(cities, start, end, latitude, longitude, altitude)

    average_windspeed = merge_datasets_by_taking_average(windspeed_data, ["windspeed"])
    average_ghi = merge_datasets_by_taking_average(ghi_data, ["GHI"])

    upsampled_data = average_windspeed.resample('15min').mean()

    filledData_spline = upsampled_data.interpolate(method='spline', order=2).round(3)

    # windspeed data is available until  23:00, so using last data point to make data until 23:45
    last_datapoint = filledData_spline.loc[[filledData_spline.index[-1]]]
    for i in range(3):
        filledData_spline = filledData_spline.append(last_datapoint, ignore_index=False)
    # for missing ghi (normally 1 day)
    # could be removed after testing
    last_dp = average_ghi.loc[[average_ghi.index[-1]]]
    for i in range(len(filledData_spline) - len(average_ghi)):
        average_ghi = average_ghi.append(last_dp, ignore_index=False)

    assert_on_number_of_rows([average_ghi, filledData_spline])
    filledData_spline.index = average_ghi.index

    result = pd.concat([filledData_spline, average_ghi], axis=1, sort=False)

    return result.append(get_and_clean_real_time_data(cities, longitude, latitude))


"""# TO-DO: Get weather data from SODA PRO for the last today and tomorrow"""


def get_today_data_request(label, latitude, longitude, altitude, start, end, columns):
    url = 'http://www.soda-pro.com/api/jsonws/helioclim3-forecast-portlet.hc3request/proxy?url=http%253A%252F%252Fwww.soda-is.com%252Fcom%252Fhc3v5_meteo_soda_get.php%253Flatlon%253D{}%252C{}%2526alt%253D-999%2526date1%253D{}%2526date2%253D{}%2526summar%253D15%2526refTime%253DUT%2526tilt%253D0%2526azim%253D180%2526al%253D0.2%2526horizon%253D1%2526outcsv%253D1%2526forecast%253D2%2526gamma-sun-min%253D12%2526header%253D1%2526code%253D1%2526format%253Dunified'.format(
        latitude, longitude, start, end)
    resp = requests.get(url).content
    link = str(resp).split("value>")

    csvfile = requests.get(link[1][:len(link[1]) - 2]).content

    # removing headers
    content = csvfile[csvfile.decode("utf-8").find("Date;Time;Global Horiz;Clear-Sky;"):]

    df = pd.DataFrame([x.split(';') for x in content.decode("utf-8").split('\n')[1:]],
                      columns=[x for x in content.decode("utf-8").split('\n')[0].split(';')])
    df.index = pd.date_range(start="{} 00:00:00".format(start), periods=len(df), freq='15Min')
    df.index.name = 'time'
    # removing the last empty line
    df = df.drop(df.index[-1])
    # replacing missing values with the previous non-missing value
    df[columns] = df[columns].ffill()

    # changing type from non-type to float. because later we want to calculate the average among all cities
    df[columns] = df[columns].apply(pd.to_numeric)

    # m/s to km/h ~ 3.6
    df['Wind speed'] = [element * 3.6 for element in df['Wind speed']]
    # df.copy().to_csv('/content/drive/My Drive/Colab Notebooks/Renewables/RadiationData/{}.csv'.format(label),columns=columns)
    return df


"""##Defining columns and cities, Getting station IDs which needs to be set manually"""

import json
import requests
from datetime import datetime, timedelta


def get_and_clean_real_time_data(cities, longitude, latitude):
    start = (datetime.today()).strftime('%Y-%m-%d')
    end = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    altitude = -999
    today_data = []
    for i in range(len(cities)):
        today_data.append(
            get_today_data_request(label="realtime{}-{}___{}".format(cities[i], start, end), latitude=latitude[i],
                                   longitude=longitude[i], altitude=altitude, start=start, end=end,
                                   columns=['Global Horiz', 'Wind speed']))

    average_today = merge_datasets_by_taking_average(today_data, ['Wind speed', 'Global Horiz'])
    # average_ghi = merge_datasets_by_taking_average(ghi_data,["GHI"])
    average_today.columns = ["windspeed", "GHI"]
    return average_today


def combine_generation_and_exogenous_data(start, end, end_entsoe, timezone):
    return get_and_clean_historical_data(start, end, timezone), calculate_percentage_and_combine_data(
        pd.Timestamp(start, tz='Etc/GMT'), pd.Timestamp(end_entsoe, tz='Etc/GMT'),
        ((
             datetime.strptime(
                 end_entsoe,
                 '%Y-%m-%d') - datetime.strptime(
                 start,
                 '%Y-%m-%d')).days) * 96)
