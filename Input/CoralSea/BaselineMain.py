# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CnCPT Thesis
# Fall 2020 - EM.THE

from CnCPT.Input.CoralSea.JapaneseForce.BaselineJapaneseForceLaydown import BaselineJapaneseForce
from CnCPT.Input.CoralSea.UnitedStatesForce.BaselineUSForceLaydown import BaselineUSForce
from CnCPT.Simulation.RunController import RunController

if __name__ == "__main__":
    controls = {"architecture_name": "Baseline",
                "start_time": 0.0,
                "end_time": 3 * 24 * 3600.0}
    output_path = r"C:\Users\Thomas Goolsby\iCloudDrive\Documents\MIT\System Design & Management\Thesis_Working_Area\CnCPT\Output\CoralSea"
    # output_path = r"~\Documents\MIT\System Design & Management\Thesis_Working_Area\CnCPT\Output\CoralSea"
    all_units = {'Blue': BaselineUSForce(),
                 'Red': BaselineJapaneseForce()}
    constants = {"simulation_map_bounds": ((-18.02904145799271, 149.9831854228132),
                                           (-18.0006410087399, 164.9716046029078),
                                           (-5.030607064197672, 164.9521271362831),
                                           (-5.001921913555804, 150.0046640118783),
                                           (-18.02904145799271, 149.9831854228132))}
    RunController(output_path).run_set(all_units, controls, constants=constants, seeds=[0], name="Baseline")
