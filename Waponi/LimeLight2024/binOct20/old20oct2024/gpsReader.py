#!/usr/bin/python

import serial
import re
import csv
from datetime import datetime

def parse_rmc_sentence(sentence):
    # Example RMC sentence: $GNRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A
    parts = sentence.split(',')
    
    if parts[0] == "$GNRMC" and parts[2] == 'A':  # 'A' indicates data is valid
        time_utc = parts[1]
        latitude = parts[3]
        latitude_direction = parts[4]
        longitude = parts[5]
        longitude_direction = parts[6]
        date = parts[9]

        # Convert latitude and longitude to decimal format
        latitude_decimal = convert_to_decimal(latitude, latitude_direction)
        longitude_decimal = convert_to_decimal(longitude, longitude_direction)

        # Format date and time to readable formats
        formatted_time = format_time(time_utc)
        formatted_date = format_date(date)

        return formatted_date, formatted_time, latitude_decimal, longitude_decimal
    return None

def convert_to_decimal(coord, direction):
    # Convert NMEA coordinates to decimal format
    if not coord:
        return None
    degrees = int(coord[:2])
    minutes = float(coord[2:])
    decimal_coord = degrees + minutes / 60.0

    if direction in ['S', 'W']:
        decimal_coord = -decimal_coord

    return decimal_coord

def format_time(time_str):
    # Format the time from HHMMSS to HH:MM:SS
    if time_str and len(time_str) >= 6:
        return f"{time_str[:2]}:{time_str[2:4]}:{time_str[4:6]}"
    return None

def format_date(date_str):
    # Format the date from DDMMYY to YYYY-MM-DD
    if date_str and len(date_str) == 6:
        day = date_str[:2]
        month = date_str[2:4]
        year = "20" + date_str[4:6]  # Assuming 21st century dates
        return f"{year}-{month}-{day}"
    return None

def append_to_csv(data, filename='gps_data.csv'):
    # Append the data to the CSV file
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def read_nmea_data(port='/dev/ttyAMA0', baudrate=9600):
    try:
        with serial.Serial(port, baudrate, timeout=1) as ser:
            while True:
                line = ser.readline().decode('ascii', errors='replace').strip()
                if line.startswith("$GNRMC"):
                    parsed_data = parse_rmc_sentence(line)
                    if parsed_data:
                        date, time_utc, latitude, longitude = parsed_data
                        print(f"Date: {date}, Time (UTC): {time_utc}, Latitude: {latitude}, Longitude: {longitude}")
                        
                        # Append to CSV
                        append_to_csv([date, time_utc, latitude, longitude])
    except serial.SerialException as e:
        print(f"Serial exception: {e}")

if __name__ == "__main__":
    # Write header to the CSV file if starting fresh
    with open('gps_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Time (UTC)', 'Latitude', 'Longitude'])
    
    read_nmea_data()

