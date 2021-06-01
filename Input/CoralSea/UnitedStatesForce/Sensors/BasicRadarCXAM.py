# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


from Simulation.Sensing.Sensor import Sensor


class BasicRadarCXAM(Sensor):
    def __init__(self):
        super().__init__(name=self.__class__.__name__)
        self.pd = 50
        self.sense_rate = 10 * 60
        self.max_range = 40 * 1000  # 40 km
