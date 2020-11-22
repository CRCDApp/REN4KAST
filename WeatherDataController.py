import json
import requests
import pandas as pd
from datetime import datetime as dateT, timedelta
import csv


def get_request(url=""):
    response = requests.get(url)
    if response.status_code != 200:
        print("!!!\tREQUEST FOR GETTING DATA FAILED\t!!! \n\n")
    return response.json()


# converts raw json input to csv and saves into the defined file
# for path parameter app.config["DATASET_FOLDER"] could be used
def weather_json_to_csv(label="", city="output.csv", json_data='', columns=[]):
    with open('/content/drive/My Drive/Colab Notebooks/Renewables/WeatherData/{}-{}.csv'.format(city, label), 'w',
              newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # csv_writer.writerow(["date-from", "date-to", "renewables"])
        csv_writer.writerow(columns)
        for xx in json_data["data"]:
            # Converting Date Time in milisecond to predefined date time
            # Removed "DATE-TO", could be added if it's necessary
            csv_writer.writerow([xx[item] for item in columns])
            # xxx= json.loads(json_data)
            # to pd
            # pd.json_normalize(json.loads(json.dumps(json_data["data"])))


def weather_json_to_pd_and_cv(label, city, json_data, columns, start):
    data = pd.json_normalize(json.loads(json.dumps(json_data["data"])))
    data.index = pd.date_range(start="{} 00:00:00".format(start), periods=len(data), freq='H')
    data.index.name = 'time'
    # replacing missing values with the previous non-missing value
    data[columns] = data[columns].ffill()
    #data.copy().to_csv('/content/drive/My Drive/Colab Notebooks/Renewables/WeatherData/{}-{}.csv'.format(city, label), columns=columns)
    return data


def bulk_get_weather_data(cities, station_ids, start, end, timezone):
    windspeed_data = []

    for i in range(len(cities)):
        # getting windspeed from meteostat
        # weather_json_to_csv(label=station_Ids[i]+"__"+start+"__"+end+"__tz-"+tz, city=cities[i], json_data=get_request("https://api.meteostat.net/v1/history/hourly?station={}&start={}&end={}&time_zone={}&time_format=Y-m-d%20H:i&key=OpDs5PvR".format(station_Ids[i],start,end,timezone) ), columns=columns)
        windspeed_data.append(
            weather_json_to_pd_and_cv(label=station_ids[i] + "__" + start + "__" + end + "__tz-" + timezone,
                                      city=cities[i],
                                      json_data=get_request(
                                          "https://api.meteostat.net/v1/history/hourly?station={}&start={}&end={}&time_zone={}&time_format=Y-m-d%20H:i&key=OpDs5PvR".format(
                                              station_ids[i], start, end, timezone)), columns=["windspeed"], start=start))

    return windspeed_data
