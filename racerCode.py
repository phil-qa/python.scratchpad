import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
'''
Intelligence gathering 
speed of pod - arbitary value derived from the distance from last sample - done
rate toward target - speed toward next checkpoint - done
implement telemetry
improve speed function
implement will_hit_target - iteration 1:  will the pod be facing the target by the time it reaches it given that we know distance and ticks and acceleration is about 25 per
tich and the turn rate is 17 degrees a tick the algorithm would be the distance to the target and the starting speed and angle
'''

def debug(m):
    print(m, file=sys.stderr, flush=True)

def calculate_distance(reference_x, reference_y, target_x, target_y):
    x_delta = target_x - reference_x
    y_delta = target_y - reference_y
    return int(math.sqrt((x_delta ** 2) + (y_delta ** 2)))

def will_pod_hit(distance_to_target, start_speed, angle_to_target):
    # light weight check assumptions, accelleration is constant 25 per tick, max speed is 650, turnRate is 17 degrees per tick
    ticks_to_target = 1
    projection_speed = start_speed
    while distance_to_target > 0:
        distance_to_target -= projection_speed
        projection_speed += 25
        if projection_speed > 650:
            projection_speed = 650
        ticks_to_target += 1 
    angle_turned = ticks_to_target * 17
    debug(f"Distance to target {distance_to_target}, anticipated turns to arrive {ticks_to_target}, required angle {angle_to_target}, available_angle {angle_turned} ")
    if angle_turned >= angle_to_target:
        return True
    else: 
        return False



class Checkpoint:
    def __init__(self, position, x, y):
        self.position = position
        self.x = x
        self.y = y
        self.distance_to_next = None

    def __str__(self):
        return(f"{self.position}, {self.x}, {self.y}, {self.distance_to_next}")

    def update_distance_to_next(self, next_x, next_y):
        self.distance_to_next = calculate_distance(self.x,self.y, next_x, next_y)

class Telemetry:
    def __init__(self):
     self.readings = []
    
    def add_reading(self,iteration, target_id,  x, y, angle_to_target, distance_to_target):
        rec = {}
        rec["iteration"] = iteration
        rec["target"] = target_id
        rec["ship_x"] = x
        rec["ship_y"] = y
        rec["angle_to_target"] = angle_to_target
        rec["distance_to_target"] = distance_to_target
        debug(rec)
        self.readings.append(rec)

       

    def __str__(self):
        report = ""
        for x in self.readings:
            line = f"{x['iteration']}, {x['target']}\n"
            report += line
        return report


class Pod:
    '''
    Independent analysis shows that the pod max acceleration is over 5 turns then slow but continual, max speed in 24 turns with no influence from non linear momentum
    the pod turns 17 degrees per tick,  


    '''
    def __init__(self, identity, start_x, start_y, distance_to_target):
        self.identity = identity
        self.x = start_x
        self.y = start_y
        self.x_momentum = 0
        self.y_momentum = 0
        self.speed = 0
        self.target_distance = distance_to_target
        self.speed_to_target = 0
        self.tel = Telemetry()
        self.race_iterator = 0
        self.target_id = 1


    def update_position(self, target_id, new_x, new_y, distance_to_target, angle_to_target):
        self.race_iterator+=1
        self.tel.add_reading(self.race_iterator, target_id, new_x, new_y, angle_to_target, distance_to_target)
        self.update_speed(new_x, new_y)
        self.speed_to_target = self.target_distance - distance_to_target
        self.x = new_x
        self.y = new_y
        self.target_distance = distance_to_target
        

    def update_speed(self, new_x, new_y):
        self.x_momentum = (self.x - new_x)*-1
        self.y_momentum = (self.y - new_y)*-1
        self.speed = calculate_distance(self.x,self.y,new_x,new_y)
    
    


    def __str__(self):
        return(f"pod {self.identity} Speed {self.speed} Speed to target {self.speed_to_target}")


def set_distance(source_checkpoint, target_checkpoint):
     source_checkpoint.update_distance_to_next(target_checkpoint.x, target_checkpoint.y)

def is_add_checkpoint(checkpoints, next_checkpoint_x, next_checkpoint_y):
    checkpoints_changed = checkpoints[-1].x != next_checkpoint_x or checkpoints[-1].y != next_checkpoint_y
    checkpoint_matches_known = (sum(c.x == next_checkpoint_x for c in checkpoints ) >0 and sum(c.y == next_checkpoint_y for c in checkpoints) > 0)
    return checkpoints_changed and not checkpoint_matches_known

def is_map_conditions_met(checkpoints, next_checkpoint_x, next_checkpoint_y ):
    next_checkpoint_is_first = len(checkpoints)> 1 and  checkpoints[0].x == next_checkpoint_x and checkpoints[0].y == next_checkpoint_y
    return next_checkpoint_is_first


    
checkpoints = []
pods = []
active_target = None
course_known = False
boost_fired = False
lap = 1
lapped = False
# game loop
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]

    

    if len(checkpoints) == 0: #no checkpoints add one
        checkpoints.append(Checkpoint(1,next_checkpoint_x, next_checkpoint_y))
        pods.append(Pod("Player", x, y, next_checkpoint_dist))

    active_target = (next((x for x in checkpoints if x.x == next_checkpoint_x and x.y == next_checkpoint_y ), None))

    if is_add_checkpoint(checkpoints, next_checkpoint_x, next_checkpoint_y):
        active_target = Checkpoint(len(checkpoints)+1, next_checkpoint_x, next_checkpoint_y)
        checkpoints.append(active_target)
        for c in checkpoints:
            debug(c)
    
    elif is_map_conditions_met(checkpoints, next_checkpoint_x, next_checkpoint_y):
        debug("Map read executing analysis")
        for c_index in range(len(checkpoints)):
            set_distance(checkpoints[c_index - 1], checkpoints[c_index])
        for c in checkpoints:
            debug(c)
        course_known = True
    
    if pods[0].x != x or pods[0].y != y: #is the pod in a different positon to last time
        pods[0].update_position(active_target.position, x,y,next_checkpoint_dist, next_checkpoint_angle)
        debug(f"{pods[0]}")
    


    

    if(course_known):
        last_target = active_target
        active_target = (next((x for x in checkpoints if x.x == next_checkpoint_x and x.y == next_checkpoint_y ), None))
        if active_target.position != last_target.position and active_target.position == 1:
            lap +=1 
            debug(f"Lap changed, lap {lap}")
            if lap == 2:
                debug(pods[0].tel)
        lengths = [x.distance_to_next for x in checkpoints]
        lengths.insert(0, lengths.pop())
        debug(f"{lengths}, {lengths.index(max(lengths))+1}" )

        thrust = 0 if (next_checkpoint_angle > 90 or next_checkpoint_angle < -90) else 100
        to_hit_target = will_pod_hit(next_checkpoint_dist, pods[0].speed, next_checkpoint_angle)
        
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
