# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


class BasicBehavior:
    def __init__(self):
        pass

    @staticmethod
    def RouteFollowing(unit, simulation_manager):
        pass


def spawn(simulation_manager):
    """

    :return:
    """
    for unit in simulation_manager.all_units:
        if bool(unit.spawn):
            for new_unit_key in unit.spawn:
                new_unit = unit.spawn[new_unit_key]
                new_unit.network = unit.network
                new_unit.kinematics.set_location(unit=unit)
                new_unit.register(simulation_manager, simulation_manager.constants)
                simulation_manager.all_units.append(new_unit)
            unit.spawn = {}


def update_state(simulation_manager):
    """
    This function maintains the state of all units in the scenario
    :return:
    """
    simulation_manager.Geography.update(simulation_manager.all_units)
    simulation_manager.unit_filter.ingest(list(simulation_manager.all_units))
