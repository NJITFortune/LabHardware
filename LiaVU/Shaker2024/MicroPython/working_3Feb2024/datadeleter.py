import os

# Specify the path to the directory containing CSV files
directory_path = '/'

allfiles = os.listdir()
csvfiles = [file for file in allfiles if file.endswith('.csv')]
print(csvfiles)

# Delete each CSV file
for csvfile in csvfiles:
    try:
        os.remove(csvfile)
        print("File deleted successfully.")
    except Exception as e:
        print("Error deleting file.")
