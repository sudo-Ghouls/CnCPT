# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from Simulation.Communication.Message import DetectionMessage
from Simulation.GeographyPhysics.core import reckon
from Simulation.Logic.General import determine_priority_target_contact, pursue_target
from Simulation.Logic.Patrol import patrol
from Simulation.Units.State import State
from Simulation.Utility.Area import Area
from Simulation.Utility.Conversions import kts_to_ms


def behavior_aggressive(unit, simulation_manager):
    if unit.group.leader is unit:
        if unit.state is State.PATROL:
            if unit.area is None:
                # establish patrol area 150 miles into enemy territory
                my_location = unit.kinematics.get_location()
                center = reckon(150, 0, my_location[0], my_location[1], unit="nmi")
                unit.area = Area.create_patrol_area_from_center(center, 100, 100, unit='nmi')
            if bool(unit.contacts) and unit.target is None:
                target_contact = determine_priority_target_contact(unit.contacts, method='range')
                if target_contact is not None:
                    unit.target = target_contact.target_name_truth
            if unit.target:
                target_contact = unit.contacts.get(unit.target, None)
                if target_contact is not None:
                    unit.target_located = True
                    unit.target_location = (target_contact.latitude, target_contact.longitude)
                    unit.state = State.ENGAGE
                else:
                    unit.target = None
                    unit.group.leader.target_located = False
                    unit.group.leader.target_location = None
            else:
                patrol(unit)
                unit.state = State.PATROL

        if unit.state is State.ENGAGE:
            if bool(unit.contacts) and unit.target is None:
                target_contact = determine_priority_target_contact(unit.contacts, method='range')
                if target_contact is not None:
                    unit.target = target_contact.target_name_truth
            if unit.target:
                target_contact = unit.contacts.get(unit.target, None)
                if target_contact is not None:
                    pursue_target(unit, target_contact, standoff_range_m=0)
                else:
                    unit.target = None
            else:
                patrol(unit)
                unit.state = State.PATROL
    else:  # for not lead units, just feed lead contacts
        if bool(unit.contacts):
            for target in unit.contacts:
                contact = unit.contacts[target]
                message = DetectionMessage(contact, simulation_manager.now)
                unit.network.send_message(message, unit, unit.group.leader)

    unit.kinematics.set_speed(kts_to_ms(20))


def behavior_passive(unit, simulation_manager):
    if unit.group.leader is unit:
        if unit.state is State.PATROL:
            if unit.area is None:
                # establish patrol area 50 miles away from enemy territory
                my_location = unit.kinematics.get_location()
                center = reckon(50, 180, my_location[0], my_location[1], unit="nmi")
                unit.area = Area.create_patrol_area_from_center(center, 100, 100, unit='nmi')
            if bool(unit.contacts) and unit.target is None:
                target_contact = determine_priority_target_contact(unit.contacts, method='range')
                if target_contact is not None:
                    unit.target = target_contact.target_name_truth
            if unit.target:
                target_contact = unit.contacts.get(unit.target, None)
                if target_contact is not None:
                    unit.target_located = True
                    unit.target_location = (target_contact.latitude, target_contact.longitude)
                    unit.state = State.ENGAGE
                else:
                    unit.target = None
                    unit.group.leader.target_located = False
                    unit.group.leader.target_location = None
            else:
                patrol(unit)
                unit.state = State.PATROL

        if unit.state is State.ENGAGE:
            if bool(unit.contacts) and unit.target is None:
                target_contact = determine_priority_target_contact(unit.contacts, method='range')
                if target_contact is not None:
                    unit.target = target_contact.target_name_truth
            if unit.target:
                target_contact = unit.contacts.get(unit.target, None)
                if target_contact is not None:
                    pursue_target(unit, target_contact, standoff_range_m=0)
                else:
                    unit.target = None
            else:
                patrol(unit)
                unit.state = State.PATROL
    else:  # for not lead units, just feed lead contacts
        if bool(unit.contacts):
            for target in unit.contacts:
                contact = unit.contacts[target]
                message = DetectionMessage(contact, simulation_manager.now)
                unit.network.send_message(message, unit, unit.group.leader)

    unit.kinematics.set_speed(kts_to_ms(20))


def behavior_baseline(unit, simulation_manager):
    """
    Just follow the baseline route you are initialized with
    """
    if unit.group.leader is unit:
        if unit.state is State.PATROL:
            if unit.area is None:
                # establish patrol area 100 miles away from enemy territory
                my_location = unit.kinematics.get_location()
                center = reckon(0, 0, my_location[0], my_location[1], unit="nmi")
                unit.area = Area.create_patrol_area_from_center(center, 100, 100, unit='nmi')
            if bool(unit.contacts) and unit.target is None:
                target_contact = determine_priority_target_contact(unit.contacts, method='range')
                if target_contact is not None:
                    unit.target = target_contact.target_name_truth
            if unit.target:
                target_contact = unit.contacts.get(unit.target, None)
                if target_contact is not None:
                    unit.target_located = True
                    unit.target_location = (target_contact.latitude, target_contact.longitude)
                    unit.state = State.ENGAGE
                else:
                    unit.target = None
                    unit.group.leader.target_located = False
                    unit.group.leader.target_location = None
            else:
                patrol(unit)
                unit.state = State.PATROL

        if unit.state is State.ENGAGE:
            if bool(unit.contacts) and unit.target is None:
                target_contact = determine_priority_target_contact(unit.contacts, method='range')
                if target_contact is not None:
                    unit.target = target_contact.target_name_truth
            if unit.target:
                target_contact = unit.contacts.get(unit.target, None)
                if target_contact is not None:
                    pursue_target(unit, target_contact, standoff_range_m=0)
                else:
                    unit.target = None
            else:
                patrol(unit)
                unit.state = State.PATROL
    else:  # for not lead units, just feed lead contacts
        if bool(unit.contacts):
            for target in unit.contacts:
                contact = unit.contacts[target]
                message = DetectionMessage(contact, simulation_manager.now)
                unit.network.send_message(message, unit, unit.group.leader)

    unit.kinematics.set_speed(kts_to_ms(20))
