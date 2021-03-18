#!/usr/bin/env bash

dt=$(date '+%d/%m/%Y %H:%M:%S');
echo "$dt" >> ./AlgoProject/logs/CronRun01.log 
echo "attempting to run getdata script from Cron" >> ./AlgoProject/logs/CronRun01.log 
echo "/usr/bin/python ./AlgoProject/scripts/02_get_data_sqlite.py" >> ./AlgoProject/logs/CronRun01.log 

/usr/bin/python ./AlgoProject/scripts/02_get_data_sqlite.py
