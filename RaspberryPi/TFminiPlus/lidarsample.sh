#!/bin/sh
cd /home/waponi/lidardata
date >> /home/waponi/lidardata/log.txt
libcamera-still -n --datetime --autofocus-range=macro
ls -tlh *.jpg | head -1 >> /home/waponi/lidardata/log.txt
sleep 1
timeout 50 python /home/waponi/LiDAR/V4/main.py
sleep 1
ls -tlh *.csv | head -1 >> /home/waponi/lidardata/log.txt
libcamera-still -n --datetime --autofocus-range=macro
sleep 1
ls -tlh *.jpg | head -1 >> /home/waponi/lidardata/log.txt
latestcsv=`ls -t /home/waponi/lidardata/*.csv | head -1`
cp $latestcsv /home/waponi/lidardata/data.csv
/home/waponi/bin/pysender.py
