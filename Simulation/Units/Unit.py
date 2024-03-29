# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from shapely.geometry import Point
from sortedcontainers import SortedListWithKey

from Simulation.GeographyPhysics.Kinematics import Kinematics
from Simulation.Logic.ChildLogic import dock
from Simulation.Units.State import State
from Simulation.Utility.Area import Area


def base_behavior(_self, simulation_manager):
    pass


blank_group_data = {'group': None,
                    'leader': None,
                    'follower': [],
                    'my_range_from_leader': None,
                    'my_bearing_from_leader': None,
                    'formation_lock': False,
                    'parent': None,
                    'children': []}


class Unit:
    def __init__(self, name=None, behavior=base_behavior, location=None, spawn_polygon=None, side=None, route=None,
                 parent=None, network=None, group_data=None, kinematics_data=None):
        """

        :param name:
        :param behavior:
        :param location:
        :param spawn_polygon:
        :param side:
        :param route:
        """
        self.alive = True
        self.name = name
        self.side = side
        self.my_brain = behavior
        self.kinematics = Kinematics()
        if spawn_polygon is not None:
            if isinstance(spawn_polygon, Area):
                self.spawn_polygon = spawn_polygon
            else:
                self.spawn_polygon = Area(bounds=spawn_polygon)
        else:
            self.spawn_polygon = None
        if location is not None:
            self.kinematics.set_location(Point(location[0], location[1]))
        elif self.spawn_polygon is not None:
            point = self.spawn_polygon.random_starting_loc_in_poly()
            self.kinematics.set_location(lat=point.x, lon=point.y)
        self.cost = None
        self.weapons = SortedListWithKey(key=(lambda x: -x.max_range))
        self.sensors = SortedListWithKey(key=(lambda x: -x.max_range))
        self.docked = False

        # Group Related
        self.parent = parent
        if group_data is None:
            group_data = blank_group_data
        self.group = group_data.pop('group', None)
        self.leader = group_data.pop('leader', None)
        self.follower = group_data.pop('follower', [])
        self.my_range_from_leader = group_data.pop('my_range_from_leader', None)
        self.my_bearing_from_leader = group_data.pop('my_bearing_from_leader', None)
        self.formation_lock = group_data.pop('formation_lock', False)
        if self.parent is None:
            self.parent = group_data.pop('parent', parent)
        self.children = group_data.pop('children', [])

        # Behavior
        self.tasks = SortedListWithKey(key=(lambda x: -x.time))
        self.target = None
        self.state = State.NONE
        self.state_change_time = 0
        self.area = None
        self.route_propagation = False
        self.route = route
        self.brain = self.unconscious_brain
        self.time_between_thoughts = 600.0  # 600 second timestep

        # Kinematics (need for unpickling object)
        if kinematics_data is not None:
            self.kinematics._location = kinematics_data.pop("_location")
            self.kinematics._heading = kinematics_data.pop("_heading")
            self.kinematics._speed = kinematics_data.pop("_speed")
            self.kinematics._max_speed = kinematics_data.pop("_max_speed")
            self.kinematics._max_range = kinematics_data.pop("_max_range")
            self.kinematics._range_travelled = kinematics_data.pop("_range_travelled")

            # Nested Unit creation
        self.spawn = {}

        # Sensing
        self.contacts = {}

        # Communication
        self.network = network
        self.new_messages = []

    def __reduce__(self):
        self.group_data = {'group': self.group,
                           'leader': self.leader,
                           'follower': self.follower,
                           'my_range_from_leader': self.my_range_from_leader,
                           'my_bearing_from_leader': self.my_bearing_from_leader,
                           'formation_lock': self.formation_lock,
                           'parent': self.parent,
                           'children': self.children}

        kinematics_data = {"_location": self.kinematics._location,
                           "_heading": self.kinematics._heading,
                           "_speed": self.kinematics._speed,
                           "_max_speed": self.kinematics._max_speed,
                           "_max_range": self.kinematics._max_range,
                           "_range_travelled": self.kinematics._range_travelled}

        return (self.__class__,
                (self.name, self.my_brain, self.kinematics.get_location(), self.spawn_polygon, self.side, self.route,
                 self.parent, self.network, self.group_data, kinematics_data))

    def add_sensor(self, sensor):
        """

        :param sensor:
        :return:
        """
        self.sensors.add(sensor)
        sensor.parent_unit = self

    def add_weapon(self, weapon_class, amount):
        """

        :param weapon_class:
        :param amount:
        :return:
        """
        weapon_name = "{0}__{1}".format(weapon_class.__name__, self.name)
        self.weapons.add(weapon_class(weapon_name, amount))

    def add_children(self, children_dict):
        """

        :param children_dict: dictionary of children to create values can be integer number (N) or a list of unit
            instances. If interger, N number of units will be spawned wit their default values.
        :return:
        """
        if children_dict is not None:
            for key in children_dict:
                if type(children_dict[key]) is int:
                    for i in range(children_dict[key]):
                        child_name = "{0}_{1}__{2}".format(key.__name__, i, self.name)
                        new_child = key(name=child_name, network=self.network, parent=self, side=self.side)
                        dock(new_child, 0.0, refuel=False)
                        self.children.append(new_child)
                else:
                    for new_child in children_dict[key]:
                        new_child.parent = self
                        new_child.side = self.side
                        new_child.network = self.network
                        dock(new_child, 0.0, refuel=False)
                        self.children.append(new_child)
        self.spawn = {child.name: child for child in self.children}  # to register children to simulation_manager

    def unconscious_brain(self, _self, simulation_manager):
        """

        :param _self:
        :param simulation_manager:
        :return:
        """

        self.my_brain(_self, simulation_manager)

    def moving(self):
        """

        :return:
        """
        speed = self.kinematics.get_speed()
        return not speed == 0

    def register(self, simulation_manager, constants=None):
        """

        :param simulation_manager:
        :param constants:
        :return:
        """
        if constants is not None:
            self.constants = constants
        simulation_manager.process(self.process(simulation_manager))

    def process(self, simulation_manager):
        """

        :param simulation_manager:
        :return:
        """
        while self.alive:
            if self.brain:
                self.brain(self, simulation_manager=simulation_manager)
            yield simulation_manager.timeout(self.time_between_thoughts)
