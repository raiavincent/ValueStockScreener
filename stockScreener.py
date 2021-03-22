from get_all_tickers import get_tickers as gt
import yfinance as yf
import pandas as pd

tickers = gt.get_tickers()

tickers = sorted(tickers)

cols = ['Ticker','Price to Book', 'Trailing PE']

stock_df = pd.DataFrame(columns=cols)

# median PE ratio of the SP 500
medianPE = 15   

print('TICKER     PB RATIO     TRAILING PE')
x=0
for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        stockInfo = stock.info
        pbRatio = stockInfo.get('priceToBook')
        # pbRatio = round(pbRatio,2)
        trailingPE = stockInfo.get('trailingPE')
        # trailingPE = round(trailingPE,2)
        # ticker = ticker.ljust(5)
        # pbRatio = pbRatio.ljust(9)
        if pbRatio < 1 and trailingPE < medianPE:
            print(ticker,pbRatio,trailingPE)
            stockDict = {}
            stockDict['Ticker'] = ticker
            stockDict['Price to Book'] = pbRatio
            stockDict['Trailing PE'] = trailingPE
            stock_df = stock_df.append(stockDict,ignore_index=True)
    except:
        pass



# ticker.info seems to make a dictionary which containts a lot of info
# so what i may be able to do is call ticker.info and pull from that dict
# need to convert it into its own dict but yep worked
