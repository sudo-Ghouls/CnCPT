# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


import os

from ArchitectureGeneration.Constraints.CONOPCon import CONOPCon
from ArchitectureGeneration.Constraints.CompositionCon import CompositionCon
from Core.Manager import Manager
from Input.CoralSea.JapaneseForce.BaselineJapaneseForceLaydown import BaselineJapaneseForce
from Input.CoralSea.UnitedStatesForce.Logic import CarrierLogic
from Input.CoralSea.UnitedStatesForce.Logic import GeneralShipLogic
from Input.CoralSea.UnitedStatesForce.Ships.Carrier import Carrier
from Input.CoralSea.UnitedStatesForce.Ships.Cruiser import Cruiser
from Input.CoralSea.UnitedStatesForce.Ships.Destroyer import Destroyer
from Input.CoralSea.UnitedStatesForce.Ships.Oiler import Oiler
from Simulation.Utility.Area import Area
from Simulation.Utility.SideEnum import SideEnum

Blue_Polygon = Area(name="Blue_Polygon",
                    bounds=((-12.81, 160.05), (-12.84, 164.04), (-15.15, 163.98), (-15.11, 160.02), (-12.81, 160.05)))


def run(specific_architecture=None):
    # Set up Test Constraints
    unitList = [Carrier, Cruiser, Destroyer, Oiler]
    LeadershipPriority = [Carrier, Cruiser, Destroyer, Oiler]  # used for auto grouping in architecture generation

    lowerBound = [2,  # CVN
                  5,  # CG
                  10,  # DDG
                  2]  # Oilier
    upperBound = [4,  # CVN
                  10,  # CG
                  15,  # DDG
                  4]  # Oilier

    Polygons = [[Blue_Polygon],  # CVN
                [Blue_Polygon],  # CG
                [Blue_Polygon],  # DDG
                [Blue_Polygon]]  # Oiler

    MyCompsCon = CompositionCon(unitList, lowerBound, upperBound, Polygons)

    CONOPList = [[CarrierLogic.behavior_baseline,
                  CarrierLogic.behavior_aggressive,
                  CarrierLogic.behavior_passive],
                 # CVN
                 [GeneralShipLogic.behavior_baseline,
                  GeneralShipLogic.behavior_aggressive,
                  GeneralShipLogic.behavior_passive],
                 # CG
                 [GeneralShipLogic.behavior_baseline,
                  GeneralShipLogic.behavior_aggressive,
                  GeneralShipLogic.behavior_passive],
                 # DDG
                 [GeneralShipLogic.behavior_baseline]]  # Oilier

    MyCONOPsCOn = CONOPCon(unitList, CONOPList)
    MyHeurCon = None

    # Initialize Manager
    filepath = os.getcwd()
    MyManager = Manager(filepath, MyCompsCon, MyCONOPsCOn, MyHeurCon, BaselineJapaneseForce, LeadershipPriority,
                        MC_size=1)
    controls = {"start_time": 0.0,
                "end_time": 3 * 24 * 3600.0,
                "utility_threshold": .9,
                "variance_threshold": .001,
                "cutoff_metric": 10000,
                "max_generations": 10,
                "full_data_logging": False}

    constants = {"simulation_map_bounds": ((-18.02904145799271, 149.9831854228132),
                                           (-18.0006410087399, 164.9716046029078),
                                           (-5.030607064197672, 164.9521271362831),
                                           (-5.001921913555804, 150.0046640118783),
                                           (-18.02904145799271, 149.9831854228132))}
    if specific_architecture is not None:
        controls["full_data_logging"] = True
        ArchCode = specific_architecture[0]
        ArchName = specific_architecture[1]
        ArchSide = SideEnum.BLUE
        MyManager.runSpecificCode(controls, constants, ArchName, ArchCode, ArchSide, seeds=range(50),
                                  output_path=r"D:\Thesis\CnCPT_Tests\CoralSeaEndersGamePeakArch")

    else:
        MyManager.runCnCPT(controls, constants, run_size=30,
                           output_path=r"D:\Thesis\CnCPT_Tests\CoralSeaEndersGame")


if __name__ == "__main__":
    run()
