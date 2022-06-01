import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def debug(m):
    print(m, file=sys.stderr, flush=True)


class Checkpoint:
    def __init__(self, position, x, y):
        self.position = position
        self.x = x
        self.y = y
        self.distance_to_next = None

    def __str__(self):
        return(f"{self.position}, {self.x}, {self.y}, {self.distance_to_next}")

    def update_distance_to_next(self, next_x, next_y):
        x_delta = next_x - self.x
        y_delta = next_y - self.y
        self.distance_to_next = int(math.sqrt((x_delta**2) + (y_delta**2)))

def set_distance(source_checkpoint, target_checkpoint):
     source_checkpoint.update_distance_to_next(target_checkpoint.x, target_checkpoint.y)



checkpoints = []
active_target = None
course_known = False
boost_fired = False
# game loop
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]

    if len(checkpoints) == 0:
        checkpoints.append(Checkpoint(1,next_checkpoint_x, next_checkpoint_y))

    checkpoints_changed = checkpoints[-1].x != next_checkpoint_x or checkpoints[-1].y != next_checkpoint_y
    checkpoint_matches_known = (sum(c.x == next_checkpoint_x for c in checkpoints ) >0 and sum(c.y == next_checkpoint_y for c in checkpoints) > 0)
    add_checkpoint = checkpoints_changed and not checkpoint_matches_known
    debug(f"checkpoint changed {checkpoints_changed}, matches known {checkpoint_matches_known}")

    if add_checkpoint:
        active_target = Checkpoint(len(checkpoints)+1, next_checkpoint_x, next_checkpoint_y)
        checkpoints.append(active_target)
        for c in checkpoints:
            debug(c)
    elif len(checkpoints)> 1 and  checkpoints[0].x == next_checkpoint_x and checkpoints[0].y == next_checkpoint_y:
        debug("Map read executing analysis")
        for c_index in range(len(checkpoints)):
            set_distance(checkpoints[c_index - 1], checkpoints[c_index])
        for c in checkpoints:
            debug(c)
        course_known = True

    if(course_known):
        active_target = next((x for x in checkpoints if x.x == next_checkpoint_x and x.y == next_checkpoint_y ), None)
        lengths = [x.distance_to_next for x in checkpoints]
        lengths.insert(0, lengths.pop())

        debug(f"{lengths}, {lengths.index(max(lengths))+1}" )
        thrust = 0 if (next_checkpoint_angle > 90 or next_checkpoint_angle < -90) else 100
        if not boost_fired and active_target.position == lengths.index(max(lengths))+1:
            if next_checkpoint_angle > -10 and next_checkpoint_angle <10:
                debug("Fire boost")
                thrust = "BOOST"
                boost_fired = True
    else:
        thrust = 0 if (next_checkpoint_angle > 90 or next_checkpoint_angle < -90) else 100








    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)


    # You have to output the target position
    # followed by the power (0 <= thrust <= 100)
    # i.e.: "x y thrust"




    print(str(next_checkpoint_x) + " " + str(next_checkpoint_y) + f" {thrust}")
