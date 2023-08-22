# stock_data_fetcher.py

import yfinance as yf
import pandas as pd

def get_stock_data(tickerSymbol, start_date, end_date, save_format=None, filename=None):
    # Get data on this ticker
    tickerData = yf.Ticker(tickerSymbol)

    # Get the historical prices for this ticker
    tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)

    # Process datetime column
    tickerDf.reset_index(inplace=True)
    for column in tickerDf.columns:
        if pd.api.types.is_datetime64tz_dtype(tickerDf[column]):
            tickerDf[column] = tickerDf[column].dt.tz_localize(None)

    # Create stock column
    tickerDf["stock"] = tickerSymbol

    # Save the dataframe locally if save_format is provided
    if save_format:
        if not filename:
            filename = f"{tickerSymbol}_stock_data"
        
        if save_format == "excel":
            tickerDf.to_excel(f"{filename}.xlsx", index=False)
        elif save_format == "csv":
            tickerDf.to_csv(f"{filename}.csv", index=False)

    return tickerDf

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python stock_data_fetcher.py <TICKER> <START_DATE> <END_DATE> [save_format: excel/csv] [filename]")
        sys.exit(1)

    ticker, start_date, end_date = sys.argv[1], sys.argv[2], sys.argv[3]
    save_format = sys.argv[4] if len(sys.argv) > 4 else None
    filename = sys.argv[5] if len(sys.argv) > 5 else None

    data = get_stock_data(ticker, start_date, end_date, save_format, filename)
    print(data)
