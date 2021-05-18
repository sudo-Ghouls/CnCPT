# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


def BehaviorC(unit, simulation_manager):
    # print('Unit: {0} ran behavior C\n'.format(unit.name))
    unit.kinematics.set_heading(20 + simulation_manager.now)
    unit.kinematics.set_speed(5)
