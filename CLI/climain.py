import sys
import random
import time

# move with arrow keys, 1-9 to cycle colors, space to set color. return cursor when done updating from server


def fast_output(text):
    sys.stdout.write(text)
    sys.stdout.flush()


def output_canvas(rows=40, columns=100):
    # update canvas using fastoutput, iterate through and parse into outputtable chars/locations
    output_str = ""
    for y in range(rows):
        for x in range(columns):
            fast_output(f"\033[{y};{x}H")
            fast_output(f"\033[{canvas[y][x]}m█")
        fast_output("\n")
    fast_output("\033[39m")


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
            canvas[y][x] = str(random.randint(90, 97))


def change_character(row=20, column=50, value="34"):
    canvas[row][column] = value


canvas = []
generate_canvas()  # for testing, gen canvas. canvas should be made on server, and synced here. connect to server instead.

while True:  # begin mainloop
    randomize_canvas()
    output_canvas()   # instead of redrawing, only get changed pixels and update those
    # time.sleep(0.1)
