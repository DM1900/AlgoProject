import pandas as pd
my_csv = pd.read_csv('Screener Results_20201020.csv')
column = my_csv.Symbol
print(column)


CSV_FILE = 'output/test1111.csv'

column.to_csv(CSV_FILE,index=False)