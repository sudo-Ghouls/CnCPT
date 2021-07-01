# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from shapely.geometry import Point

from Simulation.GeographyPhysics.core import haversine, bearing, wrapto360


def pursue_target(unit, target_contact, standoff_range_m=10000):
    """
    :param unit:
    :param target_contact:
    :param standoff_range_m:
    :return:
    """
    my_location = Point(unit.kinematics.get_location())
    target_location = Point(target_contact.latitude, target_contact.longitude)
    distance_to_target = haversine(my_location, target_location)
    if distance_to_target > standoff_range_m:
        bearing_to_go = bearing(my_location, target_location)
    else:
        bearing_to_go = wrapto360(bearing(my_location, target_location) - 180.0)
    unit.kinematics.set_heading(bearing_to_go)


def determine_priority_target_contact(contact_list, method='range', class_priority_map=None, excluded_classes=None):
    """
    :param contact_list: list or dict of contact objects
    :param method: string for sorting method
        "range" - returns the closest contact\
        "priority" - returns the highest priority contact, ties sort secondarily based on range
    :param class_priority_map: {class: rank}
        i.e. {Carrier : 1,
              Destroyer: 2}
    :return: target_contact: contact object of highest priority target
    """
    if type(contact_list) is dict:
        contacts = list(contact_list.values())
    elif type(contact_list) is list:
        contacts = contact_list
    else:
        raise Exception("Contact List is not supported type ({0})".format(type(contact_list)))

    if method == "priority" and class_priority_map is None:
        raise Exception("Priority map needed for method = priority".format(type(contact_list)))

    if method == "priority":
        data = {}
        for contact in contacts:
            data[contact] = class_priority_map.get(contact.truth_unit.__class__, 10000000)
        if not bool(data):
            return None
        sorted_contacts = dict(sorted(data.items(), key=lambda item: item[1]))
        target_contact = next(iter(sorted_contacts))
        return target_contact

    if method == "range":
        data = {}
        for contact in contacts:
            if excluded_classes is not None:
                if not isinstance(contact.truth_unit, excluded_classes):
                    data[contact] = contact.distance_to
            else:
                data[contact] = contact.distance_to
        if not bool(data):
            return None
        sorted_contacts = dict(sorted(data.items(), key=lambda item: item[1]))
        target_contact = next(iter(sorted_contacts))
        return target_contact


DAY_START = 6 * 60 * 60  # 6 AM
DAY_END = 20 * 60 * 60  # 8 PM
DAY_LENGTH = 24 * 60 * 60  # 24 hours


def is_day(time):
    time_of_day = time % DAY_LENGTH
    if DAY_START < time_of_day < DAY_END:
        return True
    else:
        return False
