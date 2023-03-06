import SimpleCustomClient as sc
import sys
import time
import PyANSI as pa
import keyboard as kbb
import threading

keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', "'", 'ì',
        'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'è', '+',
        'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ò', 'à', 'ù',
        '<', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '-', '<',
        '*',
        'shift','tab','ctrl','alt','enter','altgr','backspace','escape','space',
        'up_arrow','left_arrow','down_arrow','right_arrow']

def get_input(message):
    inp, reac = "", False
    print("")
    pa.print_("\r"+" "*(len(message)+len(inp)+5),255,0)
    pa.print_("\r"+message+inp,255,0)
    while kbb.is_pressed("enter"): pass
    while not kbb.is_pressed("enter"):
        ap = False
        if not kbb.is_pressed('enter'):
            for u in keys:
                if kbb.is_pressed(u):
                    if reac:
                        if u == 'backspace': inp = inp[:-1]
                        elif len(u)==1: inp += u
                        elif u == "space": u+=" "
                    ap,reac = True, False
                    pa.print_("\r"+" "*(len(message)+len(inp)+5),255,0)
                    pa.print_("\r"+message+inp,255,0)
        if not ap:
            reac = True
    return inp

print("PRT online terminal v.0 by PrililaCreatore")
ip = get_input("ip: ")
port = get_input("port: ")

#ip,port="",""
print("")
print("\nAttemping connection to",ip+":"+port)
time.sleep(0.1)
sc.init(ip, int(port))
print("Connection estabilished with",ip+":"+port)
#time.sleep(1)
#sc.receive_byte()
#data = sc.receive_byte()
#print(data)

def send_keys():
    global run
    global ts
    reac = True
    specials = ['shift','tab','ctrl','alt','altgr']
    while run:
        #time.sleep(0.2)
        if run:
            keys_pressed = []
            prsd = False
            for ik in range(len(keys)):
                if kbb.is_pressed(keys[ik]):
                    if not keys[ik] in specials:
                        if reac: keys_pressed.append(ik)
                        prsd = True
                    
            if not prsd: reac = True
            else: reac = False
            #print(keys_pressed)
            if len(keys_pressed)>0 and prsd:
                for u in specials:
                    if kbb.is_pressed(u): keys_pressed.append(keys.index(u))
                sc.send_bytes_page(keys_pressed)

run = True
ts = []

key_send = threading.Thread(target=send_keys, args=())
key_send.start()

writebuff = ""
pa.clear()
while run:
    try: data = sc.get_bytes_page()
    except Exception as e:
        pa.clear()
        pa.print_to(str(e),1,0,0,pa.RGB((5,0,0)))
        run = False
    if run:
        msg = [ord(B) for B in data]
        if msg[0] == 1:
            charr = [chr(msg[i]) for i in range(1,len(msg))]
            string = ""
            for u in charr: string+=u
            #print(charr)
            print(string, flush=True, end='')
    

while not kbb.is_pressed('enter'): pass
