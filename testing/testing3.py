tickerlist = "tickers/tickerfile.txt"
tickerlist = "tickers/tickerfile_TRADELIST.txt"
tickerlist = "tickers/tickerfile_TEST.txt"
#tickerlist = "tickers/tickerfile_TEST_UK.txt"
#tickerlist = "tickers/tickerfile_TEST_USA.txt"
with open(tickerlist) as file:
    tickers = [ticker.rstrip('\n') for ticker in file]
    print(tickers)