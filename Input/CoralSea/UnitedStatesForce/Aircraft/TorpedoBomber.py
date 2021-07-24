# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from Simulation.Units.BaseClasses.Aircraft import Aircraft
from Input.CoralSea.UnitedStatesForce.Logic.AircraftLogic import behavior_baseline
from Input.CoralSea.UnitedStatesForce.Sensors.Visual import VisualAir
from Input.CoralSea.UnitedStatesForce.Weapons.air_to_surface import AirLaunchedTorpedo
from Simulation.Utility.Conversions import kts_to_ms
from Simulation.Utility.SideEnum import SideEnum


class TorpedoBomber(Aircraft):
    def __init__(self, name=None, behavior=None, location=None, spawn_polygon=None,
                 side=SideEnum.BLUE, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)
        self.cost = 20
        self.refueling_length = 10 * 60 * 60  # 10 hour
        self.add_sensor(VisualAir())
        self.add_weapon(AirLaunchedTorpedo, 1)
        if behavior is None:
            self.my_brain = behavior_baseline


class DouglasTBDDevastator(TorpedoBomber):
    def __init__(self, name="DouglasTBDDevastator", behavior=None, location=None, spawn_polygon=None,
                 side=SideEnum.BLUE, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)
        self.kinematics.set_max_speed(
            kts_to_ms(111))  # cruise speed from https://en.wikipedia.org/wiki/Douglas_TBD_Devastator
        self.kinematics.set_max_range(max_range=700_000)
