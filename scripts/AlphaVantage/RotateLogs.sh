#!/bin/bash
# move old log and csv files

# move log files
mv logs/*.log logs/2021/

# move csv files
mv scripts/AlphaVantage/output/*.csv scripts/AlphaVantage/output/2021/

# end