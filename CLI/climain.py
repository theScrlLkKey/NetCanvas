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
    output_str = ""
    for y in range(rows):
        for x in range(columns):
            output_str += f"\033[{y};{x}H"
            output_str += f"\033[{canvas[y][x]}m█"
        output_str += "\n"
    fast_output(output_str)


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
    global curs_x
    global curs_y
    # 1-9 here
    if key == Key.space:  # set color
        change_character(curs_y, curs_x, "34")
    elif key == Key.left:
        if curs_x > 1:
            curs_x -= 1
    elif key == Key.right:
        if curs_x < canvas_cols-1:
            curs_x += 1
    elif key == Key.up:
        if curs_y > 1:
            curs_y -= 1
    elif key == Key.down:
        if curs_y < canvas_rows-1:
            curs_y += 1
    elif key == Key.home:
        exit()


def start_key_press():
    with Listener(on_press=on_press) as listener:
        listener.join()


canvas = []
canvas_rows = 20  # get these from server too
canvas_cols = 50
generate_canvas(canvas_rows, canvas_cols)  # for testing, gen canvas. canvas should be made on server, and synced here. connect to server instead.
output_canvas(canvas_rows, canvas_cols)

fast_output("\033[0;0H")
curs_x = 1
curs_y = 1

key_press_sub = threading.Thread(target=start_key_press, args=())
key_press_sub.start()  # send updates here

while True:  # begin mainloop, get updates here
    output_canvas(canvas_rows, canvas_cols)   # instead of redrawing, only get changed pixels and update those
    fast_output(f"\033[{curs_y};{curs_x}H")  # update cursor pos
    time.sleep(0.1)
