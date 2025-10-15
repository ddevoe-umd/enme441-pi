# Web interface for GPIO control using POST request
#
# Display a user-defined binary value on an LED bar


import RPi.GPIO as gpio
import threading
from time import sleep
import socket

from shifter import Shifter    # Use our custom Shifter class

dataPin, latchPin, clockPin = 23, 24, 25
sh = Shifter(dataPin, latchPin, clockPin)

def web_page(led_byte):
    # Define html code, with user text passed from the browser via POST request.
    # Note we cannot use an f-string here since there are HTML style definitions
    # that use the {} syntax!
    html = """
    <html><head><title>LED bar display</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <head>
    <style>
    html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
    h1{color: #0F3376; padding: 2vh;}
    p{font-size: 1.5rem;}
    .button{display: inline-block; background-color: #e7bd3b; border: none; border-radius: 4px; color: white;
                     padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
    </style>
    </head>
    <body>
    <h1>Web Server Test</h1> 
    <p>Byte value to display on LED bar:</p>
    <p><strong>""" + led_byte + """</strong> (base 10)</p>
    <p><strong>""" + bin(int(led_byte))[2:] + """</strong> (base 2)</p>
    <form action="/" method="POST">
      <p><input type="text" name="led_byte"> 
      <p><button type="submit" class="button" name="submit" value="">Display Byte</button></p>
    </form>
    </body>
    </html>
    """
    return bytes(html, 'utf-8')

# Helper function to extract key,value pairs of POST data
def parsePOSTdata(data):
    data_dict = {}
    idx = data.find('\r\n\r\n')+4
    data = data[idx:]
    data_pairs = data.split('&')
    for pair in data_pairs:
        key_val = pair.split('=')
        if len(key_val) == 2:
            data_dict[key_val[0]] = key_val[1]
    return data_dict


def serve_web_page():
    while True:
        print('Waiting for connection...')
        conn, (client_ip, client_port) = s.accept()     # blocking call
        print(f'Connection from {client_ip} on client port {client_port}')
        client_message = conn.recv(2048).decode('utf-8')
        print(f'Message from client:\n{client_message}')
        data_dict = parsePOSTdata(client_message)
        if 'led_byte' in data_dict.keys():   # make sure data was posted
            led_byte = data_dict["led_byte"]
        else:   # web page loading for 1st time so start with 0 for the LED byte
            led_byte = '0'
        conn.send(b'HTTP/1.1 200 OK\r\n')                  # status line
        conn.send(b'Content-Type: text/html\r\n')          # headers
        conn.send(b'Connection: close\r\n\r\n')   
        try:
            conn.sendall(web_page())                       # body
        finally:
            conn.close()

        sh.shiftByte(int(led_byte))    # display byte on the LED bar

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # pass IP addr & socket type
s.bind(('', 80))     # bind to given port
s.listen(3)          # up to 3 queued connections

webpageTread = threading.Thread(target=serve_web_page)
webpageTread.daemon = True
webpageTread.start()

# Do whatever we want while the web server runs in a separate thread:
try:
    while True:
        pass
except:
    print('Joining webpageTread')
    webpageTread.join()
    print('Closing socket')
    s.close()
