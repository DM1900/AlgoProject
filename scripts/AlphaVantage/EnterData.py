import csv
from datetime import datetime, timedelta

# Python program showing  
# a use of input() 

YEAR = datetime.now().strftime("%Y") 
CSVFILE =  'scripts/AlphaVantage/data/stock_{}.csv'.format(YEAR)

Date = datetime.now().strftime("%d/%m/%Y") # "%Y%m%d-%H%M") # input("Enter the date (dd/mm/yyyy): ") 


data = []
def import_csv(csvfilename):
    with open(CSVFILE) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_index = 0
        for row in csv_reader:
            if row:  # avoid blank lines
                row_index += 1
                columns = [str(row_index), row[0], row[1], row[2], row[3], row[4], row[5], row[6]]
                data.append(columns)


import_csv(CSVFILE)

data = data[-1]
if Date in data:
    #print("Date ({}) already assigned, do you wish to continue?".format(date))
    CONTINUE = input("Date ({}) already assigned, do you wish to continue?".format(Date)) 
    if CONTINUE == "yes":
        "Do Something"
    else:
        "Do nothing"

"""


print("Enter data for {}".format(Date))
TotalValue = input("Enter total account value: ") 
PieValue = input("Enter Pie value: ") 
Investment = input("Enter invested amount: ") 
PieInvestment = input("Enter Pie invested amount: ") 
Realised = input("Enter Realised value: ") 
Dividend = input("Enter Dividend value received: ") 

# https://realpython.com/python-csv/
print(Date,TotalValue,PieValue,Investment,PieInvestment,Realised,Dividend)
 

with open(CSVFILE, mode='a') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #employee_writer.writerow(['John Smith', 'Accounting', 'November'])
    writer.writerow([Date,TotalValue,PieValue,Investment,PieInvestment,Realised,Dividend])

"""
"""

TOTAL = 1899.42
PIE = 444.85

ACTIVE = round(TOTAL-PIE,2)

print(ACTIVE)

RISK = 0.5
TORISK = round(ACTIVE*(RISK/100),2)

print(TORISK)
"""