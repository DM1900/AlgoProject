import csv
from datetime import datetime, timedelta

# get csv files
YEAR = datetime.now().strftime("%Y") # get current year
CSVFILE = 'scripts/AlphaVantage/data/stock_{}.csv'.format(YEAR)
LASTYEAR = int(YEAR) - 1
CSVFILE_LASTYEAR = 'scripts/AlphaVantage/data/stock_{}.csv'.format(LASTYEAR)

Date = datetime.now().strftime("%d/%m/%Y") # "%Y%m%d-%H%M") # input("Enter the date (dd/mm/yyyy): ") 

def import_csv(csvfilename):
    global csvdata
    global data
    csvdata = []
    with open(csvfilename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_index = 0
        for row in csv_reader:
            if row:  # avoid blank lines
                row_index += 1
                columns = [str(row_index), row[0], row[1], row[2], row[3], row[4], row[5], row[6]]
                csvdata.append(columns)
    data = csvdata[-1]

def enter_data():
    print("Enter data for {}".format(Date))
    TotalValue = float(input("Enter total account value: "))
    PieValue = float(input("Enter Pie value: "))
    #Investment = input("Enter invested amount: ") 
    tmp = float(data[4])
    print("Invested amount is €{}, any change?: ".format(tmp))
    Investment = float(input("Enter additional ammount here or leave blank: ") or "0")
    Investment = float(tmp) + Investment
    tmp = float(data[5])
    print("Pie Invested amount is €{}, any change?: ".format(tmp))
    PieInvestment = float(input("Enter additional ammount here or leave blank: ") or "0")
    PieInvestment = tmp + PieInvestment
    tmp = data[6]
    Realised = input("Enter Realised value (current value €{}): ".format(tmp))
    if Realised == "":
        Realised = tmp
    tmp = data[7]
    Dividend = input("Enter Dividend value received (current value €{}): ".format(tmp))
    if Dividend == "":
        Dividend = tmp
    print(Date,TotalValue,PieValue,Investment,PieInvestment,Realised,Dividend)
    with open(CSVFILE, mode='a') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([Date,TotalValue,PieValue,Investment,PieInvestment,Realised,Dividend])

import_csv(CSVFILE)

if Date in data:
    CONTINUE = input("Date ({}) already assigned, do you wish to continue? (y or n)".format(Date)) 
    if CONTINUE == "y":
        enter_data()
    else:
        print("No action taken, end of script")
        print("Existing data: {}".format(data))
else:
    enter_data()

#import_csv(CSVFILE_LASTYEAR)
#print(data)

# end