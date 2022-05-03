# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from Simulation.Units.BaseClasses.Aircraft import Aircraft
from Simulation.Communication.Message import DetectionMessage
from Simulation.Logic.ChildLogic import return_to_parent
from Simulation.Logic.General import determine_priority_target_contact, pursue_target
from Simulation.Logic.Patrol import patrol
from Simulation.Units.State import State


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
            if target_contact is not None:
                unit.target = target_contact.target_name_truth
        if unit.target:
            target_contact = unit.contacts.get(unit.target, None)
            if target_contact is not None:
                unit.parent.target_located = True
                unit.parent.target_location = (target_contact.latitude, target_contact.longitude)
                message = DetectionMessage(target_contact, simulation_manager.now)
                unit.network.send_message(message, unit, unit.parent)
                return_to_parent(unit, simulation_manager.now)
            else:
                unit.target = None
                unit.parent.target_located = False
                unit.parent.target_location = None
        else:
            patrol(unit)

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

    if unit.state is State.RTB:
        return_to_parent(unit, simulation_manager.now)
