# get all tickers as a list and then import that list and iterate over it

from get_all_tickers import get_tickers as gt

tickers = gt.get_tickers()

with open("tickers.txt", "w") as output:
    output.write(str(tickers))