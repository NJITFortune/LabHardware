# This is a webserver that allows data to be read
# from the Pico W
# The password is 12345678
# The SSID should be customized for each device
import rp2
import network
import machine
import socket
import utime
import uos

ap = network.WLAN(network.AP_IF)
# BE SURE TO CONFIGURE EACH DEVICE TO HAVE A UNIQUE SSID
ap.config(essid="LiaVU_AP1")
ap.config(password="12345678")
ap.active(True)

# We are going to blink the LED for each web request
led = machine.Pin('LED', machine.Pin.OUT)
led.off()

def executeDEL():
    # Delete CSV files
    import uos
    directory_path = '/'
    allfiles = uos.listdir()
    csvfiles = [file for file in allfiles if file.endswith('.csv')]
    print(csvfiles)
    # Cycle to delete each CSV file
    for csvfile in csvfiles:
        try:
            uos.remove(csvfile)
            print("File deleted successfully.")
        except Exception as e:
            print("Error deleting file.")

# HTTP server with socket
addr = socket.getaddrinfo('192.168.4.1', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(10)

print('Listening on', addr)

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        led.on()
#        print('Client connected from', addr)
        r = str(cl.recv(1024))
        print(r)
        idx = r.find("POST")
        if (idx > -1):
            executeDEL()

        r = r[r.find("/"):]
        r = r[1:r.find(" ")]
        if (r == ""):
            r = "index.html"

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        f = open(r, 'r')
        while True:
            chunk = f.read(1024)  # Read the next 1KB chunk
            utime.sleep_ms(3)
            if not chunk:
                break
            cl.send(chunk)  # Send the next 1KB chunk
        cl.close()
        f.close()

        led.off()

    except OSError as e:
        cl.close()
        print('Connection closed')
        led.off()
