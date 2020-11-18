


RS = 2
RSI = str(round((100 - (100/(1+RS))), 2))


print(RSI)

tickerlist = "tickers/tickerfile.txt"

with open(tickerlist) as file:
    tickers = [ticker.rstrip('\n') for ticker in file]

print(tickers)