# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


class Sensor:
    def __init__(self, name):
        self.parent_unit = None  # updated when added to unit
        self.name = name
        self.pd = None
        self.sense_rate = None
        self.max_range = None
        self.contacts = {}

    def process(self, parent_unit, simulation_manager):
        self.detect(parent_unit, simulation_manager)

    def detect(self, parent_unit, simulation_manager):
        targets_detected, target_ranges = [], []
        targets_in_range, ranges = simulation_manager.Geography.targets_in_range(parent_unit, self.max_range)

        for idx, target_name in enumerate(targets_in_range):
            target = simulation_manager.all_units_map[target_name]
            if target.side is parent_unit.side:
                continue
            target_detected = self.calculate_pd(simulation_manager, target=target, )
            if target_detected is True:
                targets_detected.append(target)
                target_ranges.append(ranges[idx])
                try:
                    simulation_manager.isr_log[target] += 1
                except KeyError:
                    simulation_manager.isr_log[target] = 1

        for idx, target_detected in enumerate(targets_detected):
            self.contacts[target_detected.name] = Contact(target_detected, target_ranges[idx], simulation_manager)

    def calculate_pd(self, simulation_manager, **kwargs):
        dice_roll = simulation_manager.random.random_sample()
        if dice_roll < self.pd:
            return True
        return False


class Contact:
    def __init__(self, truth_unit, target_range, simulation_manager):
        self.target_name_truth = truth_unit.name
        self.distance_to = target_range
        self.truth_unit = truth_unit
        self.latitude, self.longitude = self.truth_unit.kinematics.get_location()
        self.time = simulation_manager._now
