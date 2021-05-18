from CnCPT.Simulation.Units.Unit import Unit


class DDG(Unit):
    def __init__(self, name=None, behavior=None, location=None, spawn_polygon=None, side=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon, side=side)
        self.cost = 250
