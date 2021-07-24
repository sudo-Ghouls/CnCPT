# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from Simulation.Units.BaseClasses.Ship import Ship
from Simulation.Units.core import BasicBehavior
from Simulation.Utility.SideEnum import SideEnum


class HeavyCruiser(Ship):
    def __init__(self, name=None, behavior=None, location=None, spawn_polygon=None, side=SideEnum.RED, route=None,
                 parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)
        self.cost = 250

    @staticmethod
    def behavior_aggressive(unit, simulation_manager):
        pass

    @staticmethod
    def behavior_passive(unit, simulation_manager):
        pass

    @staticmethod
    def behavior_baseline(unit, simulation_manager):
        unit.kinematics.set_speed(10)
        BasicBehavior.RouteFollowing(unit, simulation_manager)


class Myoko(HeavyCruiser):
    def __init__(self, name="Myoko", behavior=HeavyCruiser.behavior_baseline, location=None, spawn_polygon=None,
                 side=SideEnum.RED, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)


class Haguro(HeavyCruiser):
    def __init__(self, name="Haguro", behavior=HeavyCruiser.behavior_baseline, location=None, spawn_polygon=None,
                 side=SideEnum.RED, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)


class Aoba(HeavyCruiser):
    def __init__(self, name="Aoba", behavior=HeavyCruiser.behavior_baseline, location=None, spawn_polygon=None,
                 side=SideEnum.RED, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)


class Kako(HeavyCruiser):
    def __init__(self, name="Kako", behavior=HeavyCruiser.behavior_baseline, location=None, spawn_polygon=None,
                 side=SideEnum.RED, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)


class Kinugasa(HeavyCruiser):
    def __init__(self, name="Kinugasa", behavior=HeavyCruiser.behavior_baseline, location=None, spawn_polygon=None,
                 side=SideEnum.RED, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)


class Furutaka(HeavyCruiser):
    def __init__(self, name="Furutaka", behavior=HeavyCruiser.behavior_baseline, location=None, spawn_polygon=None,
                 side=SideEnum.RED, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)
