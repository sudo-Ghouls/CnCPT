# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


def sense(simulation_manager, max_retention_time=12000):
    """
    evaluates all the sensing capability on board units in the scenario
    :param simulation_manager:
    :param max_retention_time: hold time for contacts in seconds
    :return:
    """
    if len(simulation_manager.all_units) == 0:
        return
    units_with_sensors = simulation_manager.unit_filter.filter(alive=True, has_sensors=True, docked=False)
    for unit in units_with_sensors:
        for sensor in unit.sensors:
            sensor.process(unit, simulation_manager)
            update_contacts(sensor.contacts, simulation_manager.now, max_retention_time)
            unit.contacts.update(sensor.contacts)


def update_system_contacts(simulation_manager, max_retention_time=12000):
    """
        removes old (based on max retention time and dead contacts from a units contact list (cheats using truth
        data)
    :param simulation_manager:
    :param max_retention_time: hold time for contacts in seconds
    :return:
    """

    units_with_contacts = simulation_manager.unit_filter.filter(alive=True, has_contacts=True, docked=False)

    for unit in units_with_contacts:
        update_contacts(unit.contacts, simulation_manager.now, max_retention_time)


def update_contacts(contacts, current_time, max_retention_time):
    """

    :param contacts:
    :param current_time:
    :param max_retention_time:
    :return:
    """
    keys_to_pop = []
    for contact_key in contacts:
        time_elapsed = current_time - contacts[contact_key].time
        if time_elapsed > max_retention_time:
            keys_to_pop.append(contact_key)
        if contacts[contact_key].truth_unit.alive is False:
            keys_to_pop.append(contact_key)

    for key in keys_to_pop:
        _ = contacts.pop(key, None)
