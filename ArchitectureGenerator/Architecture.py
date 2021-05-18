# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


class Architecture:
    def __init__(self, units, name, side=None, code=None):
        self.units = units
        self.name = name
        self.side = side
        self.code = code

    @staticmethod
    def create_from_code(code, manager, side, name):
        units, code_idx = [], 0
        unit_keys = manager.CompCon.units.keys()
        max_num_per_unit = [manager.CompCon.units[unit].maxNumber for unit in unit_keys]
        for class_idx, UnitClass in enumerate(unit_keys):
            for unit_idx in range(max_num_per_unit[class_idx]):
                if code[code_idx] is not None:
                    unit_name = "{0}_{1}_{2}".format(side.name, UnitClass.__name__, unit_idx)
                    unit_behavior = manager.CONOPCon.units[UnitClass].CONOPs[code[code_idx]]
                    spawn_polygon = manager.CompCon.units[UnitClass].Polygons[code[code_idx + 1]]
                    new_unit = UnitClass(name=unit_name, behavior=unit_behavior, spawn_polygon=spawn_polygon, side=side)
                    units.append(new_unit)
                code_idx += 2

        return Architecture(units, name, side, code)
