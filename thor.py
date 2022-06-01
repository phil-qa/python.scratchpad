import sys
import math

def debug(m): print(m, file=sys.stderr, flush=True)

lx, ly, tx, ty = [int(i) for i in input().split()]

def locate_target(lx, ly, tx, ty):
    target_right = None
    target_below = None
    diff_x = tx - lx
    diff_y = ty - ly
    if diff_x > 0:
        target_right = False
    elif diff_x < 0:
        target_right = True
    if diff_y < 0:
        target_below = True
    elif diff_y > 0:
        target_below = False
    angle = None

    if target_right != None and target_below != None:
        angle = math.atan(diff_x / diff_y) * 180
        if angle < 0: angle *= -1
    return [target_right, target_below, angle]


def next_direction(parameters):
    target_right = parameters[0]
    target_below = parameters[1]
    angle = parameters[2]

    direction = ""

    debug(f"{target_right}, {target_below}, {angle}")
    if target_below:
        direction = "S"
    elif target_below == False:
        direction = "N"
    if target_right:
        direction += "E"
    elif target_right == False:
        direction += "W"


    return (direction)


while True:
    remaining_turns = int(input())
    next_step = next_direction(locate_target(lx, ly, tx, ty))
    if "N" in next_step:
        ty -= 1
    if "E" in next_step:
        tx += 1
    if "S" in next_step:
        ty += 1
    if "W" in next_step:
        tx -= 1
    print(next_step)
