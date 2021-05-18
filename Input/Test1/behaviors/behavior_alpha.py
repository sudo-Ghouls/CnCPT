# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

import random

def BehaviorA(unit, simulation_manager):
    # print('Unit: {0} ran behavior A\n'.format(unit.name))
    if divmod(simulation_manager.now, 3600)[1] < 1800:
        start = random.randint(0,360)
        unit.kinematics.set_heading(start + simulation_manager.now)
    unit.kinematics.set_speed(7)
