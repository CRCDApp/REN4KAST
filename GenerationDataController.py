"""#GETTING ENTSOE REAL TIME DATA"""

from datetime import datetime, timedelta
from entsoe import EntsoePandasClient
import pandas as pd
from GeneralDataHandler import assert_on_number_of_rows


def get_entsoe_data(start, end, expected_length):
    client = EntsoePandasClient("94aa148a-330b-4eee-ba0c-8a5eb0b17825")
    # start = pd.Timestamp(datetime.strptime("2020-07-01", '%Y-%m-%d'), tz='Etc/GMT')
    # end = pd.Timestamp(datetime.strptime("2020-07-11", '%Y-%m-%d'), tz='Etc/GMT')
    # start = pd.Timestamp((datetime.today() - timedelta(days=35)).strftime('%Y-%m-%d'), tz='Etc/GMT')
    # end = pd.Timestamp((datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d'), tz='Etc/GMT')
    country_code = 'DE'  # Germany

    # methods that return Pandas Series
    # dar in method
    # 'documentType': 'A75',
    # 'processType': 'A16',
    # https://github.com/EnergieID/entsoe-py/blob/5d176699472744c1acef546410826da6549112cf/entsoe/entsoe.py#L270
    #
    entsoe_data = client.query_generation(country_code, start=start, end=end, psr_type=None)

    # converting to GMT
    entsoe_data.index = entsoe_data.index.tz_convert('Etc/GMT')
    # entsoe_data.to_csv('/content/drive/My Drive/Colab Notebooks/Renewables/ENTSOE-DATA/GMT-ENTSOE-{}-{}-{}.csv'.format(country_code,start, end),sep=',', encoding='utf-8')
    """Handling missing and null values for last few datapoints (today)"""

    # https://towardsdatascience.com/data-cleaning-with-python-and-pandas-detecting-missing-values-3e9c6ebcf78b
    # entsoe_data.isnull()#.values.any()
    # entsoe_data.isnull().sum()

    last_dp = entsoe_data.loc[[entsoe_data.index[-1]]]
    for i in range(expected_length - len(entsoe_data)):
        entsoe_data = entsoe_data.append(last_dp, ignore_index=False)

    entsoe_data = entsoe_data.ffill()
    return entsoe_data


def calculate_percentage_and_combine_data(start, end, expected_length):
    entsoe_data = get_entsoe_data(start, end, expected_length)
    assert expected_length == len(entsoe_data), "Oh no! Number of rows did NOT match! {} vs. {}".format(expected_length,
                                                                                                        len(
                                                                                                            entsoe_data))

    entsoe_data.index = pd.date_range(start="{} 00:00:00".format(start), periods=len(entsoe_data), freq='15Min')
    entsoe_data.index.name = 'time'
    """trying to remove null values but since it has 3 hours delay, error happens cause few last rows are null and it cannot handle it.

    For now this step could be ignored
    """

    generation_data = entsoe_data
    sumBioMassAndHydro = generation_data['Biomass'] + generation_data['Hydro Run-of-river and poundage'] + \
                         generation_data[
                             'Hydro Water Reservoir'] + generation_data['Geothermal'] + generation_data['Waste']
    sumBioMassAndHydro

    sumOthers = generation_data['Wind Offshore'] + generation_data['Wind Onshore'] + generation_data['Solar'] + \
                generation_data['Nuclear'] + generation_data['Fossil Brown coal/Lignite'] + generation_data[
                    'Fossil Hard coal'] + generation_data['Fossil Gas'] + generation_data['Hydro Pumped Storage'] + \
                generation_data['Other'] + generation_data['Other renewable'] + generation_data['Fossil Oil']
    print(sumOthers)

    calcTotal = sumBioMassAndHydro + sumOthers
    calcTotal

    RenForecast = generation_data.drop(columns=['Biomass', 'Fossil Brown coal/Lignite', 'Fossil Gas',
                                                'Fossil Hard coal', 'Fossil Oil', 'Geothermal', 'Hydro Pumped Storage',
                                                'Hydro Run-of-river and poundage', 'Hydro Water Reservoir', 'Nuclear',
                                                'Other', 'Waste', ('Other renewable', 'Actual Consumption'),
                                                ('Solar', 'Actual Consumption'),
                                                ('Wind Onshore', 'Actual Consumption')])

    # print(RenForecast.columns)
    RenForecast.insert(0, "calcTotal", calcTotal["Actual Aggregated"], True)
    RenForecast.insert(1, "sumBioMassAndHydro", sumBioMassAndHydro["Actual Aggregated"], True)

    RenForecast.columns = ["calcTotal", "sumBioMassAndHydro", "Other renewable", "Solar", "Wind Offshore",
                           "Wind Onshore"]
    RenForecast

    renewablesPercentage = pd.DataFrame(columns=['percentage'], index=[RenForecast.index])
    forecast = RenForecast.copy()
    for index, row in forecast.iterrows():
        if (row["sumBioMassAndHydro"].all == 0.0):
            print(row["sumBioMassAndHydro"])

    renewablesPercentage = pd.DataFrame(columns=['percentage'], index=[RenForecast.index])
    forecast = RenForecast.copy()
    for index, row in forecast.iterrows():
        sum_renewables = row['sumBioMassAndHydro'] + row['Other renewable'] + row['Solar'] + row['Wind Offshore'] + row[
            'Wind Onshore']
        prct = sum_renewables / row['calcTotal']
        prct = prct * 100
        renewablesPercentage.loc[index] = [round(prct, 2)]
        # / bar tedad *100
    renewablesPercentage

    renewablesPercentage.index = entsoe_data.index
    return renewablesPercentage

    # finalres.to_csv( '/content/drive/My Drive/Colab Notebooks/Renewables/ENTSOE-DATA/ENTSOE-ALL-RENEWABLES-PERCENTAGE-NOT-ORIGINAL-DE-{}-{}.csv'.format(start, end), sep=',', encoding='utf-8')
