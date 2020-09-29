tickerlist = "tickerfile.txt"
with open(tickerlist) as file:
    tickers = [ticker.rstrip('\n') for ticker in file]
for ticker in tickers:
    print(ticker)


avg_gain

avg_gainavg_gain