"""
Scrape stock data using Alpha Vantage API
Reference: https://www.alphavantage.co/
"""

import os
import pandas as pd
import time
import argparse

from alpha_vantage_utils import get_time_series_data


def main():
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('write_dir', help='dataset write directory')
    args = parser.parse_args()

    # create empty dataframe to hold opening price data
    # each day (col) is an observation (row) of opening price data
    open_df = pd.DataFrame(columns=['timestamp'])

    # get symbols for all markets
    nasdaq_symbols_df = pd.read_csv('market_symbols/nasdaq_symbols.csv')
    # amex_symbols_df = pd.read_csv('market_symbols/amex_symbols.csv')
    # nyse_symbols_df = pd.read_csv('market_symbols/nyse_symbols.csv')

    # configure Alpha Vantage args
    function = 'TIME_SERIES_DAILY_ADJUSTED'
    apikey = os.environ.get('ALPHAVANTAGE_API_KEY')

    # grab stock data for nasdaq market (limited to 5 requests per min)
    for symbol in nasdaq_symbols_df['Symbol']:
        # request data
        data = get_time_series_data(
            function, symbol, apikey, output_size='full', datatype='csv')

        # rate limit check block
        if type(data) == int and data == -1:
            # rate limited, wait 60 seconds
            print('[INFO]: waiting 60 seconds...')

            # sleep for a little longer than 60 seconds
            time.sleep(65)

            # request data again
            data = get_time_series_data(
                function, symbol, apikey, output_size='full', datatype='csv')

        if type(data) == int and data == 0:
            # error or no data for this symbol
            print('[INFO]: Error or missing data for {}'.format(symbol))
        elif type(data) == int and data == -2:
            # day limit, exit to try again tomorrow
            print('[INFO]: reached daily request limit; exiting')
            exit()
        else:
            # we got some legit data for a symbol
            print('[INFO]: Writing data for {}'.format(symbol))

            # add column if not already in dataset
            open_df = open_df.merge(
                data[['timestamp', 'open']], how='outer', on='timestamp')\
                .rename({'open': symbol}, axis=1)

        # save data to csv
        open_df.to_csv(
            '{}open_prices.csv'.format(args.write_dir), index=False)


if __name__ == '__main__':
    main()
