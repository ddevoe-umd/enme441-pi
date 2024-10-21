# webserver.py
#
# Web server via sockets, see:
# https://docs.micropython.org/en/latest/esp8266/tutorial/network_tcp.html
#
# When contacted by a client (web browser), send a web page
# displaying the states of selected GPIO pins.

import socket
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

pins = (19,21,22,23,25,26,32,33)
for p in pins: GPIO.setup(p, GPIO.IN) 

# Generate HTML for the web page:
def web_page():
    rows = [f'<tr><td>{str(p)}</td><td>{p.value()}</td></tr>' for p in pins]
    html = f"""
        <html>
        <head> <title>GPIO Pins</title> </head>
        <body> <h1>Pin States</h1>
        <table border="1"> <tr><th>Pin</th><th>Value</th></tr>
        {'\n'.join(rows)}
        </table>
        </body>
        </html>
        """
    print(html)
    return (bytes(html,'utf-8'))   # convert html string to UTF-8 bytes object
    
addr = socket.getaddrinfo('', 80)[-1][-1][0]

# Serve the web page to a client on connection:
def serve_web_page():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # pass IP addr & port number
    s.bind(('', 80))
    s.listen(3)  # up to 3 queued connections
    while True:
        print('Waiting for connection...')
        conn, addr = s.accept()
        print(f'Connection from {addr}')
        conn.send(b'HTTP/1.0 200 OK\n')         # status line 
        conn.send(b'Content-type: text/html\n') # header (content type)
        conn.send(b'Connection: close\r\n\r\n') # header (tell client to close at end)
        conn.sendall(web_page())               # body
        conn.close()

serve_web_page()
