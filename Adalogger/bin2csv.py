import struct
import csv

def convert_binary_to_csv(binary_filename, csv_filename):
    """Reads a binary log file and saves the data as a CSV file."""
    try:
        with open(binary_filename, "rb") as bin_file, open(csv_filename, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Time_us", "ADC_Value"])  # CSV Header

            while chunk := bin_file.read(6):  # Read 6 bytes per sample
                timestamp, value = struct.unpack("<IH", chunk)
                csv_writer.writerow([timestamp, value])

        print(f"Conversion complete: {csv_filename}")
    except Exception as e:
        print("Error:", e)

# Convert log_000.bin to log_000.csv
convert_binary_to_csv("log_000.bin", "log_000.csv")

