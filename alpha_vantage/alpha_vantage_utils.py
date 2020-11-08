"""
Utility functions for the Alpha Vantage API.
Reference: https://www.alphavantage.co/documentation/
"""

import requests
import pandas as pd
import io

def get_time_series_data(function, symbol, apikey, outputsize='full', datatype='csv'):
    """
    - function (str): Specifies which type of data to pull. Refer to API docs.
    - symbol (str): Specifies which stock (i.e. 'IBM') to pull data from.
    - apikey (str): Your API access key from Alpha Vantage.
    - outputsize (str): 'full' (default) for 20 years of data or 'compact' for
        only 100 data samples.
    - datatype (str): 'csv' (default) to return data in Pandas dataframe or
        'json' to return data as Python dictionary.
    """

    # construct endpoint request string
    request = \
        'https://www.alphavantage.co/query?function={}&symbol={}' \
        '&outputsize={}&apikey={}&datatype={}'. \
        format(function, symbol, outputsize, apikey, datatype)

    # query endpoint
    response = requests.get(request)

    # try to parse json from response
    try:
        response_json = response.json()
        if 'Error Message' in list(response_json.keys()):
            #print('[ALPHAVANTAGE ERROR]')
            return 0
        elif 'Note' in list(response_json.keys()):
            #print('[ALPHAVANTAGE RATE LIMIT]')
            return -1
        elif 'Information' in list(response_json.keys()):
            #print('[ALPHAVANTAGE DAY LIMIT]')
            return -2
    except:
        pass

    # return data in desired format
    if (datatype == 'csv'):
        return pd.read_csv(io.BytesIO(response.content), encoding='utf8')
    else:
        return response.json()
