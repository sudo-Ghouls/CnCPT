# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from Input.CoralSea.BaseClasses.Aircraft import Aircraft
from Input.CoralSea.JapaneseForce.Sensors.Visual import VisualAir
from Input.CoralSea.JapaneseForce.Weapons.air_to_surface import AirLaunchedBomb
from Simulation.Communication.Message import DetectionMessage
from Simulation.Logic.ChildLogic import return_to_parent
from Simulation.Logic.General import determine_priority_target_contact, pursue_target
from Simulation.Logic.Patrol import patrol
from Simulation.Units.State import State
from Simulation.Utility.Conversions import kts_to_ms
from Simulation.Utility.SideEnum import SideEnum
from Input.CoralSea.UnitedStatesForce.Logic.AircraftLogic import behavior_baseline


class DiveBomber(Aircraft):
    def __init__(self, name=None, behavior=None, location=None, spawn_polygon=None, side=SideEnum.RED, route=None,
                 parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)
        self.cost = 25
        self.refueling_length = 10 * 60 * 60  # 10 hour
        self.add_sensor(VisualAir())
        self.add_weapon(AirLaunchedBomb, 2)
        if behavior is None:
            self.my_brain = behavior_baseline


class AichiD3AType99(DiveBomber):
    def __init__(self, name="AichiD3AType99", behavior=behavior_baseline, location=None, spawn_polygon=None,
                 side=SideEnum.RED, route=None, parent=None, network=None, group_data=None, kinematics_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data,
                         kinematics_data=kinematics_data)
        self.kinematics.set_max_speed(kts_to_ms(230))  # Cruise speed from https://en.wikipedia.org/wiki/Aichi_D3A
        self.kinematics.set_max_range(max_range=1_352_000)
