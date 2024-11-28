import sys
import random  # colored static sometime


def fast_output(text):
    sys.stdout.write(text)
    sys.stdout.flush()


def output_canvas():
    # update canvas using fastoutput, iterate through and parse into outputtable chars/locations
    for y in range(40):
        for x in range(100):
            fast_output(f"\033[{y};{x}H")
            fast_output(f"\033[{canvas[y][x]}m█")
        fast_output("\n")


# setup canvas, fill with blanks, 40x100 canvas for now, replace with var in actual code, make init_canvas()
canvas = []
for y in range(40):
    row = []
    for x in range(100):
        row.append("30")
    canvas.append(row)

print(canvas)
output_canvas()

# rand color canvas
for y in range(40):
    for x in range(100):
        canvas[y][x] = str(random.randint(90, 97))

print(canvas)
output_canvas()
