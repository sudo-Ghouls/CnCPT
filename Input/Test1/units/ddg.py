from Simulation.Units.Unit import Unit


class DDG(Unit):
    def __init__(self, name=None, behavior=None, location=None, spawn_polygon=None,
                 side=None, route=None, parent=None, network=None, group_data=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=side, route=route, parent=parent, network=network, group_data=group_data)
        self.cost = 250
