# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

import numpy as np
from shapely.geometry import Point

earth_radius = 6378.1  # km
# Unit values taken from http://www.unitconversion.org/unit_converter/length.html
_CONVERSIONS = {"km": 1.0,
                "m": 1000.0,
                "mi": 0.621371192,
                "nmi": 0.539956803,
                "ft": 3280.839895013,
                "in": 39370.078740158}


def wrapto360(angle):
    return (angle + 360) % 360


def bearing_change(ang1, ang2):
    ang1 = wrapto360(ang1)
    ang2 = wrapto360(ang2)
    max_ang = max((ang1, ang2))
    min_ang = min((ang1, ang2))
    return wrapto360(max_ang - min_ang)


def propagate(simulation_manager):
    """
    This function propagates all units forward in time based on their current velocity and heading
    :return:
    """
    if len(simulation_manager.all_units) == 0:
        return
    units_to_propagate = simulation_manager.unit_filter.filter(alive=True, moving=True, docked=False)

    for unit in units_to_propagate:
        distance_propagated = Geography.propagate(unit, simulation_manager.time_step)
        unit.kinematics.update_range_traveled(distance_propagated)
    # list(map(Geography.propagate, units_to_propagate, itertools.repeat(simulation_manager.time_step, len(units_to_propagate))))

    units_currently_docked = simulation_manager.unit_filter.filter(alive=True, docked=True)
    for unit in units_currently_docked:
        if unit.parent is not None:
            if unit.docked is True:
                unit.kinematics.set_location(unit=unit.parent)
            else:
                unit.docked = False


def haversine(point1, point2, unit='m'):
    # convert all latitudes/longitudes to radians
    if isinstance(point1, Point):
        lat1, lon1 = np.radians(point1.coords[0][0]), np.radians(point1.coords[0][1])
    else:
        lat1, lon1 = np.radians(point1[0]), np.radians(point1[1])
    if isinstance(point2, Point):
        lat2, lon2 = np.radians(point2.coords[0][0]), np.radians(point2.coords[0][1])
    else:
        lat2, lon2 = np.radians(point2[0]), np.radians(point2[1])

    # calculate haversine
    lat = lat2 - lat1
    lon = lon2 - lon1
    d = np.sin(lat * 0.5) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(lon * 0.5) ** 2
    return 2 * earth_radius * _CONVERSIONS[unit] * np.arcsin(np.sqrt(d))


def bearing(point1, point2):
    # convert all latitudes/longitudes to radians
    if isinstance(point1, Point):
        lat1, lon1 = np.radians(point1.coords[0][0]), np.radians(point1.coords[0][1])
    else:
        lat1, lon1 = np.radians(point1[0]), np.radians(point1[1])
    if isinstance(point2, Point):
        lat2, lon2 = np.radians(point2.coords[0][0]), np.radians(point2.coords[0][1])
    else:
        lat2, lon2 = np.radians(point2[0]), np.radians(point2[1])
    # calculate bearing
    dlon = lon2 - lon1
    ang_rad = np.arctan2(np.sin(dlon) * np.cos(lat2), np.cos(lat1) * np.sin(lat2) - np.sin(
        lat1) * np.cos(lat2) * np.cos(dlon))
    ang_deg = np.degrees(ang_rad)

    return ang_deg
