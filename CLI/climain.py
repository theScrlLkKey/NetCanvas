import sys
import random
import time
from pynput.keyboard import Listener, Key
import threading


# move with arrow keys, 1-9 to cycle colors, space to set color. return cursor when done updating from server


def fast_output(text):
    sys.stdout.write(text)
    sys.stdout.flush()


def output_canvas(rows=40, columns=100):
    # update canvas using fastoutput, iterate through and parse into outputtable chars/locations
    fast_output("\033[s")
    output_str = ""
    for y in range(rows):
        for x in range(columns):
            output_str += f"\033[{y};{x}H"
            output_str += f"\033[{canvas[y][x]}m█"
        output_str += "\n"
    fast_output(output_str)
    fast_output("\033[39m")
    fast_output("\033[u")


def generate_canvas(rows=40, columns=100):
    # setup canvas, fill with blanks, 40x100 canvas for now
    global canvas
    for y in range(rows):
        row = []
        for x in range(columns):
            row.append("90")
        canvas.append(row)


def randomize_canvas(rows=40, columns=100):
    # rand color canvas
    global canvas
    for y in range(rows):
        for x in range(columns):
            colors = [30,31,32,33,34,35,36,37,90,91,92,93,94,95,96,97]
            canvas[y][x] = str(colors[random.randint(0, 15)])


def change_character(row=20, column=50, value="34"):
    canvas[row][column] = value


def on_press(key):
    # 1-9 here
    if key == Key.space:  # set color
        pass
    elif key == Key.left:
        fast_output('\033[1D')
    elif key == Key.right:
        fast_output('\033[1C')
    elif key == Key.up:
        fast_output('\033[1A')
    elif key == Key.down:
        fast_output('\033[1B')
    elif key == Key.shift:
        exit()


def start_key_press():
    with Listener(on_press=on_press) as listener:
        listener.join()


canvas = []
generate_canvas()  # for testing, gen canvas. canvas should be made on server, and synced here. connect to server instead.

key_press_sub = threading.Thread(target=start_key_press, args=())
key_press_sub.start()  # send updates here

while True:  # begin mainloop, get updates here
    output_canvas()   # instead of redrawing, only get changed pixels and update those
    time.sleep(0.5)
