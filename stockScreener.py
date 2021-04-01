import pandas as pd
from datetime import datetime
from tickerList import tickers
import gspread
from stockSecrets import valueStockFolderId, dashboardURL
import stockquotes
import stockAttribPuller as sap
from stockCols import cols
import importlib

# start timer
startTime = datetime.now()
importlib.reload(sap)

# create dateString to get the date for the sheet
dateString = datetime.strftime(datetime.now(), '%Y_%m_%d')

# sort tickers, not sure why, but I did
tickers = sorted(tickers) 

# ticker.info is used from yf to create a json that I can pull from
# called for each ticker in the list
# store that json as its own variable and pull the data
# stockquotes module is used to get the current price of the ticker object

stock_df = pd.DataFrame()
index = 1
for ticker in tickers:
    try:
        ticker_df = sap.pullStocks(ticker)
        stockObj = stockquotes.Stock(ticker)
        currentPrice = stockObj.current_price
        ticker_df['Price'] = currentPrice
        # current price is not being added here
        stock_df = stock_df = stock_df.append(ticker_df,ignore_index=True)
        print(index, ticker)
        index += 1
    except Exception:
        pass
    
stock_df = stock_df[cols]
stock_df = stock_df.dropna(axis=1,how='all')
stock_df.fillna('N/A',inplace=True)

tickerCount = len(stock_df.index)
tickerCount = '{:,}'.format(tickerCount)
print(f'Pulled {tickerCount} stocks on {dateString}'.format(tickerCount))

# gc authorizes and lets us access the spreadsheets
gc = gspread.oauth()

# create the workbook where the day's data will go
# add in folder_id to place it in the folder we want
sh = gc.create(f'Stock sheet as of {dateString}',folder_id=valueStockFolderId)

# access the first sheet of that newly created workbook
worksheet = sh.get_worksheet(0)

# edit the worksheet with the created dataframe for the day's data
worksheet.update([stock_df.columns.values.tolist()] + stock_df.values.tolist())

# open the main workbook with that workbook's url
db = gc.open_by_url(dashboardURL)

# changed this over to the second sheet so the dashboard can be the first sheet
# dbws is the database worksheet, as in the main workbook that is updated and
# used to analyze and pick from
dbws = db.get_worksheet(1)

# below clears the stock sheet so it can be overwritten with updates
# z1000 is probably overkill but would rather over kill than underkill
range_of_cells = dbws.range('A1:Z1000')
for cell in range_of_cells:
    cell.value = ''
dbws.update_cells(range_of_cells)

# update the stock spreadsheet in the database workbook with the stock_df
dbws.update([stock_df.columns.values.tolist()] + stock_df.values.tolist())

# output total time to run this script
print(datetime.now()-startTime)
