import sys
import math
import unittest


# Score points by scanning valuable fish faster than your opponent.

# A map is 10000 x 10000 u starting at 0 0
# A drone moves max 600 u per turn but sink by 300u if no motors
# A drone scans min 800u to 2000u around source
# A battery starts at 30 and drains by 5 for a high power scan put +1 for normal
# Drone has Id, x, y, and battery
# a number of fish is given
# the fish have id, colour, type, x, y, speed
# the details broadcast are id, colour and type

def log(message):
    print(message, file=sys.stderr, flush=True)


# drone, id, mine, x, y, battery
class drone:
    def __init__(self, id, mine, x, y, battery, boundry=None, strategy=None, radar=None):
        self.id = id
        self.mine = mine
        self.x = x
        self.y = y
        self.battery = battery
        self.power_light = 1
        self.action = 'WAIT'
        self.surfacing = False
        self.scanned = None
        self.strategy = strategy
        self.radar = radar
        self.known_targets = []
        self.target_x = None
        self.target_y = None
        self.boundry = boundry

    def get_next_action(self):

        strategy_target = self.strategy.get_target(self.radar.unscanned_targets)
        log(f'pre strategy {self.target_x}, {self.target_y} pust strategy {strategy_target}')
        self.ship_direction_cordinates(strategy_target)

        self.go_to_target()

    def radar_ping(self, radar_readings):
        self.radar.locate_targets(self, radar_readings, self.known_targets)

    def update_known_fish(self, fish):
        add_or_update(fish, self.known_targets)

    def go_to_target(self):
        if self.x != self.target_x or self.y != self.target_y:
            self.action = f'MOVE {self.target_x} {self.target_y} {self.power_light}'
        else:
            self.action = f"WAIT {self.power_light}"

    def ship_direction_cordinates(self, target_vector):

        if target_vector == 'SU':
            self.target_x = self.x
            self.target_y = self.y - 300
        if target_vector == 'TL':
            self.target_x = self.x - 300 if (self.x - 300) >= 0 else 0
            self.target_y = self.y - 300 if (self.y - 300 >= 0) else 0
        if target_vector == 'TR':
            self.target_x = self.x + 300 if (self.x + 300 <= self.boundary) else self.boundary
            self.target_y = self.y - 300 if (self.y - 300) >= 0 else 0
        if target_vector == 'BL':
            self.target_x = self.x - 300 if (self.x - 300) >= 0 else 0
            self.target_y = self.y + 300 if (self.y + 300) <= self.boundary else self.boundary
        if target_vector == 'BR':
            self.target_x = self.x + 300 if (self.x + 300) <= self.boundary else self.boundary
            self.target_y = self.y + 300 if (self.y + 300) <= self.boundary else self.boundary

    def turn_on_power_light(self):
        self.power_light = 1

    def turn_off_power_light(self):
        self.power_light = 0

    def check_for_surface(self, game_timer):
        if not self.surfacing:
            should_surface = SurfaceLogic.check_for_surface(self, game_timer, self.radar.unscanned_targets)
            if should_surface:
                log('surfacing')
                my_active_drone.surface(my_scan_record)

        if my_active_drone.surfacing:
            my_active_drone.surfaced()

    def surface(self, scanned):
        if self.y != 499 and self.scanned != scanned:
            self.scanned = scanned
            self.action = f"MOVE {self.x} {499} {self.power_light}"
            self.surfacing = True

    def surfaced(self):
        if self.y <= 499:
            self.surfacing = False


class fish:
    def __init__(self, id, _type, colour):
        self.id = id
        self.colour = colour
        self._type = _type
        self.x = None
        self.y = None
        self.vx = None
        self.vy = None
        self.visible = False
        self.base_value = self._get_base_value()
        self.scanned = False

    def update_location(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def _get_base_value(self):
        if self._type == 0:
            return 1
        elif self._type == 1:
            return 2
        else:
            return 3


def add_or_update(object_to_update, array):
    if object_to_update.id in [d.id for d in array]:
        if isinstance(object_to_update, drone):
            active_drone = [d for d in array if d.id == object_to_update.id][0]
            active_drone.x = object_to_update.x
            active_drone.y = object_to_update.y
            active_drone.battery = object_to_update.battery
        elif isinstance(object_to_update, fish):
            active_fish = [f for f in array if f.id == object_to_update.id][0]
            active_fish.update_location(object_to_update.x, object_to_update.y, object_to_update.vx,
                                        object_to_update.vy)
    else:
        array.append(object_to_update)

    return array


import math


class SurfaceLogic:
    # should I surface depends on:
    # if I Have to surface
    # if I have a combination of value
    # if I have some fish after some time
    # I need to know what is known about the scans that the opponent has because
    # the faster I can remove things from the list the more accurate things are

    def check_for_surface(ship, game_timer, fishes):
        return any([SurfaceLogic.have_to_surface(ship, game_timer), SurfaceLogic.have_valuable_content(fishes)])

    def have_to_surface(ship, game_timer):
        number_turns_needed = int(ship.y / 300)
        log(f'turns needed {number_turns_needed} available {game_timer + 3}')
        return (game_timer + 3) <= number_turns_needed

    def have_valuable_content(fishes):
        # if any are complete sets true
        fish_data = Analysis.get_fish_data(fishes)
        for c in fish_data['colours'].values():
            if len(c) == 3:
                return True
        for t in fish_data['types'].values():
            if len(t) == 4:
                return True
        return False


class MarshallStrategy:
    # determine the bias
    # move to bias edge
    # drop and ping every 5 turns until 1400 above base
    # converge
    def find_bias(ship, radar):
        pass


class MoveToDetectedStrategy:
    def __init__(self, boundary):
        self.boundary = boundary
        self.target_x = None
        self.target_y = None

    def get_target(self, detected_targets):
        counts_per_sector = {}
        for detected in set(detected_targets):
            counts_per_sector[detected] = len([x for x in radar if x == detected])
        if len(counts_per_sector) == 0:
            return 'SU'
        max_key = max(counts_per_sector, key=counts_per_sector.get)
        return max_key


class RadarStrategy:
    def __init__(self):
        self.name = 'Radar'
        self.all_targets = []
        self.unscanned_targets = []

    def locate_targets(self, ship, radar, known_fish):
        # log(radar)
        for f in radar:
            add_or_update(f, self.all_targets)
        radar = self.discount_already_known(ship, known_fish, radar)
        for f in radar:
            add_or_update(f, self.unscanned_targets)

    def discount_already_known(self, ship, known, radar_readings):
        # determine where known fish are
        for k in known:
            if k.x < ship.x and k.y < ship.y:
                if 'TL' in radar_readings: radar_readings.remove('TL')
            if k.x > ship.x and k.y < ship.y:
                if 'TR' in radar_readings: radar_readings.remove('TR')
            if k.x < ship.x and k.y > ship.y:
                if 'BL' in radar_readings: radar_readings.remove('BL')
            if k.x > ship.x and k.y > ship.y:
                if 'BR' in radar_readings: radar_readings.remove('BR')
        return radar_readings
        # discount them from the readings


def box_the_fish(fishes):
    '''
    returns box representing the area of fish as x,y string objects
    takes a list of fish objects
    '''
    if len(fishes) == 0: return None
    min_x = min([x.x for x in fishes])
    max_x = max([x.x for x in fishes])
    min_y = min([y.y for y in fishes])
    max_y = max([y.y for y in fishes])
    median = (min_x + int((max_x - min_x) / 2), int(min_y + int((max_y - min_y) / 2)))
    return [min_x, min_y, max_x, max_y, median]


def objects_in_sector(objects, sector):
    identified = [o for o in objects if
                  o.x >= sector['xmin'] and o.x <= sector['xmax'] and o.y >= sector['ymin'] and o.y <= sector['ymax']]
    return identified


def get_distance(source_x, source_y, destination_x, destination_y):
    return round(math.sqrt((source_x - destination_x) ** 2 + (source_y - destination_y) ** 2))


# quadrants
# divide the length by 2 thats the halfway point,
# convert to range 0 to hw -1  hw to edge
# for each y load with rows of for each  x
def generate_tiles(y_start, x_start, rng):
    tiles = {}
    tiles['xmin'] = x_start
    tiles['ymin'] = y_start
    tiles['xmax'] = x_start + rng
    tiles['ymax'] = y_start + rng
    tiles['range'] = rng
    tiles['midpoint'] = (int(x_start + (rng / 2)), int(y_start + (rng / 2)))
    return tiles


def generate_quadrants(map_dimension):
    # log('generating quadrants')
    half_points = int(map_dimension / 2)
    quadrants = {}
    quadrants['q1'] = generate_tiles(0, 0, half_points)
    quadrants['q2'] = generate_tiles(0, half_points, half_points)
    quadrants['q3'] = generate_tiles(half_points, 0, half_points)
    quadrants['q4'] = generate_tiles(half_points, half_points, half_points)
    return quadrants


def develop_data(quads, fishes):
    data = {}
    data_frame = {}
    for k, q in quads.items():
        data_frame[k] = objects_in_sector(fishes, q)
    for k, q in data_frame.items():
        if len(q) > 0:
            fish_box = box_the_fish(q)
            centroid_tile = fish_box[4]
        else:
            centroid_tile = quads[k]['midpoint']

        quadrant_data = {}
        quadrant_data['number_fish'] = len(q)
        quadrant_data['fish'] = q
        quadrant_data['tiles'] = quads[k]
        quadrant_data['fish_centroid'] = centroid_tile
        data[k] = quadrant_data
    return data


class Analysis:
    # analysis functions
    def get_fish_data(fishes):
        data = {}
        colours = {}
        types = {}
        colourind = list(set([f.colour for f in fishes]))
        typeind = list(set([f._type for f in fishes]))
        for c in colourind:
            colours[c] = [f for f in fishes if f.colour == c]
        for t in typeind:
            types[t] = [f for f in fishes if f._type == t]
        data['colours'] = colours
        data['types'] = types
        return data


# data containers
my_drones = []
enemy_drones = []
fish_array = []
my_scan_record = []
radar_readings = []
foe_scan_record = []
drone_strategy = MoveToDetectedStrategy(10000)
drone_radar_logic = RadarStrategy()

creature_count = int(input())
for i in range(creature_count):
    creature_id, color, _type = [int(j) for j in input().split()]
    fish_array = add_or_update(fish(creature_id, _type, color), fish_array)

# intel
all_colours = list(set([f.colour for f in fish_array]))
colour_counts = {c: len([f for f in fish_array if f.colour == c]) for c in all_colours}
quadrants = generate_quadrants(10000)

game_timer = 200
# game loop
while True:
    my_score = int(input())
    foe_score = int(input())

    my_scan_record = []
    my_scan_count = int(input())
    for i in range(my_scan_count):
        creature_id = int(input())
        my_scan_record.append(creature_id)
        [f for f in fish_array if f.id == creature_id][0].scanned = True

    foe_scan_record = []
    foe_scan_count = int(input())
    for i in range(foe_scan_count):
        creature_id = int(input())
        foe_scan_record.append(creature_id)

    my_drone_count = int(input())
    for i in range(my_drone_count):
        drone_id, drone_x, drone_y, emergency, battery = [int(j) for j in input().split()]
        add_or_update(drone(drone_id, True, drone_x, drone_y, battery, strategy=drone_strategy, radar=drone_radar_logic,
                            boundry=10000), my_drones)

    foe_drone_count = int(input())
    for i in range(foe_drone_count):
        drone_id, drone_x, drone_y, emergency, battery = [int(j) for j in input().split()]
        add_or_update(drone(drone_id, False, drone_x, drone_y, battery), enemy_drones)

    drone_scan_count = int(input())
    for i in range(drone_scan_count):
        drone_id, creature_id = [int(j) for j in input().split()]
        # log(f"drone{drone_id} sees {creature_id}")

    # also update the known fish
    visible_creature_count = int(input())
    for i in range(visible_creature_count):
        creature_id, creature_x, creature_y, creature_vx, creature_vy = [int(j) for j in input().split()]
        active_fish = [f for f in fish_array if f.id == creature_id][0]
        active_fish.x = creature_x
        active_fish.y = creature_y
        active_fish.visible = True

    # radar will report number of blips and locations relative to sub
    radar_blip_count = int(input())
    radar_readings = []
    for i in range(radar_blip_count):
        inputs = input().split()
        drone_id = int(inputs[0])
        creature_id = int(inputs[1])
        radar = inputs[2]
        radar_readings.append(radar)

    # intel
    valid_fish = [f for f in fish_array if f.visible and f.id not in my_scan_record]
    # log(f'valid fish {[f.id for f in valid_fish]}')
    # how many fish do we really know about
    visible_fish = [f for f in fish_array if f.visible]
    log(f'my scan {sorted(my_scan_record)}')
    log(f'foe scan {sorted(foe_scan_record)}')
    log(f'visible fish {sorted([f.id for f in visible_fish])}')
    log(f'valid fish {sorted([f.id for f in valid_fish])}')

    intel = develop_data(quadrants, valid_fish)
    target = 5000, 5000
    max_fish = max(intel, key=lambda k: intel[k]['number_fish'])
    target = intel[max_fish]['fish_centroid']
    # log(target)

    game_timer -= 1

    for i in range(my_drone_count):
        my_active_drone = my_drones[i]
        log(f"drone {my_active_drone.id} {my_active_drone.x}, {my_active_drone.y}, battery {my_active_drone.battery}")
        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)

        # MOVE <x> <y> <light (1|0)> | WAIT <light (1|0)>
        my_active_drone.check_for_surface(game_timer)
        # if not my_active_drone.surfacing:
        #  should_surface = SurfaceLogic.check_for_surface(my_active_drone, game_timer, valid_fish)
        #  if should_surface:
        #    log('surfacing')
        #    my_active_drone.surface(my_scan_record)

        # if my_active_drone.surfacing:
        #  my_active_drone.surfaced()
        my_active_drone.radar_ping(radar_readings)
        if not my_active_drone.surfacing:
            my_active_drone.get_next_action()

        print(my_active_drone.action)

