# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE
from Simulation.Units.UnitGroup import UnitGroup


class Architecture:
    def __init__(self, units, name, side=None, code=None):
        self.units = units
        self.name = name
        self.side = side
        self.code = code

    @staticmethod
    def create_from_code(code, manager, side, name):
        units_ungrouped, units_grouped, code_idx, polygon_groups = [], [], 0, {}
        unit_keys = manager.CompCon.units.keys()
        max_num_per_unit = [manager.CompCon.units[unit].maxNumber for unit in unit_keys]
        for class_idx, UnitClass in enumerate(unit_keys):
            for unit_idx in range(max_num_per_unit[class_idx]):
                if code[code_idx] is not None:
                    unit_name = "{0}_{1}_{2}".format(side.name, UnitClass.__name__, unit_idx)
                    unit_behavior = manager.CONOPCon.units[UnitClass].CONOPs[code[code_idx]]
                    spawn_polygon = manager.CompCon.units[UnitClass].Polygons[code[code_idx + 1]]
                    new_unit = UnitClass(name=unit_name, behavior=unit_behavior, spawn_polygon=spawn_polygon, side=side)
                    update_polygon_group(new_unit, spawn_polygon, polygon_groups)
                    units_ungrouped.append(new_unit)
                code_idx += 2

        sort_polygon_group_by_leadership(polygon_groups, manager.LeadershipPriority)
        for idx, polygon_group in enumerate(polygon_groups):
            polygon_unit_group = UnitGroup.construct_unit_group("Polygon_{0}".format(idx + 1),
                                                                polygon_groups[polygon_group],
                                                                leader=polygon_groups[polygon_group][0])
            units_grouped += polygon_unit_group
        return Architecture(units_grouped, name, side, code)


def update_polygon_group(unit, spawn_polygon, polygon_groups_dict):
    if spawn_polygon.name in polygon_groups_dict.keys():
        polygon_groups_dict[spawn_polygon.name].append(unit)
    else:
        polygon_groups_dict[spawn_polygon.name] = [unit]


def sort_polygon_group_by_leadership(polygon_groups, leadership_priority):
    rank_map, rank = {}, 1
    for unit_class in leadership_priority:
        rank_map[unit_class] = rank
        rank += 1

    for polygon_group in polygon_groups:
        units = polygon_groups[polygon_group]
        units_rank = [rank_map[unit.__class__] for unit in units]
        units_sorted = [u for _, u in sorted(zip(units_rank, units), key=lambda x: x[0])]
        polygon_groups[polygon_group] = units_sorted
