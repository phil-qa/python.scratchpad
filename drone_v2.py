import random
import sys
import unittest
class utility:
    def log(message):
        print(message, file=sys.stderr, flush=True)

    def add_or_update(object_to_update, array):
        if object_to_update.id in [d.id for d in array]:
            if isinstance(object_to_update, Drone):
                active_drone = [d for d in array if d.id == object_to_update.id][0]
                active_drone.x = object_to_update.x
                active_drone.y = object_to_update.y
                active_drone.battery = object_to_update.battery
            elif isinstance(object_to_update, Fish):
                active_fish = [f for f in array if f.id == object_to_update.id][0]
                active_fish.update_location(object_to_update.x, object_to_update.y, object_to_update.vx,
                                            object_to_update.vy)
        else:
            array.append(object_to_update)

        return array

class Map:
    def __init__(self, dimension):
        self.dimension = dimension
        self.half_dimension =int(dimension/2)
class Drone:
    def __init__(self, id, mine, x, y, map, strategy = None ):
        self.id = id
        self.mine = mine
        self.x = x
        self.y = y
        self.map = map
        self._power_light = 1
        self._strategy = strategy
        self.known_fish = []
        self.target_x = None
        self.target_y = None
        self._action = f'WAIT'
        self.surfacing = False

    def action(self):
        return f'{self._action} {self._power_light}'

    def set_action(self, radar_readings, currently_identified, game_timer):
        action_choice = self._strategy.get_target(self, radar_readings, currently_identified, game_timer)

    def update_radar_data(self,data):
        self._strategy.radar_strategy.location_update(data)

    def go_to(self, x, y):
        self.target_x = x
        self.target_y = y
        self._action = f'MOVE {x} {y}'

    def set_power_light(self, state):
        if state == 'OFF':
            self._power_light = 0
        else:
            self._power_light = 1

    def surface(self):
        self._action = f'MOVE {self.x} {499}'


class Fish:
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

class BasicSurfaceStrategy:
    def __init__(self, dimension):
        self.dimension = dimension
        self.surfacing = False

    def check_for_surface(self,ship, game_timer, objects):
        self.surfacing =  any([self._have_to_surface(ship, game_timer), self._have_valuable_content(objects)])

    def _have_to_surface(self, ship, game_timer):
        number_turns_needed = int(ship.y/300)
        return (game_timer + 3) <= number_turns_needed

    def _have_valuable_content(self, objects):
        object_data = Analysis.get_object_data(objects)
        for c in object_data['colours'].values():
            if len(c) == 3:
                return True
        for t in object_data['types'].values():
            if len(t) == 4:
                return True
        return False

class Analysis:
    def get_object_data(objects):
        data = {}
        colours = {}
        types = {}
        colourind = list(set([f.colour for f in objects]))
        typeind = list(set([f._type for f in objects]))
        for c in colourind:
            colours[c] = [f for f in objects if f.colour == c]
        for t in typeind:
            types[t] = [f for f in objects if f._type == t]
        data['colours'] = colours
        data['types'] = types
        return data

class Radar:
    def __init__(self):
        self.locations = {}
    def locate_targets(self, known_targets):
        ''' locations will be updated with a k:v of creature_id and relative location
        a request for the unknown relatives will b ereturned in a K:V'''
        unknown_target_locations = self._remove_known(known_targets)
        return unknown_target_locations

    def location_update(self, data):
        '''from a data drop creature_id, Relative location update the locations dictionary'''
        self.locations[data[0]] = data[1]

    def _remove_known(self, known):
        known_ids = [f.id for f in known]
        return {k:v for (k,v) in self.locations if k not in known_ids}

class GoToUnknown:
    def __init__(self, map, radar_strategy, surface_strategy):
        self.map = map
        self.radar_strategy = Radar()
        self.surface_strategy = surface_strategy
        self.target_x = None
        self.target_y = None

    def get_target(self,ship, radar_readings, currently_identified, game_timer):
        ''' takes the radar data from the game input which is a  list of  rough locations
        and returns an activity to do next based on the things that are already known, something
        that should be based on the known stuff'''
        # should drone surface
        if self.surface_strategy.check_for_surface(ship, game_timer, currently_identified):
            ship.surface()
            return None
        #if the drone should not surface what direction is the most fish in
        target_sectors = self.radar_strategy.locate_targets(currently_identified)
        counts_per_sector = {}
        for sector in set(target_sectors):
            counts_per_sector[sector] = len([x for x in target_sectors if x == sector])
        if len(counts_per_sector) == 0:
            ship.surface()
            return None
        max_key = max(counts_per_sector, key=counts_per_sector.get)
        self.ship_direction_cordinates(max_key)
        return (self.target_x, self.target_y)

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


# data containers
map = Map(10000)

fish_array = []
my_drones = []
enemy_drones = []
radar = Radar
surface_logic = BasicSurfaceStrategy(map.dimension)
strategy = GoToUnknown(map,radar,surface_logic)

#execution routine
#creature_count = int(input())
#for i in range(creature_count):
#    creature_id, color, _type = [int(j) for j in input().split()]
#    fish_array = Utility.add_or_update(Fish(creature_id, _type, color), fish_array)

game_timer = 200
#game loop
loop = False
if loop:
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
        Utility.add_or_update(Drone(drone_id, True, drone_x, drone_y, map, strategy), my_drones)

    foe_drone_count = int(input())
    for i in range(foe_drone_count):
        drone_id, drone_x, drone_y, emergency, battery = [int(j) for j in input().split()]
        Utility.add_or_update(Drone(drone_id, False, drone_x, drone_y, battery), enemy_drones)

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
    for i in range(radar_blip_count):
        inputs = input().split()
        drone_id = int(inputs[0])
        creature_id = int(inputs[1])
        radar = inputs[2]
        [d for d in my_drones if d.id == drone_id][0].update_radar_data((creature_id,radar))


    game_timer -= 1

    for i in range(my_drone_count):
        my_active_drone = my_drones[i]
        Utility.log(f"drone {my_active_drone.id} {my_active_drone.x}, {my_active_drone.y}, battery {my_active_drone.battery}")
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



class tests(unittest.TestCase):
    import random
    def test_map(self):
        map = Map(10000)
        self.assertTrue(map.half_dimension == 5000, f"should be 5000 is {map.half_dimension}")
        self.assertTrue(map.dimension == 10000)

    def test_drone(self):
        map = Map(10000)
        drone = Drone(0, True, 0, 300, map)

        self.assertTrue(drone.id == 0)
        self.assertTrue(drone.mine)
        self.assertTrue(drone.x == 0)
        self.assertTrue(drone.y == 300)
        self.assertEqual(drone._power_light, 1)
        self.assertIsNone(drone._strategy)
        self.assertFalse(drone.known_fish)
        self.assertIsNone(drone.target_x)
        self.assertIsNone(drone.target_y)
        self.assertEqual(drone.action(), "WAIT 1")
        # drone goes to
        drone.go_to(300,600)
        self.assertTrue(drone.target_x == 300)
        self.assertTrue(drone.target_y == 600)
        self.assertTrue(drone.action() == "MOVE 300 600 1")
        # drone activities
        drone.set_power_light('OFF')
        self.assertTrue(drone.action() == "MOVE 300 600 0", f'powerlight off, is {drone.action()}')
        drone.set_power_light('ON')
        self.assertTrue(drone.action() == "MOVE 300 600 1")
        drone.surface()
        self.assertTrue(drone.action() == 'MOVE 0 499 1', f'failed , {drone.action()}')

    def test_fish(self):
        fish = Fish(0,1,1)
        self.assertTrue(fish.id == 0)
        self.assertTrue(fish.colour == 1)
        self.assertTrue(fish._type == 1)

        fish.update_location(2,2,0,0)
        self.assertTrue(fish.x == 2)
        self.assertTrue(fish.y == 2)
        self.assertTrue(fish.vx == 0)
        self.assertTrue(fish.vy == 0)

    def game_tests(self):
        f_array = []
        for f in range (10):
            Utility.add_or_update(Fish(f,1,2),f_array)

        f[0].x = 10
        f[0].y = 10
        f[1].x = 1000
        f[1].y = 1000
        f[2].x = 1500
        f[2].y = 1500
        f[3].x = 5500
        f[3].y = 10
        f[4].x = 6000
        f[4].y = 1000
        f[6].x = 10
        f[6].y = 5500
        f[7].x = 100
        f[7].y = 6000
        f[8].x = 5200
        f[8].y = 5500
        f[9].x = 6000
        f[9].y = 6500



        map = Map(10000)
        radar = Radar
        surface_logic = BasicSurfaceStrategy(map.dimension)
        strategy = GoToUnknown(map, radar, surface_logic)

        my_ship = Drone(0,True,4900,0, map,strategy)
        self.assertTrue(my_ship._strategy)
        radar_locations = []
        for f in f_array:
            loc = 'TL' if (f.x <my_ship.x and f.y < my_ship.y) else 'TR' if (f.x > my_ship.x and f.y < my_ship.y) else 'BL' if (f.x < my_ship.x and f.y > my_ship.y) else 'BR' if (f.x > my_ship.x and f.y > my_ship.y)
            radar_locations.append(loc)
        my_ship.set_action()





unittest.main()