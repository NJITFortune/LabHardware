import sdcardio
import storage
from configs import SD_CS, SD_SPI
import sys

sdcard = sdcardio.SDCard(SD_SPI, SD_CS)  # Creating SD card instance
vfs = storage.VfsFat(sdcard)  # set storage type
storage.mount(vfs, "/sd")  # mounting the SD card so it can be accessed system wide
sys.path.append("/sd")
