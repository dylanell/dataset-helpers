# Alpha Vantage Dataset Helpers

This project uses the [Alpha Vantage API](https://www.alphavantage.co/) to query historical stock price data.

### Environment:

- Python 3.7.4

### Python Packages:

- requests
- pandas

### Prerequisites:

In order to use the Alpha Vantage API, you must first obtain a free API key from their website [here](https://www.alphavantage.co/support/#api-key). This key will need to be included as a variable in API requests in order to receive a query response from Alpha Vantage servers.

*Note*: Alpha Vantage currently limits free accounts to 5 requests per minute and 500 total requests per day.

### `generate_dataset.py`:

Run:

```
$ python generate_dataset.py
```

At this time, the dataset generator script is hardcoded to pull daily opening price time series stock data from stocks within the NASDAQ, AMEX, or NYSE markets. Symbols for these stocks are pulled from corresponding csv lookup-files for each market located in the `market_symbols` directory of this project. The daily opening prices for each stock symbol are written to a csv file with the following format:

```
timestamp, symbol1, symbol2, ...
YYYY-MM-DD, open1, open2, ...
...
```

Future versions of this project will support generating datasets from other time series data by changing the `function` specification according to the argument flags defined in the [Alpha Vantage Time Series Stock API Documentation](https://www.alphavantage.co/documentation/#time-series-data).

### References:

1. Alpha Vantage API documentation:
  - https://www.alphavantage.co/documentation/#
