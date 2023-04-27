from random import randint


def random_with_N_digits(n)->int:
    range_start = 10 ** (n - 1)
    range_end = (10**n) - 1
    return randint(range_start, range_end)


def generate_file_name()->str:
    """generates file unique file name"""
    return str(random_with_N_digits(5)) + ".csv"


class Logger:
    """Class for logging data to CSV"""

    def __init__(self, headers:str=None,file_name:str=None, path:str="/sd/",batch_size:int=1000,overwrite:bool=False,bin:bool=False)->None:
        if file_name:
            self.file_name = file_name # Uses user specified file name
        else:
            self.file_name = generate_file_name()  # Generates 5 digits unique name for each file
        self.file_path = path + self.file_name # Create path
        if overwrite:
            if bin:
                self.file = open(self.file_path, "wb") # open file in binary write mode (overwriting the previous file)
            else:
                self.file = open(self.file_path, "w") # open file in write mode (overwriting the previous file)
        else:
            if bin:
                self.file = open(self.file_path, "ab") # open file in append mode
            else:
                self.file = open(self.file_path, "a") # open file in append mode
        if headers:
            self.set_headers(headers) # Writing file headers
        self.index = 0 # Logged data counter
        self.batch_size = batch_size # Sets the data items to save at the time
        self.bin = bin

    def set_headers(self, header)->None:
        """Sets the headers for CSV file"""
        self.file.write(header)
        self.file.write("\r\n")

    def log_data(self, data)->None:
        """Logs the data to the current CSV file"""
        self.index += 1
        self.file.write(data)  # Logging data
        if self.bin:
            self.file.write(b"\r\n")  # new line
        else:
            self.file.write("\r\n")  # new line
        if self.index % self.batch_size == 0:
            self.save_recorded_data_to_file()

    def save_recorded_data_to_file(self)->None:  # fail safe for power lost - saving data on every self.batch_sizeth read
        self.file.close()
        if self.bin:
            self.file = open(self.file_path, "ab")
        else:
            self.file = open(self.file_path, "a")

    def close(self)->None:
        """Closing the file and destructing the object"""
        self.file.close()
        del self
