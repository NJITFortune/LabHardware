import rp2
import network
import machine
import socket

ap = network.WLAN(network.AP_IF)
ap.config(essid="LiaVU_AP")
ap.config(password="12345678")
ap.active(True)

led = machine.Pin('LED', machine.Pin.OUT)
led.off()

def get_file(file_name):
    with open(file_name, 'rb') as file:
        return file.read()

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
#        print(r)
        r = r[r.find("/"):]
        r = r[1:r.find(" ")]
        if (r == ""):
            r = "index.html"

#        print(r)
        
        response = get_file(r)
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        led.off()
        
    except OSError as e:
        cl.close()
#        print('Connection closed')
        led.off()
