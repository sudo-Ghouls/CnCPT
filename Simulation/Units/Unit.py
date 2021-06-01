# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from shapely.geometry import Point
from sortedcontainers import SortedListWithKey

from Simulation.GeographyPhysics import Kinematics, Route
from Simulation.Logic.ChildLogic import dock
from Simulation.Units.State import State
from Simulation.Utility.Area import Area


def base_behavior(_self, simulation_manager):
    pass


class Unit:
    def __init__(self, name=None, behavior=base_behavior, location=None, spawn_polygon=None, side=None, route=None,
                 parent=None, network=None):
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
            self.spawn_polygon = Area(spawn_polygon)
        else:
            self.spawn_polygon = None
        if location is not None:
            self.kinematics.set_location(Point(location[0], location[1]))
        elif spawn_polygon is not None:
            point = self.spawn_polygon.random_starting_loc_in_poly()
            self.kinematics.set_location(lat=point.x, lon=point.y)
        self.cost = None
        self.weapons = SortedListWithKey(key=(lambda x: -x.max_range))
        self.sensors = SortedListWithKey(key=(lambda x: -x.max_range))
        self.docked = False

        # Group Related
        self.group = None
        self.leader = None
        self.follower = []
        self.my_range_from_leader = None
        self.my_bearing_from_leader = None
        self.formation_lock = False
        self.parent = parent
        self.children = []

        # Behavior
        self.tasks = SortedListWithKey(key=(lambda x: -x.time))
        self.target = None
        self.state = State.NONE
        self.state_change_time = 0
        self.area = None
        self.route_propagation = False
        self.route = Route(route)
        self.brain = self.unconscious_brain
        self.time_between_thoughts = 600.0  # 600 second timestep

        # Nested Unit creation
        self.spawn = {}

        # Sensing
        self.contacts = {}

        # Communication
        self.network = network
        self.new_messages = []

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
                        new_child = key(name=child_name)
                        new_child.parent = self
                        new_child.side = self.side
                        dock(new_child, 0.0, refuel=False)
                        self.children.append(new_child)
                else:
                    for new_child in children_dict[key]:
                        new_child.parent = self
                        new_child.side = self.side
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
