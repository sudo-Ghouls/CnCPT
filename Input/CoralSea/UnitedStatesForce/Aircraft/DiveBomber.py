# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from Simulation.Units.BaseClasses.Aircraft import Aircraft
from Input.CoralSea.UnitedStatesForce.Logic.AircraftLogic import behavior_baseline
from Input.CoralSea.UnitedStatesForce.Sensors.Visual import VisualAir
from Input.CoralSea.UnitedStatesForce.Weapons.air_to_surface import AirLaunchedBomb
from Simulation.Utility.Conversions import kts_to_ms
from Simulation.Utility.SideEnum import SideEnum


class DiveBomber(Aircraft):
    def __init__(self, name=None, behavior=None, location=None, spawn_polygon=None,
                 side=SideEnum.BLUE, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)
        self.cost = 25
        self.refueling_length = 10 * 60 * 60  # 10 hour
        self.add_sensor(VisualAir())
        self.add_weapon(AirLaunchedBomb, 2)
        if behavior is None:
            self.my_brain = behavior_baseline


class DouglasSBDDauntless(DiveBomber):
    def __init__(self, name="DouglasSBDDauntless", behavior=None, location=None, spawn_polygon=None,
                 side=SideEnum.BLUE, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)
        self.kinematics.set_max_speed(
            kts_to_ms(161))  # Cruise speed from https://en.wikipedia.org/wiki/Douglas_SBD_Dauntless
        self.kinematics.set_max_range(max_range=1_794_000)
