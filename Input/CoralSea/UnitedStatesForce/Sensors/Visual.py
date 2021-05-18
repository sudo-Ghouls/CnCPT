# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


from CnCPT.Simulation.Sensors.Sensor import Sensor


class VisualSurface(Sensor):
    def __init__(self):
        super().__init__(name=self.__class__.__name__)
        self.pd = 100
        self.sense_rate = 1 * 60
        self.max_range = 15 * 1000  # 15 km


class VisualAir(Sensor):
    def __init__(self):
        super().__init__(name=self.__class__.__name__)
        self.pd = 100
        self.sense_rate = 1 * 60
        self.max_range = 80 * 1000  # 80 km
