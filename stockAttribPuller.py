import yfinance as yf
import pandas as pd

def pullStocks(ticker):
    '''
    This function pulls down all necessary info for a stock we are adding to
    a dataframe and creates its own singular dataframe. In the main script, it
    appends all of the stock dataframes into one.

    Parameters
    ----------
    ticker : str
        The ticker of the stock we are currently pulling info for.

    Returns
    -------
    stock_df : dataframe
        A dataframe of stock information.

    '''
    stock_df = pd.DataFrame()
    try:
        stock = yf.Ticker(ticker)
        stockInfo = stock.info
        stock_df = stock_df.append(stockInfo,ignore_index=True)
        stock_df = stock_df.drop(['uuid'])
    except Exception:
        # need to add Exception to except statement to allow for 
        # keyboard interrupt
        pass
    return stock_df

if __name__ == '__main__':
    pullStocks()