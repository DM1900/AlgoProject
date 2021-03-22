#!/usr/bin/env bash

dt=$(date '+%d/%m/%Y %H:%M:%S');
echo "$dt" >> ./logs/CronRun01.log 
echo "attempting to run getdata script from Cron" >> ./logs/CronRun01.log 
echo "/usr/bin/python ./scripts/02_get_data_sqlite.py" >> ./logs/CronRun01.log 

/usr/bin/python ./scripts/02_get_data_sqlite.py