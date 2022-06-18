from cmath import acos, asin
import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
# add additional 
'''
Intelligence gathering 
speed of pod - arbitary value derived from the distance from last sample - done
rate toward target - speed toward next checkpoint - done
implement telemetry
improve speed function
implement will_hit_target - iteration 1:  will the pod be facing the target by the time it reaches it given that we know distance and ticks and acceleration is about 25 per
tich and the turn rate is 17 degrees a tick the algorithm would be the distance to the target and the starting speed and angle
add additional telemetry to determine turn rate is it constant - NO
add code to decelerate and accelerate - Done
Implement trajectorey angle as simple response - done
implement apex points
'''

def debug(m):
    print(m, file=sys.stderr, flush=True)

def distance_between_two_points(reference_x, reference_y, target_x, target_y):
    x_delta = target_x - reference_x
    y_delta = target_y - reference_y
    return int(math.sqrt((x_delta ** 2) + (y_delta ** 2)))

def calculate_angles_from_coords(point_a.x, point_a.y, point_b.x, point_b.y, point_c.x, point_c.y):
    distance_a_to_b = distance_between_two_points(point_a.x, point_a.y, point_b.x, point_b.y)
    distance_b_to_c = distance_between_two_points(point_b.x, point_b.y, point_c.x, point_c.y)
    distance_c_to_a = distance_between_two_points(point_c.x, point_c.y, point_a.x, point_a.y)
    

def calculate_trajectory(primary_x, primary_y, secondary_x, secondary_y, target_x, target_y):
    reference_line = distance_between_two_points(primary_x, primary_y, target_x, target_y)
    travel_line = distance_between_two_points(primary_x, primary_y, secondary_x, secondary_y)
    target_line = distance_between_two_points(secondary_x,secondary_y, target_x, target_y)

    reference_angle = int(57.29*((acos((reference_line**2+travel_line**2-target_line**2)/(2*reference_line * travel_line)).real)))
    travel_angle = int(57.29*(acos((travel_line**2 + target_line **2 - reference_line **2)/ (2 * travel_line * target_line)).real))
    target_angle =int( 57.29*(acos ((target_line ** 2 + reference_line ** 2 - travel_line ** 2)/(2 * target_line * reference_line)).real))
    return [reference_angle, travel_line, target_angle, travel_angle]

def will_pod_hit(refrence_x, reference_y, secondary_x, secondary_y, target_x, target_y):
    # light weight check assumptions, accelleration is constant 25 per tick, max speed is 650, turnRate is 17 degrees per tick
    # v 1.2 - normalize to 360 degrees - done - redact for 1.3
    # v 1.3 - compensate for speed by reducing the angle available as a factor of percent of max speed - fail cant detect miss in time 
    # v 1.4 - apply vector angles and try and determine where it will go over the distance 


    vectors = calculate_angle(refrence_x, reference_y, secondary_x, secondary_y, target_x, target_y)
    debug(vectors)

    return True


class Checkpoint:
    def __init__(self, position, x, y):
        self.position = position
        self.x = x
        self.y = y
        self.distance_to_next = None
        self.apex_x = None
        self.apex_y = None 
        self.angle_to_next = None

    def __str__(self):
        return(f"{self.position}, {self.x}, {self.y}, {self.distance_to_next}")

    def update_distance_to_next(self, next_x, next_y):
        self.distance_to_next = distance_between_two_points(self.x,self.y, next_x, next_y)
    
    def set_angle_to_next(self, previous_checkpoint, next_checkpoint):
        trajectory_data = calculate_trajectory(previous_checkpoint.x, previous_checkpoint.y,self.x, self.y,next_checkpoint.x, next_checkpoint.y)
        self.angle_to_next = trajectory_data[0]
    


     

class Telemetry:
    def __init__(self):
     self.readings = []
    
    def add_reading(self,iteration, target_id,  x, y, angle_to_target, distance_to_target, speed, trajectory_angle, speed_toTarget, will_hit):
        rec = {}
        rec["iteration"] = iteration
        rec["target"] = target_id
        rec["ship_x"] = x
        rec["ship_y"] = y
        rec["angle_to_target"] = angle_to_target if angle_to_target >=0 else angle_to_target * -1 
        rec["distance_to_target"] = distance_to_target
        rec["trajectory_angle"] = trajectory_angle
        rec["speed_to_target"] = speed_toTarget
        rec["ship_speed"] = speed
        rec["will_hit_target"] = will_hit

        debug(rec)
        self.readings.append(rec)



class Course:
    def __init__(self):
        self.checkpoints = []
        self.course_known = False
        self.active_target_checkpoint = None
        self.last_active_checkpoint = None
    
    def add_checkpoint(self, id, x, y):
         checkpoints.append(Checkpoint(id,x,y))

    def update_active_target(self, target_x, target_y):
        self.update_course_state(target_x, target_y)
        self.active_target_checkpoint = (next((cp for cp in checkpoints if cp.x == target_x and cp.y == target_y ), None))
    
    def is_add_checkpoint(self, next_checkpoint_x, next_checkpoint_y):
        checkpoints_changed = self.checkpoints[-1].x != next_checkpoint_x or checkpoints[-1].y != next_checkpoint_y
        checkpoint_matches_known = (sum(c.x == next_checkpoint_x for c in checkpoints ) >0 and sum(c.y == next_checkpoint_y for c in checkpoints) > 0)
        return checkpoints_changed and not checkpoint_matches_known

    def is_map_conditions_met(self, next_checkpoint_x, next_checkpoint_y ):
        next_checkpoint_is_first = len(self.checkpoints)> 1 and  self.checkpoints[0].x == next_checkpoint_x and self.checkpoints[0].y == next_checkpoint_y
        return next_checkpoint_is_first
    
    def update_course_state(self, next_checkpoint_x, next_checkpoint_y):
        if self.is_add_checkpoint(next_checkpoint_x, next_checkpoint_y):
            active_target = Checkpoint(len(self.checkpoints)+1, next_checkpoint_x, next_checkpoint_y)
            checkpoints.append(active_target)
            for c in self.checkpoints:
                debug(c)
    
        elif self.is_map_conditions_met(next_checkpoint_x, next_checkpoint_y): #set checkpoints
            debug("Map read executing analysis")
            for c_index in range(len(self.checkpoints)):
                wrap_index = c_index+1 if c_index+1 < len(self.checkpoints) else -1
                set_distance(self.checkpoints[c_index - 1], self.checkpoints[c_index])
                debug(f"{c_index}, {wrap_index}")
                self.checkpoints[c_index].set_angle_to_next(self.checkpoints[c_index-1], self.checkpoints[wrap_index])

            for c in self.checkpoints:
                debug(c)
            self.course_known = True

def map_checkpoint(previous_checkpoint, current_checkpoint, next_checkpoint):
    current_checkpoint.update_distance_to_next(next_checkpoint.x, next_checkpoint.y)
    current_checkpoint.apex_angle = calculate_trajectory(previous_checkpoint.x, previous_checkpoint.y, current_checkpoint.x, current_checkpoint.y, next_checkpoint.x, next_checkpoint.y)[0]


def set_distance(source_checkpoint, target_checkpoint):
       source_checkpoint.update_distance_to_next(target_checkpoint.x, target_checkpoint.y)
  
    
        

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
        self.trajectory_angle = 0
        self.thrust = 100
        self.hit_next_target = True
        self.fire_boost = False


    def update_position(self, target_id, new_x, new_y, distance_to_target, angle_to_target, target_x, target_y):
        self.race_iterator+=1
        self.update_speed(new_x, new_y)
        self.speed_to_target = self.target_distance - distance_to_target
        trajectory = calculate_trajectory(self.x,self.y,new_x,new_y,target_x, target_y)
        debug(trajectory)
        self.trajectory_angle = trajectory[0]
        self.update_pod_position(new_x, new_y)
        self.target_distance = distance_to_target
        self.will_I_hit_target()
        self.tel.add_reading(self.race_iterator,self.hit_next_target, target_id, new_x, new_y, angle_to_target, distance_to_target, self.speed, self.trajectory_angle, self.speed_to_target)
        

    def update_speed(self, new_x, new_y):
        self.x_momentum = (self.x - new_x)*-1
        self.y_momentum = (self.y - new_y)*-1
        self.speed = distance_between_two_points(self.x,self.y,new_x,new_y)
    
    def update_pod_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
    
    def accellerate(self, rate): 
        if (self.thrust+ rate) >100:
            self.thrust = 100
        else:
            self.thrust += rate
    
    def decellerate(self, rate):
        if (self.thrust - rate )<17:
            self.thrust = 17
        else:
            self.thrust -= rate
    
    def will_I_hit_target(self):
        self.hit_next_target = True if self.trajectory_angle in range(0,30)  else False 

    def __str__(self):
        return(f"pod {self.identity} Speed {self.speed} Speed to target {self.speed_to_target}, trajectory angle to target {self.trajectory_angle}")





class Optimisation:
    def __init__(self):
        self.window = 80
    

'''Operational race code'''


pods = []
active_target = None
course_known = False
boost_fired = False
lap = 1
lapped = False
opt = Optimisation()
course = Course()
checkpoints = course.checkpoints

# game loop
while True:
    # next_checkpoint_x: x position of the next check point
    # next_checkpoint_y: y position of the next check point
    # next_checkpoint_dist: distance to the next checkpoint
    # next_checkpoint_angle: angle between your pod orientation and the direction of the next checkpoint

    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]

    if len(checkpoints) == 0: #no checkpoints add one
        course.add_checkpoint(1,next_checkpoint_x, next_checkpoint_y)
        pods.append(Pod("Player", x, y, next_checkpoint_dist))
    
    player = pods[0]
    course.update_active_target(next_checkpoint_x, next_checkpoint_y)
    
    if pods[0].x != x or pods[0].y != y: #is the pod in a different positon to last time
        pods[0].update_position(course.active_target_checkpoint.position, x,y,next_checkpoint_dist, next_checkpoint_angle,next_checkpoint_x, next_checkpoint_y )
        debug(f"{pods[0]}")
    


    

    if(course.course_known):
        player = pods[0]
        course.last_active_checkpoint = course.active_target_checkpoint
        
        course.update_active_target(next_checkpoint_x,next_checkpoint_y )

        if course.active_target_checkpoint != course.last_active_checkpoint and course.active_target_checkpoint == course.checkpoints[1] :
            lap +=1 
            debug(f"Lap changed, lap {lap}")
            if lap == 2:
                debug(pods[0].tel)
        lengths = [x.distance_to_next for x in checkpoints]
        lengths.insert(0, lengths.pop())
        debug(f"{lengths}, {lengths.index(max(lengths))+1}" )

        player.decellerate(40) if not player.hit_next_target else player.accellerate(60)

        longest_leg = next(x for x in checkpoints if x.distance_to_next == max(lengths))
        debug(longest_leg.position)
        
        if not boost_fired and course.active_target_checkpoint.position == lengths.index(max(lengths))+1:
            if player.trajectory_angle <= 30:
                debug("Fire boost")
                player.fire_boost = True
                boost_fired = True
    else:
        player.decellerate(40) if not player.hit_next_target else player.accellerate(60)



    debug(f"thrust {player.thrust}, boost fired {boost_fired}")






    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)


    # You have to output the target position
    # followed by the power (0 <= thrust <= 100)
    # i.e.: "x y thrust"


    thrust_value = player.thrust
    if player.fire_boost:
        thrust_value = "BOOST"


    print(str(next_checkpoint_x) + " " + str(next_checkpoint_y) + f" {thrust_value}")
