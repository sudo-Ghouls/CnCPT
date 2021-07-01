# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

import json
import os
import sys


def truncate_6(f):
    return int(f * 1e6) / 1e6


def log(simulation_manager):
    """

    :return:
    """
    if simulation_manager.full_data_logging:
        simulation_manager.data_logger.dump_units_to_file(simulation_manager)
        simulation_manager.data_logger.update_formatted_unit_data(simulation_manager)


def update_status_bar(simulation_manager):
    """

    """
    fraction_complete = float(simulation_manager._now - simulation_manager.start_time) / (
            simulation_manager.end_time - simulation_manager.start_time)
    status = ""
    if fraction_complete >= 1:
        status = "Done.\r\n"
    num_blocks = int(round(25 * fraction_complete))
    bar_string = "#" * num_blocks + "-" * (25 - num_blocks)
    text_1 = "\r[{0}] {1:5.1f}%".format(bar_string, fraction_complete * 100)
    text_time = simulation_manager._now
    speed = ((simulation_manager._now - simulation_manager.start_time) / simulation_manager.elapsed_real_time)
    text_2 = "[Time: {0}] [Speed: {1} x Realtime] {2}".format(text_time, speed, status)
    text = text_1 + text_2
    try:
        sys.stdout.write((text).encode("utf8"))
    except TypeError:
        sys.stdout.write(text)
    sys.stdout.flush()


class DataLogger:
    def __init__(self, output_path):
        self.output_path = output_path
        self.unit_data_file = open(os.path.join(output_path, "unit_data.log"), "w")
        self.formatted_unit_data_file = open(os.path.join(output_path, "formatted_unit_data.log"), "w")
        self.add_json_file_starters()

        self.formatted_unit_data = {"UnitData": {},
                                    "MapBounds": []}

    def update_formatted_unit_data(self, simulation_manager):
        for unit in simulation_manager.all_units:
            time = simulation_manager.now
            if time not in self.formatted_unit_data["UnitData"].keys():
                self.formatted_unit_data["UnitData"][time] = {}
            if unit.name not in self.formatted_unit_data["UnitData"][time].keys():
                self.formatted_unit_data["UnitData"][time][unit.name] = self.extract_data_from_unit(unit, time)
            else:
                raise ValueError("Unit is already logged for this time")

    @staticmethod
    def extract_data_from_unit(unit, time):
        if unit.spawn_polygon is not None:
            spawn_poly = unit.spawn_polygon.bounds
        else:
            spawn_poly = None
        location = unit.kinematics.get_location()
        unit_data = {"time": time,
                     "alive": unit.alive,
                     "name": unit.name,
                     "side": unit.side.name,
                     "type": unit.__class__.__bases__[0].__name__,
                     "behavior": unit.my_brain.__name__,
                     "spawn_polygon": spawn_poly,
                     "location_x": truncate_6(location[0]),
                     "location_y": truncate_6(location[1]),
                     "heading": truncate_6(unit.kinematics.get_heading()),
                     "speed": truncate_6(unit.kinematics.get_speed()),
                     "cost": unit.cost,
                     "time_between_thoughts": unit.time_between_thoughts}
        return unit_data

    def dump_units_to_file(self, simulation_manager):
        for unit in simulation_manager.all_units:
            self.unit_data_file.write(json.dumps(self.extract_data_from_unit(unit, simulation_manager.now)) + ",\n")

    def add_json_file_starters(self):
        self.unit_data_file.write('{"data":[')

    def close_data_logger(self, simulation_manager):
        self.unit_data_file.write(
            '{' + '{0}:{1}'.format('"MapBounds"', list(simulation_manager.Geography.map.bounds))
            + '}]}')
        self.unit_data_file.close()

        self.formatted_unit_data["MapBounds"] = list(simulation_manager.Geography.map.bounds)
        self.formatted_unit_data_file.write(json.dumps(self.formatted_unit_data, indent=4))
        self.formatted_unit_data_file.close()
        self.unit_data_file.close()
