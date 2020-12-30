print("Load Libraries")
# Load the Pandas libraries with alias 'pd' 
import pandas as pd 
import numpy as np
from IPython.display import HTML 
# Read data from file 'filename.csv' 
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later) 
FILE = "output/RSIData_Extended_20201214.csv"
print(FILE)
df = pd.read_csv(FILE) 
# Preview the first 5 lines of the loaded data 

#print(df.tail())

print("html")

html = df.to_html(classes='table table-striped')
  
# write html to file 
HTMLFILE = "output/htmloutput.html"
text_file = open(HTMLFILE, "w") 
text_file.write(html) 
text_file.close() 

