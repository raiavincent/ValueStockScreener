import pandas as pd
from datetime import datetime
from tickerList import tickers
import gspread
from stockSecrets import valueStockFolderId, dashboardURL, dbId
import stockquotes
import stockAttribPuller as sap
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
    
stock_df = stock_df.dropna(axis=1,how='all')
stock_df.fillna('',inplace=True)
stock_df = stock_df.applymap(str)
# need to change 52WeekChange column name because BigQuery does not like 
# columns that start with numbers
stock_df = stock_df.rename(columns={'52WeekChange':'WeekChange52'})

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
range_of_cells = worksheet.range('A1:CZ10000')
worksheet.update_cells(range_of_cells,value_input_option='USER_ENTERED')

# open the main workbook with that workbook's url
db = gc.open_by_url(dashboardURL)

# changed this over to the second sheet so the dashboard can be the first sheet
# dbws is the database worksheet, as in the main workbook that is updated and
# used to analyze and pick from
dbws = db.get_worksheet(1)

# below clears the stock sheet so it can be overwritten with updates
# z1000 is probably overkill but would rather over kill than underkill
range_of_cells = dbws.range('A1:CU10000')
for cell in range_of_cells:
    cell.value = ''
dbws.update_cells(range_of_cells)

# update the stock spreadsheet in the database workbook with the stock_df
# need to specify this as user entered to keep the data type
dbws.update([stock_df.columns.values.tolist()] + stock_df.values.tolist())

# unstringify the strung data for SQL purposes
spreadsheetId = dbId  # Please set the Spreadsheet ID.
sheetName = "Data"  # Please set the sheet name.

spreadsheet = gc.open_by_key(spreadsheetId)
sheetId = spreadsheet.worksheet(sheetName)._properties['sheetId']

requests = {
    "requests": [
        {
            "findReplace": {
                "sheetId": sheetId,
                "find": "^'",
                "searchByRegex": True,
                "includeFormulas": True,
                "replacement": ""
            }
        }
    ]
}

spreadsheet.batch_update(requests)

# output total time to run this script
print(datetime.now()-startTime)
