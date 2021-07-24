# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CnCPT Thesis
# Fall 2020 - EM.THE

import os
import pickle

from Input.CoralSea.JapaneseForce.BaselineJapaneseForceLaydown import BaselineJapaneseForce
from Input.CoralSea.UnitedStatesForce.BaselineUSForceLaydown import BaselineUSForce
from Simulation.RunController import RunController

if __name__ == "__main__":
    controls = {"architecture_name": "Baseline",
                "start_time": 0.0,
                "end_time": 3 * 24 * 3600.0,
                "full_data_logging": True}
    output_path = r"D:\Thesis\CoralSeaBaseline"
    # output_path = r"~\Documents\MIT\System Design & Management\Thesis_Working_Area\CnCPT\Output\CoralSea"

    constants = {"simulation_map_bounds": ((-18.02904145799271, 149.9831854228132),
                                           (-18.0006410087399, 164.9716046029078),
                                           (-5.030607064197672, 164.9521271362831),
                                           (-5.001921913555804, 150.0046640118783),
                                           (-18.02904145799271, 149.9831854228132))}
    baseline_performance_data, set_output_path = RunController(output_path).run_set(BaselineJapaneseForce,
                                                                                    BaselineUSForce, controls,
                                                                                    constants=constants,
                                                                                    seeds=range(10),
                                                                                    name="Baseline")
    with open(os.path.join(set_output_path, "Simulation_Set_Log.pkl"), 'wb') as f:
        pickle.dump(baseline_performance_data, f)
