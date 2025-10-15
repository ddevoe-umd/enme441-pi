# webserver.py
#
# Web server via sockets.
#
# When contacted by a client (web browser), send a web page
# displaying the states of selected GPIO pins.
#
# Must run as sudo to access port 80.  
#
# Port 8080 is a non-privileged alternative to port 80 that can
# be used to avoid the need for sudo, if desired.

import socket
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

pins = (19,21,22,23,25,26,32,33)
for p in pins: GPIO.setup(p, GPIO.IN) 

# Generate HTML for the web page:
def web_page():
    rows = [f'<tr><td>{p}</td><td>{GPIO.input(p)}</td></tr>' for p in pins]
    html = """
        <html>
        <head> <title>GPIO Pins</title> </head>
        <body> <h1>Pin States</h1>
        <table border="1"> <tr><th>Pin</th><th>Value</th></tr>
        """ + '\n'.join(rows) + """
        </table>
        </body>
        </html>
        """
    print(html)
    return (bytes(html,'utf-8'))   # convert html string to UTF-8 bytes object
     
# Serve the web page to a client on connection:
def serve_web_page():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP-IP socket
    s.bind(('', 80))
    s.listen(3)  # up to 3 queued connections
    while True:
        print('Waiting for connection...')
        conn, (client_ip, client_port) = s.accept()     # blocking call
        print(f'Connection from {client_ip}')   
        conn.send(b'HTTP/1.1 200 OK\n')         # status line 
        conn.send(b'Content-type: text/html\n') # header (content type)
        conn.send(b'Connection: close\r\n\r\n') # header (tell client to close at end)
        conn.sendall(web_page())                # body
        conn.close()

serve_web_page()
