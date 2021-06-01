# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from Simulation.GeographyPhysics.core import haversine, bearing
from Simulation.GeographyPhysics.Geography import Geography

class Route:
    def __init__(self, waypoints):
        self.waypoints = waypoints
        self.idx = 1
        self.direction = 0  # 0 is nominal, 1 is reversed
        self.last_dis = 0
        self.last_bear = None

    def _get_next_waypoint(self):
        if self.idx == 0 and self.direction:
            self.direction = 0
        elif self.idx == len(self.waypoints) - 1 and not self.direction:
            self.direction = 1
        if not self.direction:
            self.idx = self.idx + 1
            return self.waypoints[self.idx]
        else:
            self.idx = self.idx - 1
            return self.waypoints[self.idx]

    def propagate_on_route(self, unit, time_step):
        unit_loc = unit.kinematics.get_location()
        unit_distance_traveled = unit.kinematics.get_speed() * time_step
        distance_to_travel = unit_distance_traveled
        waypoint = unit.route.waypoints[unit.route.idx]
        dist_to_waypoint, bear_to_waypoint = haversine(unit_loc, waypoint), \
                                             bearing(unit_loc, waypoint)
        if dist_to_waypoint <= distance_to_travel:
            next_waypoint = self._get_next_waypoint()
            bear_to_next_waypoint = bearing(waypoint, next_waypoint)
            distance_to_travel -= dist_to_waypoint
            new_lat, new_lon = Geography.reckon(distance_to_travel, bear_to_next_waypoint, waypoint[0], waypoint[1])
            unit.kinematics.set_location(lat=new_lat, lon=new_lon)
            unit.kinematics.set_heading(bear_to_waypoint)
        else:
            new_lat, new_lon = Geography.reckon(distance_to_travel, bear_to_waypoint, unit_loc[0], unit_loc[1])
            unit.kinematics.set_location(lat=new_lat, lon=new_lon)
            unit.kinematics.set_heading(bear_to_waypoint)
        return distance_to_travel
