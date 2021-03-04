#!/usr/bin/env bash

dt=$(date '+%d/%m/%Y %H:%M:%S');
echo "$dt" >> /home/admin/AlgoProject/scripts/AlphaVantage/CronRun01.log 
echo "attempting to run getdata script from Cron" >> /home/admin/AlgoProject/scripts/AlphaVantage/CronRun01.log 
echo "/usr/bin/python /home/admin/AlgoProject/scripts/AlphaVantage/02_get_data_sqlite.py" >> /home/admin/AlgoProject/scripts/AlphaVantage/CronRun01.log 

python /home/admin/AlgoProject/scripts/AlphaVantage/02_get_data_sqlite.py
