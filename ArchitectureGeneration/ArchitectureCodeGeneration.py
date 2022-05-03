# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

import random as r

import numpy as np
import pandas as pd


def generateBaseArchCode(simulation_manager):
    comp_con_list = simulation_manager.CompCon.units.keys()
    simulation_manager.max_num_per_unit = [simulation_manager.CompCon.units[unit].maxNumber for unit in comp_con_list]
    simulation_manager.num_loc_polys = [int(len(simulation_manager.CompCon.units[unit].Polygons)) for unit in
                                        comp_con_list]
    simulation_manager.conop_con_list = simulation_manager.CONOPCon.units.keys()
    simulation_manager.max_conop_per_unit = [simulation_manager.CONOPCon.units[unit].maxNumConop for unit in
                                             simulation_manager.conop_con_list]
    base_arch_code = []
    for idx, Unit in enumerate(comp_con_list):
        base_arch_code.extend([simulation_manager.max_conop_per_unit[idx], simulation_manager.num_loc_polys[idx]] * (
            simulation_manager.max_num_per_unit[idx]))  # two b/c one 0 for behavior one 0 for loc
    return base_arch_code


def generateAllArchCodes(simulation_manager):
    comp_con_list = simulation_manager.CompCon.units.keys()
    lower_bound_per_unit = [simulation_manager.CompCon.units[unit].lowerBound for unit in comp_con_list]
    upper_bound_per_unit = [simulation_manager.CompCon.units[unit].upperBound for unit in comp_con_list]
    ArchCodes = GenerateArchCode(simulation_manager.base_arch_code, lower_bound_per_unit, upper_bound_per_unit,
                                 simulation_manager.num_loc_polys,
                                 simulation_manager.max_conop_per_unit)
    return ArchCodes


def MaximumIdxFromCons(simulation_manager, NumLocPolys, MaxConopPerUnit):
    all_cons = np.concatenate((NumLocPolys, MaxConopPerUnit))
    return max(all_cons)


def GenerateArchCode(BaseArchCode, LowerBoundPerUnit, UpperBoundPerUnit, NumLocPolys, MaxConopPerUnit):
    possible_arch_codes, arch_codes = [], []
    ref_unit_code = generate_unit_code_map(LowerBoundPerUnit, UpperBoundPerUnit)
    for Col in range(len(BaseArchCode)):
        if Col % 2 == 0:
            ref_unit = ref_unit_code[Col]
            if LowerBoundPerUnit[ref_unit] == UpperBoundPerUnit[ref_unit]:
                options = list(range(BaseArchCode[Col]))
            else:
                options = [-1] + list(range(BaseArchCode[Col]))  # Behavior Choice
        else:
            options = list(range(BaseArchCode[Col]))
        if len(possible_arch_codes) == 0:
            possible_arch_codes = np.vstack(np.array(r.choices(options, k=10000)))
        else:
            possible_arch_codes = np.concatenate(
                (possible_arch_codes, np.vstack(np.array(r.choices(options, k=10000)))), axis=1)
        # Loop ever every second column setting value equal to None if related Behavior is None
        if Col % 2 == 1:
            for Row in range(np.size(possible_arch_codes, 0)):
                if possible_arch_codes[Row, Col - 1] == -1:
                    possible_arch_codes[Row, Col] = -1

    for ArchCode in possible_arch_codes:
        if ValidArch(ArchCode, LowerBoundPerUnit, UpperBoundPerUnit, NumLocPolys, MaxConopPerUnit):
            if len(arch_codes) == 0:
                arch_codes = ArchCode
            else:
                arch_codes = np.append(arch_codes, ArchCode, axis=0)
    arch_codes = np.reshape(arch_codes, (int(int(len(arch_codes)) / len(BaseArchCode)), len(BaseArchCode)))
    arch_codes = pd.DataFrame(arch_codes).drop_duplicates().values
    return arch_codes


def generate_unit_code_map(LowerBoundPerUnit, UpperBoundPerUnit):
    ref_unit_code = []
    start_idx = 0
    for Unit_i in range(len(LowerBoundPerUnit)):
        max_num_of_unit_i = UpperBoundPerUnit[Unit_i]
        end_idx = start_idx + max_num_of_unit_i * 2
        unit_id_array = [Unit_i] * (end_idx - start_idx)
        ref_unit_code += (unit_id_array)
        start_idx = end_idx
    return ref_unit_code


def ValidArch(ArchCode, LowerBoundPerUnit, UpperBoundPerUnit, NumLocPolys, MaxConopPerUnit):
    # ArchCode = np.array([1,2,3,4,5,6,7,8,9,10])
    if next(iter(set(ArchCode))) is None:
        return False
    start_idx = 0
    for Unit_i in range(len(LowerBoundPerUnit)):
        max_num_of_unit_i = UpperBoundPerUnit[Unit_i]
        end_idx = start_idx + max_num_of_unit_i * 2
        # Check if Behavior Columns are Valid
        unit_i_behaviors = ArchCode[start_idx:end_idx:2]
        if next(iter(set(unit_i_behaviors))) == -1:
            if LowerBoundPerUnit[Unit_i] > 0:
                return False
        else:
            if len([i for i in unit_i_behaviors if i >= 0]) < LowerBoundPerUnit[Unit_i]:
                return False
            if max([i for i in unit_i_behaviors if i >= 0]) > MaxConopPerUnit[Unit_i] - 1:
                return False
        # Check if Location Columns are Valid
        unit_i_locations = ArchCode[start_idx + 1:end_idx:2]
        if next(iter(set(unit_i_locations))) < 0:
            if LowerBoundPerUnit[Unit_i] > 0:
                return False
        else:
            if len([i for i in unit_i_locations if i >= 0]) < LowerBoundPerUnit[Unit_i]:
                return False
            if max([i for i in unit_i_locations if i >= 0]) > NumLocPolys[Unit_i] - 1:
                return False

        unit_i_info = np.vstack((unit_i_behaviors, unit_i_locations))
        for i in range(np.size(unit_i_info, 1)):
            if len(set(unit_i_info[:, i])) > 1:
                if None in set(unit_i_info[:, i]):
                    return False
        start_idx = end_idx
    return True
