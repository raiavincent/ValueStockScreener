import yfinance as yf
import pandas as pd
from datetime import datetime
import gspread
from stockSecrets import valueStockFolderId, dashboardURL
import stockquotes
from get_all_tickers import get_tickers as gt
import schedule
import time

def getStocks():
    # start timer
    startTime = datetime.now()
    
    # create dateString to get the date for the sheet
    dateString = datetime.strftime(datetime.now(), '%Y_%m_%d')
    
    # sort tickers, not sure why, but I did
    tickers = sorted(gt.get_tickers())
    
    # establish database names and the dataframe
    cols = (['Ticker','Price','Sector','Industry','Price to Book',
             'Trailing PE','Dividend Rate'])
    
    stock_df = pd.DataFrame(columns=cols)
    
    # median PE ratio of the SP 500, using 15 for now until function made
    # TODO create an imported function to get med PE of SP500
    medianPE = 15   
    
    # ticker.info is used from yf to create a json that I can pull from
    # called for each ticker in the list
    # store that json as its own variable and pull the data
    # stockquotes module is used to get the current price of the ticker object
    for ticker in tickers:
        # try except statement to get around any data that may not be available 
        # and causing errors
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
                print(ticker,currentPrice,sector,industry,pbRatio,
                       trailingPE,dividend)
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
            # need to add Exception to except statement to allow for 
            # keyboard interrupt
            pass
    
    # gc authorizes and lets us access the spreadsheets
    gc = gspread.oauth()
    
    # create the workbook where the day's data will go
    # add in folder_id to place it in the folder we want
    sh = gc.create(f'Value Stocks as of {dateString}',folder_id=valueStockFolderId)
    
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

schedule.every().monday.at('16:15').do(getStocks)
schedule.every().tuesday.at('16:15').do(getStocks)
schedule.every().wednesday.at('16:15').do(getStocks)
schedule.every().thursday.at('16:15').do(getStocks)
schedule.every().friday.at('16:15').do(getStocks)

while True:
    schedule.run_pending()
    time.sleep(1)