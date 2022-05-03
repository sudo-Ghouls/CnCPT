# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


import sys
import uuid


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
            if self.engagements_conducted >= self.max_engagements:
                return
            target = simulation_manager.all_units_map[target_name]
            if not isinstance(target, self.viable_target_classes):
                continue
            if target.side is parent_unit.side:
                continue
            if target in self.engagement_history_dict.keys():
                # check if unit has been shot at yet,
                time_elapsed = simulation_manager.now - self.engagement_history_dict[target]
                if time_elapsed >= self.engagement_rate:
                    target_killed, pk_diceroll = self.calculate_pk(simulation_manager, target=target)
                    self.engagements_conducted += 1
                    self.update_weapon_log(target_killed, parent_unit, simulation_manager, ranges[idx], target,
                                           pk_diceroll)
                    self.engagement_history_dict[target] = simulation_manager.now
                else:
                    continue
            else:
                target_killed, pk_diceroll = self.calculate_pk(simulation_manager, target=target)
                self.update_weapon_log(target_killed, parent_unit, simulation_manager, ranges[idx], target, pk_diceroll)
                self.engagement_history_dict[target] = simulation_manager.now
                self.engagements_conducted += 1
            if target_killed is True:
                targets_killed.append(target)
                simulation_manager.kill_log[target] = {"target": target.name,
                                                       "target_side": target.side.name,
                                                       "target_class": target.__class__.__name__,
                                                       "target_type": target.my_type,
                                                       "time_sec": simulation_manager.now,
                                                       "weapon": self.__class__.__name__,
                                                       "shooter": parent_unit.name,
                                                       "shooter_side": parent_unit.side.name,
                                                       "shooter_class": parent_unit.__class__.__name__,
                                                       "shooter_type": parent_unit.my_type,
                                                       "range_m": ranges[idx]}

        # now kill all the units that died in the last set of salvos
        for target_killed in targets_killed:
            target_name = target_killed.name
            simulation_manager.all_units_map[target_name].alive = False

    def calculate_pk(self, simulation_manager, **kwargs):
        dice_roll = simulation_manager.random.random_sample()
        if dice_roll < self.pk:
            return True, dice_roll
        return False, dice_roll

    def update_weapon_log(self, target_killed, parent_unit, simulation_manager, range, target, pk_diceroll):
        engagement_uuid = uuid.uuid1()
        plat, plon = parent_unit.kinematics.get_location()
        tlat, tlon = target.kinematics.get_location()
        simulation_manager.weapon_log[engagement_uuid] = {"target_killed": target_killed,
                                                          "pk_diceroll": pk_diceroll,
                                                          "shooter_side": parent_unit.side.name,
                                                          "shooter_name": parent_unit.name,
                                                          "shooter_class": parent_unit.__class__.__name__,
                                                          "shooter_type": parent_unit.my_type,
                                                          "shooter_location_lat": plat,
                                                          "shooter_location_lon": plon,
                                                          "range": range,
                                                          "target_side": target.side.name,
                                                          "target_name": target.name,
                                                          "target_class": target.__class__.__name__,
                                                          "target_type": target.my_type,
                                                          "target_location_lat": tlat,
                                                          "target_location_lon": tlon}
