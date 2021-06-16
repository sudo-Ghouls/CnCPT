# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from Input.CoralSea.BaseClasses.Aircraft import Aircraft
from Input.CoralSea.JapaneseForce.Sensors.Visual import VisualAir
from Input.CoralSea.JapaneseForce.Weapons.air_to_air import AirToAirGun
from Simulation.Logic.ChildLogic import return_to_parent
from Simulation.Logic.General import determine_priority_target_contact, pursue_target
from Simulation.Logic.Patrol import patrol
from Simulation.Units.State import State
from Simulation.Utility.Conversions import kts_to_ms
from Simulation.Utility.SideEnum import SideEnum


class Fighter(Aircraft):
    def __init__(self, name=None, behavior=None, location=None, spawn_polygon=None, side=None, route=None, parent=None,
                 network=None, group_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=SideEnum.RED, route=route, parent=parent, network=network, group_data=group_data)
        self.cost = 200
        self.refueling_length = 10 * 60 * 60  # 10 hour
        self.add_sensor(VisualAir())
        self.add_weapon(AirToAirGun, 100)
        if behavior is None:
            self.my_brain = self.behavior_baseline

    @staticmethod
    def behavior_baseline(unit, simulation_manager):
        if unit.kinematics.get_range_traveled() > unit.kinematics.get_max_range():
            unit.state = State.RTB

        if unit.state is State.DOCKED_REFUELING:
            if simulation_manager.now - unit.state_change_time > unit.refueling_length:
                unit.state = State.DOCKED_READY

        if unit.state is State.SEARCH:
            if bool(unit.contacts) and unit.target is None:
                target_contact = determine_priority_target_contact(unit.contacts, method='range',
                                                                   excluded_classes=Aircraft)
                if unit.target is not None:
                    unit.target = target_contact.target_name_truth
            if unit.target:
                target_contact = unit.contacts.get(unit.target, None)
                if target_contact is not None:
                    unit.state = State.ENGAGE
                else:
                    unit.target = None
            else:
                patrol(unit)

        if unit.state is State.ENGAGE:
            if bool(unit.contacts) and unit.target is None:
                target_contact = determine_priority_target_contact(unit.contacts, method='range')
                if unit.target is not None:
                    unit.target = target_contact.target_name_truth
            if unit.target:
                target_contact = unit.contacts.get(unit.target, None)
                if target_contact is not None:
                    pursue_target(unit, target_contact, standoff_range_m=0)
                else:
                    unit.target = None
            else:
                patrol(unit)

        if unit.state is State.RTB:
            return_to_parent(unit, simulation_manager.now)

    @staticmethod
    def behavior_aggressive(unit, simulation_manager):
        pass

    @staticmethod
    def behavior_passive(unit, simulation_manager):
        pass


class A6M2Zero(Fighter):
    def __init__(self, name="A6M2Zero", behavior=Fighter.behavior_baseline, location=None, spawn_polygon=None,
                 side=SideEnum.RED, route=None, parent=None, network=None, group_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data)


class MitsubishiA5MType96(Fighter):
    def __init__(self, name="MitsubishiA5MType96", behavior=Fighter.behavior_baseline, location=None,
                 spawn_polygon=None, side=SideEnum.RED, route=None, parent=None, network=None, group_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data)
        self.kinematics.set_max_speed(
            kts_to_ms(235))  # Max speed from https://en.wikipedia.org/wiki/Grumman_F4F_Wildcat
        self.kinematics.set_max_range(max_range=1_201_000)
