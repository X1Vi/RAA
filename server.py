import socket
import threading
import json
import time
import os

HOST = 'localhost'
PORT = 8000

device_map = {}
device_count = 0

s : socket = None


def listen():
    global device_count
    print("Listening")
    global s 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()

    while True:
        conn, addr = s.accept()
        print(f"Connected successfully: {addr}")
        device_count += 1
        device_map[addr] = {"socket": conn, "index": device_count}

def create_listen_thread():
    listen_thread = threading.Thread(target=listen)
    listen_thread.start()

def display_connected_sockets():
    for key in device_map:
        print(key, device_map[key]['socket'], device_map[key]['index'])

def take_input_and_send_message():
    while True:
        if len(device_map) == 0:
            time.sleep(20)
            print("No connected devices")
            continue

        display_connected_sockets()
        try:
            index = int(input("Enter index of the socket to send commands to: "))
       
            getSocket = find_socket_by_index(index)

            commands = []
            command_quantity = int(input("Enter how many commands you want to enter? "))
            for _ in range(command_quantity):
                command = input("Enter command: ")
                parse_commands(command, commands)
            json_commands = json.dumps(commands)
            if getSocket is None:
                take_input_and_send_message()
            getSocket.send(json_commands.encode())
        except ValueError:
            take_input_and_send_message()
            
def listenForMessagesSingularThread():
    time.sleep(0.4)
    key : None
    while True:
        try:
            for key, device in device_map.items():
                key = key
                data = device['socket'].recv(1024)
                data = {"data": data, "key": key, "device": device}
                store_data_in_file(data_str=str(data))
        except Exception as e:
            device_map.pop(key)
            listenForMessagesSingularThread()
            




def store_data_in_file(data_str):
   f = open("demofile2.txt", "a")
   f.write(f"{data_str} \n")
   f.close()


def runListenMessageThread():
    threading.Thread(target=listenForMessagesSingularThread).start()

def find_socket_by_index(index: int):
    for key in device_map:
        if device_map[key]['index'] == index:
            return device_map[key]['socket']

def parse_commands(subcommand: str, commands: list):
    command_arr = subcommand.split(' ')
    commands.append(command_arr)

def main():
    create_listen_thread()
    runListenMessageThread()
    send_message_thread = threading.Thread(target=take_input_and_send_message)
    send_message_thread.start()

if __name__ == "__main__":
    try:
        main()
    except Exception as  e:
        main()