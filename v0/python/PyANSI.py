from math import floor
import sys
import keyboard
import time
#print(end = "")
wins = []
slctd_win = 0
slctd_cols = [1,3]
char_with_density = "Ñ@#W$9876543210?!abc;:+=-,._ "
reverse_char_with_density = " _.,-=+:;cba!?0123456789$W#@Ñ"

console_enable = False
console_y0, console_y1 = 15, 25
console_x0, console_x1 = 0, 40
console_data = []
console_color = [0,255,1,3]
#console_listen = False
console_input = ""
reac = True
reac1 = False
on_console = False

console_message_got = True
console_message = ""

keys = ["1","2","3","4","5","6","7","8","9",
        "0","'","ì","q","w","e","r","t","y",
        "u","i","o","p","è","+","a","s","d",
        "f","g","h","j","k","l","ò","à","ù",
        "<","z","x","c","v","b","n","m",",",
        ".","-","*","/","-","backspace", "space"]

def writeout(tw): sys.stdout.write(tw)
def col_str(stri,colm, colb):
    #print("\033[{}m".format(41))
    return("\033[38;5;{};48;5;{}m{}\033[0m".format(colm, colb, stri))
def print_to(txt,c,r,cm,cb):
    writeout("\033[{};{}H".format(r,c))
    writeout(col_str(txt, cm, cb))
    print("")
def print_(txt,cm,cb):
    #writeout("\033[{};{}H".format(r,c))
    writeout(col_str(txt, cm, cb))
    #print("")
def set_sq(c,r,cb):
    writeout("\033[{};{}H".format(r,c*2+1))
    writeout(col_str("  ", 0, cb))
    print("")
def RGB(c):
    return(16+(floor(c[2])-6*floor(c[2]/6))+(floor(c[1])-6*floor(c[1]/6))*6+(floor(c[0]-6*floor(c[0]/6)))*36)
def RGBI(c):
    r,g,b,i=c
    r,g,b,i=r-2*floor(r/2),g-2*floor(g/2),b-2*floor(b/2),i-2*floor(i/2)
    return(int("0b"+str(i)+str(b)+str(g)+str(r),2))
def grayscale(c):
    return(c+232-24*floor(c/24))
def clear():
    writeout("\033[2J")
    writeout("\n")
def set_cur_visibility(sttmnt):
    if sttmnt:
        writeout("\033[?25h")
        print("")
    else:
        writeout("\033[25l")
        print("")
def new_line():
    writeout("\n")
def carriage_return():
    writeout("\r")
def tab():
    writeout("\t")
def new_page():
    writeout("\n")
def set_display_mode(mode):
    writeout("\033[={}h".format(mode))

class console():
    def get_input():
        global reac
        global console_input
        global reac1
        global console_message_got
        global console_message
        
        keys_p = []
        #reac = False
        for key in keys:
            if keyboard.is_pressed(key): keys_p.append(key)
        for i in range(len(keys_p)):
            if not(keys_p[i] == "backspace" or keys_p[i] == "space"):
                keys_p[i] = ord(keys_p[i])
                if keyboard.is_pressed("shift"):
                    keys_p[i] -= 32
            elif keys_p[i] == "space":
                keys_p[i] = ord(" ")
        if reac:
            for u in keys_p:
                if u == "backspace":
                    console_input = console_input[:len(console_input)-1]
                else:
                    console_input += chr(u)
            if keyboard.is_pressed("enter") and reac1:
                console.send("you", console_input)
                console_message, console_message_got = console_input, False
                console_input = ""
                reac1 = False
            if not keyboard.is_pressed("enter"): reac1 = True
        if len(keys_p) > 0: reac = False
        else: reac = True
        #console.send("e",str(keys_p))
        console.refresh()
    def enable(b):
        global console_enable
        console_enable = b
    def set_pos(x0,x1,y0, y1):
        global console_x0
        global console_x1
        global console_y0
        global console_y1
        for r in range(console_y1 - console_y0+1): print_to(" "*(console_x1-console_x0),0,r+console_y0-1,0,0)
        console_x0, console_x1, console_y0, console_y1 = x0, x1, y0, y1
        console.refresh()
    def set_color(col):
        global console_color
        console_color = list(col)
        console.refresh()
    def send(user,msg):
        global console_data
        console_data.append([user,msg])
        console.refresh()
    def refresh():
        for r in range(console_y1 - console_y0+1): print_to(" "*(console_x1-console_x0),console_x0,r+console_y0-1,console_color[0],console_color[1])
        print_to("Console:", console_x0, console_y0-1,console_color[2],console_color[1])
        to_print = []
        i=0
        for u in console_data:
            to_print.append(u)
            if i >= console_y1 - console_y0 - 2:
                del to_print[0]
            i+=1

        i=0
        for r in to_print:
            print_to(r[0]+"> "+r[1],console_x0,i+console_y0,console_color[0],console_color[1])
            i+=1

        crs = " "
        if round(time.time()*2) % 2 <= 0 and on_console: crs = "_"
        print_to(console_input+crs,console_x0,console_y1-2,console_color[3],console_color[1])
            
        
class windows():
    global wins
    def create_win(title,xp,yp,xs,ys,level):
        global wins
        taf = []
        for __ in range(ys):
            taf.append([])
            for __ in range(xs):
                taf[-1].append([0,0,0])
                
        wins.append([xp,yp,xs,ys,taf,title,level,len(wins)])
        return(len(wins)-1)
    def set_win_pos(win,pos):
        global wins
        if pos[0] != None:
            wins[win][0] = pos[0]
        if pos[1] != None:
            wins[win][1] = pos[1]
    def get_win_pos(win):
        global wins
        return(wins[win][0:1])
    def set_win_size(win,size):
        global wins
        taf = []
        for __ in range(ys):
            taf.append([])
            for __ in range(xs):
                taf[-1].append([" ",0,0])     
        if size[0] != None:
            wins[win][2] = size[0]
            wins[win][4] = taf
        if size[1] != None:
            wins[win][3] = size[1]
            wins[win][4] = taf
    def get_win_size(win):
        global wins
        return(wins[win][2:3])
    def get_win_data(win):
        global wins
        return(wins[win][4])
    def set_win_px(win,pos,char):
        global wins
        x,y = pos
        if x>=0 and y>=0 and x<wins[win][2] and y<wins[win][3]:
            wins[win][4][pos[1]][pos[0]] = char
    def render_wins():
        wins_u = []
        for __ in range(1000):
            wins_u.append(None)
        for u in wins:
            if u != None:
                wins_u[u[6]] = u
            
        clear()
        i=0
        for u in wins_u:
            if not u == None:
                if u[7] == slctd_win:
                    bc = slctd_cols[1]
                else:
                    bc = slctd_cols[0]
                print("")
                for x in range(u[2]+2):
                    print_to(" ",x+u[0]-1,u[1]-1,0,bc)
                    print_to(" ",x+u[0]-1,u[1]+u[3],0,bc)
                for y in range(u[3]):
                    print_to(" ",u[0]-1,u[1]+y,0,bc)
                    print_to(" ",u[0]+u[2],u[1]+y,0,bc)
                print_to(u[5],u[0]-1,u[1]-1,7-bc,bc)
                for y in range(u[3]):
                    for x in range(u[2]):
                        pxd = u[4][y][x]
                        print_to(pxd[0],x+u[0],y+u[1],pxd[1],pxd[2])
            i+=1

    def get_sel_win():
        return(slctd_win)
    def set_sel_win(win,get_front):
        global slctd_win
        global wins
        slctd_win = win
        if get_front:
            for i in range(len(wins)):
                if wins[i] != None:
                    wins[i][6] -= 1
            wins[win][6] = 0
                
    def set_sel_cols(c):
        global slctd_cols
        if c[0] != None:
            slctd_cols[0] = c[0]
        if c[1] != None:
            slctd_cols[1] = c[1]
    def del_win(win):
        global wins
        wins[win] = None
    def set_level(win,level):
        global wins
        wins[win][6] = level
    def get_level(win):
        return(wins[win][6])
        
    
    
