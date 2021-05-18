# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from CnCPT.Input.CoralSea.BaseClasses.Ship import Ship
from CnCPT.Input.CoralSea.JapaneseForce.Aircraft.DiveBomber import AichiD3AType99
from CnCPT.Input.CoralSea.JapaneseForce.Aircraft.Fighter import A6M2Zero
from CnCPT.Input.CoralSea.JapaneseForce.Aircraft.TorpedoBomber import NakajimaB5NType97
from CnCPT.Simulation.UnitBehavior import BasicBehavior
from CnCPT.Simulation.Utility.SideEnum import SideEnum


class Carrier(Ship):
    def __init__(self, name=None, behavior=None, location=None, spawn_polygon=None):
        super().__init__(name=name, behavior=behavior, location=location, spawn_polygon=spawn_polygon,
                         side=SideEnum.RED)
        self.cost = 200
        self.aircraft = {}

    @staticmethod
    def behavior_aggressive(unit, simulation_manager):
        pass

    @staticmethod
    def behavior_passive(unit, simulation_manager):
        pass

    @staticmethod
    def behavior_baseline(unit, simulation_manager):
        unit.kinematics.set_speed(10)
        BasicBehavior.RouteFollowing(unit, simulation_manager)


#  Shōkaku 58 total - 21 Aichi D3A Type 99 "kanbaku" dive bombers, 19 Nakajima B5N Type 97 "kankō" torpedo bombers,
#  18 A6M2 Zero fighters; Zuikaku 63 total - 21 kankō, 22 kanbaku, 20 Zeros; Shōhō 18 total - 6 kankō, 4 Mitsubishi
#  A5M Type 96 fighters, 8 Zeros (Lundstrom 2005b, p. 188; Millot 1974, p. 154). Cressman 2000, p. 93, states Shōhō
#  carried 13 fighters without specifying how many of which type. (Lundstrom 2005b, p. 188; Millot 1974, p. 154).

class Shokaku(Carrier):
    def __init__(self, name="Shokaku", behavior=Carrier.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)
        self.aircraft = {AichiD3AType99: 21,
                         NakajimaB5NType97: 19,
                         A6M2Zero: 18}


class Zuikaku(Carrier):
    def __init__(self, name="Zuikaku", behavior=Carrier.behavior_baseline, location=None, spawn_polygon=None):
        super().__init__(name, behavior, location, spawn_polygon)
        self.aircraft = {AichiD3AType99: 22,
                         NakajimaB5NType97: 21,
                         A6M2Zero: 20}
