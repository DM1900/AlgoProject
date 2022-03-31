#!/bin/sh

dt=$(date '+%d/%m/%Y %H:%M:%S');
cd /home/ec2-user/AlgoProject
echo "$dt" >> ./logs/CronRun01.log 
echo "attempting to run getdata script from Cron" >> ./logs/CronRun01.log 
echo "/usr/bin/python /home/derek/AlgoProject/scripts/02_get_data_sqlite.py" >> ./logs/CronRun01.log 

#/usr/bin/python3 /home/ec2-user/AlgoProject/scripts/01_get_data_singleticker.py

/usr/bin/python3 /home/ec2-user/AlgoProject/scripts/02_get_data_sqlite.py

