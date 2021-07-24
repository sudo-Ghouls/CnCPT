# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


from Simulation.Units.BaseClasses import Aircraft
from Simulation.Units.BaseClasses.Ship import Ship
from Simulation.Utility.SideEnum import SideEnum


def post_process(simulation_manager):
    red_units = [unit for unit in simulation_manager.all_units if unit.side is SideEnum.RED]
    red_ships = [unit for unit in red_units if isinstance(unit, Ship)]
    red_aircraft = [unit for unit in red_units if isinstance(unit, Aircraft)]

    blue_units = [unit for unit in simulation_manager.all_units if unit.side is SideEnum.BLUE]
    blue_ships = [unit for unit in blue_units if isinstance(unit, Ship)]
    blue_aircraft = [unit for unit in blue_units if isinstance(unit, Aircraft)]

    # blue_weapon_log = simulation_manager.weapon_log[SideEnum.BLUE]
    # red_weapon_log = simulation_manager.weapon_log[SideEnum.RED]
    kill_log = simulation_manager.kill_log
    # isr_log = simulation_manager.isr_log
    vsm_ships = variable_survivability_metric(blue_ships)
    vsm_aircraft = variable_survivability_metric(blue_aircraft)
    vscm_ships = variable_survivability_cost_metric(blue_ships)
    vscm_aircraft = variable_survivability_cost_metric(blue_aircraft)
    vscm_blue = variable_survivability_cost_metric(blue_units)

    # vimm = variable_ISR_measure_metric(red_units, isr_log)
    # vwum = variable_weapon_utilization_metric(blue_weapon_log)

    fam_ships = fixed_attrition_metric(red_ships)
    fam_aircraft = fixed_attrition_metric(red_aircraft)
    facm_ships = fixed_attrition_cost_metric(red_ships)
    facm_aircraft = fixed_attrition_cost_metric(red_aircraft)
    facm_red = fixed_attrition_cost_metric(red_units)
    # fimm = fixed_ISR_measure_metric(blue_units, isr_log)
    # fwum = fixed_weapon_utilization_metric(red_weapon_log)

    # assume equal weights for all 10 metrics
    # score = np.mean([vsm_ships,
    #                  vsm_aircraft,
    #                  vscm_ships,
    #                  vscm_aircraft,
    #                  fam_ships,
    #                  fam_aircraft,
    #                  facm_ships,
    #                  facm_aircraft])
    # score = np.mean([fam_ships,
    #                  fam_aircraft,
    #                  facm_ships,
    #                  facm_aircraft])

    score = .2 * (vscm_blue) + .80 * (facm_red)

    # score = np.mean([vsm, vsrm, vscm, vimm, vwum, fam, farm, facm, fimm, fwum])
    results = {"score": score,
               "vsm_ships": vsm_ships,
               "vsm_aircraft": vsm_aircraft,
               "vscm_ships": vscm_ships,
               "vscm_aircraft": vscm_aircraft,
               "vscm_blue": vscm_blue,
               "fam_ships": fam_ships,
               "fam_aircraft": fam_aircraft,
               "facm_ships": facm_ships,
               "facm_aircraft": facm_aircraft,
               "facm_red": facm_red}
    return results


def variable_survivability_metric(blue_units):
    """ Max score is 100 and only achievable if all blue platforms survive the scenario

    """
    total_num_blue = len(blue_units)
    if total_num_blue == 0:
        return 100
    num_alive = len([unit for unit in blue_units if unit.alive is True])
    return (num_alive / total_num_blue) * 100.0


def variable_survivability_cost_metric(blue_units):
    """

    """
    total_cost = sum([unit.cost for unit in blue_units])
    if total_cost == 0:
        return 100
    realized_cost = sum([unit.cost for unit in blue_units if unit.alive is False])
    return (1 - (realized_cost / total_cost)) * 100.0


def variable_ISR_measure_metric(red_units, isr_log):
    """

    """
    pass


def variable_weapon_utilization_metric(blue_weapon_log):
    """

    """
    pass


def fixed_attrition_metric(red_units):
    """

    """
    total_num_red = len(red_units)
    if total_num_red == 0:
        return 100
    num_killed = len([unit for unit in red_units if unit.alive is False])
    return (num_killed / total_num_red) * 100.0


def fixed_attrition_cost_metric(red_units):
    """

    """
    total_cost = sum([unit.cost for unit in red_units])
    if total_cost == 0:
        return 100
    realized_cost = sum([unit.cost for unit in red_units if unit.alive is False])
    return (realized_cost / total_cost) * 100.0


def fixed_ISR_measure_metric(blue_units, isr_log):
    """

    """
    pass


def fixed_weapon_utilization_metric(red_weapon_log):
    """

    """
    pass
