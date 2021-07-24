# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


import sys


class Weapon:
    def __init__(self, name, amount=sys.maxsize):
        self.name = name
        self.max_engagements = amount
        self.engagements_conducted = 0
        self.pk = None
        self.engagement_rate = None  # in seconds
        self.max_range = None  # in meters
        self.engagement_history_dict = {}
        self.viable_target_classes = ()

    def reload(self):
        self.engagements_conducted = 0

    def engage(self, parent_unit, simulation_manager):
        if self.engagements_conducted >= self.max_engagements:
            return
        targets_killed = []
        targets_in_range, ranges = simulation_manager.Geography.targets_in_range(parent_unit, self.max_range)
        for idx, target_name in enumerate(targets_in_range):
            target = simulation_manager.all_units_map[target_name]
            if not isinstance(target, self.viable_target_classes):
                continue
            if target.side is parent_unit.side:
                continue
            if target in self.engagement_history_dict.keys():
                # check if unit has been shot at yet,
                time_elapsed = simulation_manager.now - self.engagement_history_dict[target]
                if time_elapsed >= self.engagement_rate:
                    target_killed = self.calculate_pk(simulation_manager, target=target)
                    self.engagements_conducted += 1
                    self.update_weapon_log(target_killed, parent_unit, simulation_manager)
                    self.engagement_history_dict[target] = simulation_manager.now
                else:
                    continue
            else:
                target_killed = self.calculate_pk(simulation_manager, target=target)
                self.update_weapon_log(target_killed, parent_unit, simulation_manager)
                self.engagement_history_dict[target] = simulation_manager.now
            if target_killed is True:
                targets_killed.append(target)
                simulation_manager.kill_log[target] = {"Target_Side": target.side.name,
                                                       "Time_sec": simulation_manager.now,
                                                       "Weapon": self.__class__.__name__,
                                                       "Shooter": parent_unit.name,
                                                       "Shooter_Class": parent_unit.__class__.__name__,
                                                       "Shooter_Side": parent_unit.side.name,
                                                       "Range_m": ranges[idx]}

        # now kill all the units that died in the last set of salvos
        for target_killed in targets_killed:
            target_name = target_killed.name
            simulation_manager.all_units_map[target_name].alive = False

    def calculate_pk(self, simulation_manager, **kwargs):
        dice_roll = simulation_manager.random.random_sample()
        if dice_roll < self.pk:
            return True
        return False

    def update_weapon_log(self, target_killed, parent_unit, simulation_manager):
        try:
            if target_killed:
                simulation_manager.weapon_log[parent_unit.side][self]['Success'] += 1
            else:
                simulation_manager.weapon_log[parent_unit.side][self]['Failure'] += 1
        except KeyError:
            try:
                if target_killed:
                    simulation_manager.weapon_log[parent_unit.side][self]['Success'] = 1
                else:
                    simulation_manager.weapon_log[parent_unit.side][self]['Failure'] = 1
            except KeyError:
                try:
                    if target_killed:
                        simulation_manager.weapon_log[parent_unit.side][self] = {'Success': 1}
                    else:
                        simulation_manager.weapon_log[parent_unit.side][self] = {'Failure': 1}
                except KeyError:
                    if target_killed:
                        simulation_manager.weapon_log[parent_unit.side] = {self: {'Success': 1}}
                    else:
                        simulation_manager.weapon_log[parent_unit.side] = {self: {'Failure': 1}}
