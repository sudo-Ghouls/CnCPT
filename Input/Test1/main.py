import os

from CnCPT.ArchitectureGenerator.Architecture import Architecture
from CnCPT.ArchitectureGenerator.Constraints.CONOPCon import CONOPCon
from CnCPT.ArchitectureGenerator.Constraints.CompositionCon import CompositionCon
from CnCPT.Core.Manager import Manager
from CnCPT.Input.Test1.behaviors.behavior_alpha import BehaviorA
from CnCPT.Input.Test1.behaviors.behavior_charlie import BehaviorC
from CnCPT.Input.Test1.behaviors.behavior_delta import BehaviorD
from CnCPT.Input.Test1.red_units import red_units
from CnCPT.Input.Test1.units.cg import CG
from CnCPT.Input.Test1.units.ddg import DDG
from CnCPT.Simulation.Utility.SideEnum import SideEnum

if __name__ == "__main__":
    # Set up Test Constraints
    unitList = [DDG, CG]
    lowerBound = [2,  # DDG
                  2]  # CG
    upperBound = [15,  # DDG
                  3]  # CG
    Polygons = [[((43.22, -68.92), (43.22, -62.4), (39.14, -62.4), (39.14, -68.92), (43.22, -68.92))],  # DDG
                [((43.22, -68.92), (43.22, -62.4), (39.14, -62.4), (39.14, -68.92), (43.22, -68.92))]]  # CG
    MyCompsCon = CompositionCon(unitList, lowerBound, upperBound, Polygons)

    CONOPList = [[BehaviorD, BehaviorA],  # DDG
                 [BehaviorA, BehaviorC]]  # CG

    # CONOPList = [[BehaviorD, BehaviorA, BehaviorC],  # DDG
    #              [BehaviorA]]  # CG

    MyCONOPsCOn = CONOPCon(unitList, CONOPList)
    MyHeurCon = None

    # Initialize Manager
    filepath = os.getcwd()
    RedArch = Architecture(red_units, "RedSide", SideEnum.RED)
    MyManager = Manager(filepath, MyCompsCon, MyCONOPsCOn, MyHeurCon, RedArch)
    controls = {"start_time": 0.0,
                "end_time": 24 * 3600.0}
    MyManager.runCnCPT(controls, run_size=1,
                       output_path=r"C:\Users\Thomas Goolsby\iCloudDrive\Documents\MIT\System Design & Management\Thesis_Working_Area\CnCPT\Output\Test1")
