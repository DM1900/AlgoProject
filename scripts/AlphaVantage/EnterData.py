import csv
from datetime import datetime, timedelta

# Python program showing  
# a use of input() 

Date = datetime.now().strftime("%d/%m/%Y") # "%Y%m%d-%H%M") # input("Enter the date (dd/mm/yyyy): ") 
print("Enter data for {}".format(Date))
TotalValue = input("Enter total account value: ") 
PieValue = input("Enter Pie value: ") 
Investment = input("Enter invested amount: ") 
PieInvestment = input("Enter Pie invested amount: ") 
Realised = input("Enter Realised value: ") 
Dividend = input("Enter Dividend value received: ") 

YEAR = datetime.now().strftime("%Y") 
CSVFILE =  'scripts/AlphaVantage/data/stock_{}.csv'.format(YEAR)

# https://realpython.com/python-csv/
print(Date,TotalValue,PieValue,Investment,PieInvestment,Realised,Dividend)
 

with open(CSVFILE, mode='a') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #employee_writer.writerow(['John Smith', 'Accounting', 'November'])
    writer.writerow([Date,TotalValue,PieValue,Investment,PieInvestment,Realised,Dividend])

"""

TOTAL = 1899.42
PIE = 444.85

ACTIVE = round(TOTAL-PIE,2)

print(ACTIVE)

RISK = 0.5
TORISK = round(ACTIVE*(RISK/100),2)

print(TORISK)
"""