import sys
import random
import time
from pynput.keyboard import Listener, Key
import threading
import _thread


# move with arrow keys, 1-9 to cycle colors, space to set color. return cursor when done updating from server
# all terminal stuff is offset by one, ensure canvas stays indexed at zero


def fast_output(text):
    sys.stdout.write(text)
    sys.stdout.flush()


def output_canvas(rows=40, columns=100):
    # update canvas using fastoutput, iterate through and parse into outputtable chars/locations
    output_str = ""
    for y in range(rows):
        for x in range(columns):
            output_str += f"\033[{y+1};{x+1}H"  # +1 because terminal indexes at 1 not 0
            output_str += f"\033[{canvas[y][x]}m█"
        output_str += "\n"
    fast_output(output_str)


def output_pixel(row=20, column=50, color="34", mode="solid"):  # use for cursor and also individual pixel update
    if mode == "solid":
        fast_output(f"\033[{row};{column}H\033[{canvas[row-1][column-1]}m█")  # -1 because terminal indexes at 1
    elif mode == "trans":
        fast_output(f"\033[{row};{column}H\033[{canvas[row-1][column-1]}m▒")
    elif mode == "str":
        fast_output(f"\033[{row};{column}H{str(color)}")


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


def change_character(row=20, column=50, color="34"):
    canvas[row][column] = color
    # pixel send code here


def on_press(key):
    global curs_x
    global curs_y
    # 1-9 here
    if key == Key.space:  # set color
        change_character(curs_y-1, curs_x-1, "34")  # -1 because curs_xy is terminal (index at 1) and canvas indexes at 0
    elif key == Key.left:
        if curs_x > 1:
            curs_x -= 1
    elif key == Key.right:
        if curs_x < canvas_cols:
            curs_x += 1
    elif key == Key.up:
        if curs_y > 1:
            curs_y -= 1
    elif key == Key.down:
        if curs_y < canvas_rows:
            curs_y += 1
    elif key == Key.home:
        fast_output("\033[2J ")
        _thread.interrupt_main()
        exit()
    output_pixel(1, canvas_cols+1, str(curs_y) + ", " + str(curs_x) + "  ", mode="str")


def start_key_press():
    with Listener(on_press=on_press) as listener:
        listener.join()


fast_output("\033[2J")

canvas = []
canvas_rows = 40  # get these from server too
canvas_cols = 100
generate_canvas(canvas_rows, canvas_cols)  # for testing, gen canvas. canvas should be made on server, and synced here. connect to server instead.
output_canvas(canvas_rows, canvas_cols)

fast_output("\033[1;1H")  # calib cursor location
curs_x = 1
curs_y = 1

output_pixel(canvas_rows+1, 1, "<keybinds>", mode="str")

key_press_sub = threading.Thread(target=start_key_press, args=())
key_press_sub.start()  # send updates here

while True:  # begin mainloop, get updates here
    output_canvas(canvas_rows, canvas_cols)   # get changed pixels and update those in canvas before redraw
    output_pixel(curs_y, curs_x, canvas[curs_y-1][curs_x-1], "trans")  # update virtual cursor, can't desync, -1 yk
    time.sleep(0.1)
