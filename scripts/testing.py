#!/usr/bin/python
# DerekM - 2021
# The data is gathered from Alpha Vantage which has a delay of 1 day on all stock data.
# Please factor that into any tradng decisions (this is based on Daily RSI so it's not such a big issue here)
#

print("Test %")

def pct_change(first, second):
    diff = second - first
    change = 0
    try:
        if diff > 0:
            change = (diff / first) * 100
        elif diff < 0:
            diff = first - second
            change = -((diff / first) * 100)
    except ZeroDivisionError:
        return float('inf')
    return change
    

CLOSE = 170.1
PRICE = 174.2

DIFFV = pct_change(CLOSE,PRICE)
DIFFV = float(round(DIFFV,2))
print(DIFFV)