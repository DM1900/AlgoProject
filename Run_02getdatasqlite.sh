#!/bin/sh

dt=$(date '+%d/%m/%Y %H:%M:%S');
cd /home/admin/AlgoProject
echo "$dt" >> ./logs/CronRun01.log 
echo "attempting to run getdata script from Cron" >> ./logs/CronRun01.log 
echo "/usr/bin/python /home/admin/AlgoProject/scripts/02_get_data_sqlite.py" >> ./logs/CronRun01.log 

/usr/bin/python3 /home/admin/AlgoProject/scripts/02_get_data_sqlite.py
