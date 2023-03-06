import socket
import sys
import threading
import math

def init(ip, port_):
    global client_socket
    global ip_server
    global port
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip_server = ip
    port = port_
    client_socket.connect((ip_server, port))

def str_to_bytes(strr): return [ord(l) for l in str(strr)]

def send_bytes(data):
    client_socket.send(bytes(data))

def send_message(name,msg):
    send_bytes(str_to_bytes(chr(10)+" "+name+"> "+msg))

def receive_byte():
    data = client_socket.recv(1)
    return data

def send_bytes_page(bts):
    bt = []
    for i in range(len(bts)*2):
        if i % 2 == 0: bt.append(bts[round(i/2)])
        else: bt.append(0)
    bt[-1]=255
    send_bytes(bt)

def get_bytes_page():
    run, dtype, output = True, 0, []
    while run:
        data = receive_byte()
        if data == b'\xff' and dtype == 1: run = False; return output
        if run:
            if dtype == 0: output.append(data)
            dtype = 1 - dtype
            
def send_command(code, args):
    send_bytes_page([code-256*math.floor(code/256),math.floor(code/256)]+list(args))
    return get_bytes_page()

def get_command():
    page = get_bytes_page()
    if len(page) > 2:
        ccode = page[0] + page[1]*256
        args = page[2:]
        return ccode, args
    return 0,[]
