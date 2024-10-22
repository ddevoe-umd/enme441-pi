# Web interface for GPIO control using a GET request
#
# Use a simple HTML button to allow user to turn a GPIO output on/off

from RPi import GPIO
from time import sleep
import socket

led = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)

data = ""

def web_page():
    if GPIO.input(led):
        gpio_state="ON"
    else:
        gpio_state="OFF"

    # Define html code, with button state passed to the browser via GET request
    # (either "/?led=on" or "/?led=off").
    #
    # Note we cannot use an f-string here since there are HTML style definitions
    # that use the {} syntax!
    html = """
    <html><head><title>Web Server Test</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,">
    <style>
    html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
    h1{color: #0F3376; padding: 2vh;}
    p{font-size: 1.5rem;}
    .button{display: inline-block; background-color: #e7bd3b; border: none; border-radius: 4px; color: white;
                     padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
    .button2{background-color: #4286f4;}
    </style>
    </head>
    <body>
    <h1>Web Server Test</h1>
    <p>GPIO state: <strong>""" + gpio_state + """</strong></p>
    <form action="/" method="GET">
    <p><button class="button" type="submit" name="button_on">ON</button></p>
    <p><button class="button button2" type="submit" name="button_off">OFF</button></p>
    </form>
    </body>
    </html>
    """
    return html.encode('utf-8')

def serve_web_page():
    try:
        while True:
            print('Waiting for connection...')
            conn, addr = s.accept()      # blocking call -- code pauses until connection
            print(f'Connection from {addr}')
            data = conn.recv(1024).decode('utf-8')  # specify buffer size (max data to be received)
            print('\nGET request recieved:\n--------------------')
            print(data)
            data = data[data.find('GET')+6 : data.find('HTTP')]  # slice the GET data
            if len(data) > 0:   # check that GET message was sent
                if "button_on" in data:
                    GPIO.output(led, 1)
                if "button_off" in data:
                    GPIO.output(led, 0)
            conn.send(b'HTTP/1.1 200 OK\n')             # status line
            conn.send(b'Content-Type: text/html\n')     # headers
            conn.send(b'Connection: close\r\n\r\n')
            conn.sendall(web_page())                   # body
            conn.close()
    except Exception as e:
        print(e)
    conn.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP-IP socket
s.bind(('', 80))
s.listen(3)

serve_web_page()
