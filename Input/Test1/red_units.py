from CnCPT.Input.Test1.behaviors.behavior_delta import BehaviorD
from CnCPT.Input.Test1.units.cg import CG
from CnCPT.Input.Test1.units.ddg import DDG
from CnCPT.Simulation.Utility.SideEnum import SideEnum

spawn_polygon = ((43.22, -68.92), (43.22, -62.4), (39.14, -62.4), (39.14, -68.92), (43.22, -68.92))

all_units = []
for CGi in range(10):
    name = "Red_CG_" + str(CGi)
    new_CG = CG(name=name, behavior=BehaviorD, spawn_polygon=spawn_polygon, side=SideEnum.RED)
    all_units.append(new_CG)

for DDGi in range(5):
    name = "Red_DDG_" + str(DDGi)
    new_DDG = DDG(name=name, behavior=BehaviorD, spawn_polygon=spawn_polygon, side=SideEnum.RED)
    all_units.append(new_DDG)

red_units = all_units
