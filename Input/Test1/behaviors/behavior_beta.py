# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


def BehaviorB(unit, simulation_manager):
    # print('Unit: {0} ran behavior B\n'.format(unit.name))
    unit.kinematics.set_heading(90)
    unit.kinematics.set_speed(10)
