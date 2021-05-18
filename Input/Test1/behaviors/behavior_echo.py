# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


def BehaviorE(unit, simulation_manager):
    # print('Unit: {0} ran behavior E\n'.format(unit.name))
    unit.kinematics.set_heading(200)
    unit.kinematics.set_speed(10)
