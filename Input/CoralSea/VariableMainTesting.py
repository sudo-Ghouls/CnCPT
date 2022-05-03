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

Blue_Polygon_1 = Area(name="Blue_Polygon_1",
                      bounds=((-12.38, 150.60), (-12.39, 153.97), (-15.30, 153.96), (-15.27, 150.61), (-12.38, 150.60)))
Blue_Polygon_2 = Area(name="Blue_Polygon_2",
                      bounds=((-15.79, 155.61), (-15.69, 159.37), (-17.78, 159.69), (-17.73, 155.78), (-15.79, 155.61)))
Blue_Polygon_3 = Area(name="Blue_Polygon_3",
                      bounds=((-12.81, 160.05), (-12.84, 164.04), (-15.15, 163.98), (-15.11, 160.02), (-12.81, 160.05)))
Blue_Polygon_4 = Area(name="Blue_Polygon_4",
                      bounds=((-10.59, 155.10), (-10.77, 158.66), (-13.07, 158.81), (-13.04, 155.23), (-10.59, 155.10)))

if __name__ == "__main__":
    # Set up Test Constraints
    unitList = [Carrier, Cruiser, Destroyer, Oiler]
    LeadershipPriority = [Carrier, Cruiser, Destroyer, Oiler]  # used for auto grouping in architecture generation

    lowerBound = [2,  # CVN
                  8,  # CG
                  13,  # DDG
                  2]  # Oilier
    upperBound = [6,  # CVN
                  8,  # CG
                  13,  # DDG
                  2]  # Oilier

    Polygons = [[Blue_Polygon_1, Blue_Polygon_2, Blue_Polygon_3, Blue_Polygon_4],  # CVN
                [Blue_Polygon_1, Blue_Polygon_2, Blue_Polygon_3, Blue_Polygon_4],  # CG
                [Blue_Polygon_1, Blue_Polygon_2, Blue_Polygon_3, Blue_Polygon_4],  # DDG
                [Blue_Polygon_1, Blue_Polygon_2, Blue_Polygon_3, Blue_Polygon_4]]  # Oiler

    MyCompsCon = CompositionCon(unitList, lowerBound, upperBound, Polygons)

    CONOPList = [[CarrierLogic.behavior_baseline],
                 # CVN
                 [GeneralShipLogic.behavior_baseline],
                 # CG
                 [GeneralShipLogic.behavior_baseline],
                 # DDG
                 [GeneralShipLogic.behavior_baseline]]  # Oilier

    MyCONOPsCOn = CONOPCon(unitList, CONOPList)
    MyHeurCon = None

    # Initialize Manager
    filepath = os.getcwd()
    MyManager = Manager(filepath, MyCompsCon, MyCONOPsCOn, MyHeurCon, BaselineJapaneseForce, LeadershipPriority,
                        MC_size=1)
    controls = {"start_time": 0.0,
                "end_time": .1 * 24 * 3600.0,
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

    MyManager.runCnCPT(controls, constants, run_size=30,
                       output_path=r"D:\Thesis\CnCPT_Tests\BreedingTest")
