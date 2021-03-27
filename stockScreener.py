# ticker.info seems to make a dictionary which containts a lot of info
# so what i may be able to do is call ticker.info and pull from that dict
# need to convert it into its own dict but yep worked

import yfinance as yf
import pandas as pd
from datetime import datetime
from tickerList import tickers
import gspread
from stockSecrets import valueStockFolderId, dashboardURL
import stockquotes

startTime = datetime.now()

tickers = sorted(tickers)

cols = ['Ticker','Sector','Industry','Price to Book', 'Trailing PE','Dividend Rate']

stock_df = pd.DataFrame(columns=cols)

# median PE ratio of the SP 500
# TODO: create an imported function to get med PE of SP500
medianPE = 15   

for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        stockInfo = stock.info
        pbRatio = stockInfo.get('priceToBook')
        trailingPE = stockInfo.get('trailingPE')
        sector = stockInfo.get('sector')
        industry = stockInfo.get('industry')
        dividend = stockInfo.get('dividendRate')
        stockObj = stockquotes.Stock(ticker)
        currentPrice = stockObj.current_price
        if pbRatio < 1 and trailingPE < medianPE and dividend > 0:
            print(ticker,currentPrice,sector,industry,pbRatio,trailingPE,dividend)
            stockDict = {}
            stockDict['Ticker'] = ticker
            stockDict['Price'] = currentPrice
            stockDict['Sector'] = sector
            stockDict['Industry'] = industry
            stockDict['Price to Book'] = pbRatio
            stockDict['Trailing PE'] = trailingPE
            stockDict['Dividend Rate'] = dividend
            stock_df = stock_df.append(stockDict,ignore_index=True)
    except Exception:
        pass

dateString = datetime.strftime(datetime.now(), '%Y_%m_%d')
stock_df.to_csv(f'Value Stocks as of {dateString}')

gc = gspread.oauth()

sh = gc.create(f'Value Stocks as of {dateString}',folder_id=valueStockFolderId)

worksheet = sh.get_worksheet(0)

worksheet.update([stock_df.columns.values.tolist()] + stock_df.values.tolist())

db = gc.open_by_url(dashboardURL)

dbws = db.get_worksheet(0)

# need to clear the first sheet before we can add all the new info
# z1000 is probably overkill but would rather over kill than underkill

range_of_cells = dbws.range('A1:Z1000')
for cell in range_of_cells:
    cell.value = ''
dbws.update_cells(range_of_cells)

dbws.update([stock_df.columns.values.tolist()] + stock_df.values.tolist())

print(datetime.now()-startTime)
