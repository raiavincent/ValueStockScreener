import yfinance as yf
import pandas as pd

def pullStocks(ticker):
    stock_df = pd.DataFrame()
    try:
        stock = yf.Ticker(ticker)
        stockInfo = stock.info
        stock_df = stock_df.append(stockInfo,ignore_index=True)
    except Exception:
        # need to add Exception to except statement to allow for 
        # keyboard interrupt
        pass
    return stock_df

if __name__ == '__main__':
    pullStocks()