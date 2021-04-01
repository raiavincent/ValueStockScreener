import yfinance as yf
import pandas as pd

def pullStocks(ticker):
    stock_df = pd.DataFrame()
    try:
        stock = yf.Ticker(ticker)
        stockInfo = stock.info
        # pbRatio = stockInfo.get('priceToBook')
        # trailingPE = stockInfo.get('trailingPE')
        # sector = stockInfo.get('sector')
        # industry = stockInfo.get('industry')
        # dividend = stockInfo.get('dividendRate')
        # stockObj = stockquotes.Stock(ticker)
        # currentPrice = stockObj.current_price
        # stockInfo['Price'] = currentPrice
        # print(ticker)
        stock_df = stock_df.append(stockInfo,ignore_index=True)
        # stock_df = stock_df.append(priceDict,ignore_index=True)
    except Exception:
        # need to add Exception to except statement to allow for 
        # keyboard interrupt
        pass
    return stock_df

if __name__ == '__main__':
    pullStocks()