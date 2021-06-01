# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


def adjudicate(simulation_manager):
    """

    :param simulation_manager:
    :return:
    """
    if len(simulation_manager.all_units) == 0:
        return
    units_with_weapons = simulation_manager.unit_filter.filter(alive=True, armed=True, docked=False)
    for unit in units_with_weapons:
        for weapon in unit.weapons:
            weapon.engage(unit, simulation_manager)
