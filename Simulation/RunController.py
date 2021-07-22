# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

import cProfile
import datetime
import io
import os
import pstats
import random
from pstats import SortKey

import numpy as np

from ArchitectureGeneration.Architecture import Architecture
from Simulation.Communication.Network import auto_network_architectures
from Simulation.DataManagement.PostProcessing import post_process
from Simulation.SimulationManager import SimulationManager
from Simulation.Utility.Constants import intialize_constants


class RunController:
    """ 

    """

    def __init__(self, output_path=None, profile=False):
        """

        :param output_path:
        :return:
        """
        if output_path is None:
            path = os.path.join(os.path.dirname(__file__), "..", 'Output')
            self.output_path = os.path.abspath(path)
        else:
            self.output_path = os.path.abspath(output_path)
        self.timestamp_format = "%Y-%m-%d-%H%M%S"
        self.seedstamp_format = "%d"
        self.SimulationManager = SimulationManager
        self.profile = profile

        try:
            os.mkdir(self.output_path)
        except FileExistsError:
            pass

    def run_set(self, CONOPCon, CompCon, LeadershipPriority, FixedArchGenerator, VariableArchInstance, controls,
                seeds=[0], name=None,
                constants=None):
        """

        :param all_units:
        :param controls:
        :param seeds:
        :param name:
        :param constants:
        :return:
        """
        set_data = {}

        if constants is None:
            constants = intialize_constants()

        # Generate Top level directory
        if name is not None:
            output_path = os.path.join(self.output_path, name)
            try:
                os.mkdir(output_path)
            except FileExistsError:
                pass
        else:
            output_path = self.output_path

        # Generate Timestamp level directory
        datestring = datetime.datetime.now().strftime(self.timestamp_format)
        output_path = os.path.join(output_path, datestring)
        try:
            os.mkdir(output_path)
        except FileExistsError:
            pass

        # Run Seeds
        for seed in seeds:
            FixedArchUnits = FixedArchGenerator()
            VariableArch = Architecture.create_from_code(VariableArchInstance.code, CONOPCon, CompCon,
                                                         LeadershipPriority, VariableArchInstance.side,
                                                         VariableArchInstance.name)
            all_units = VariableArch.units + FixedArchUnits
            seed_data = self.run_seed(all_units, controls, constants, seed, output_path)
            set_data[seed] = seed_data
        data = {"score_mean": np.mean([set_data[seed]["score"] for seed in set_data]),
                "score_var": np.var([set_data[seed]["score"] for seed in set_data]),
                "vsm_ships_mean": np.mean([set_data[seed]["vsm_ships"] for seed in set_data]),
                "vsm_ships_var": np.var([set_data[seed]["vsm_ships"] for seed in set_data]),
                "vsm_aircraft_mean": np.mean([set_data[seed]["vsm_aircraft"] for seed in set_data]),
                "vsm_aircraft_var": np.var([set_data[seed]["vsm_aircraft"] for seed in set_data]),
                "vscm_ships_mean": np.mean([set_data[seed]["vscm_ships"] for seed in set_data]),
                "vscm_ships_var": np.var([set_data[seed]["vscm_ships"] for seed in set_data]),
                "vscm_aircraft_mean": np.mean([set_data[seed]["vscm_aircraft"] for seed in set_data]),
                "vscm_aircraft_var": np.var([set_data[seed]["vscm_aircraft"] for seed in set_data]),
                "vscm_blue_mean": np.mean([set_data[seed]["vscm_blue"] for seed in set_data]),
                "vscm_blue_var": np.var([set_data[seed]["vscm_blue"] for seed in set_data]),
                "fam_ships_mean": np.mean([set_data[seed]["fam_ships"] for seed in set_data]),
                "fam_ships_var": np.var([set_data[seed]["fam_ships"] for seed in set_data]),
                "fam_aircraft_mean": np.mean([set_data[seed]["fam_aircraft"] for seed in set_data]),
                "fam_aircraft_var": np.var([set_data[seed]["fam_aircraft"] for seed in set_data]),
                "facm_ships_mean": np.mean([set_data[seed]["facm_ships"] for seed in set_data]),
                "facm_ships_var": np.var([set_data[seed]["facm_ships"] for seed in set_data]),
                "facm_aircraft_mean": np.mean([set_data[seed]["facm_aircraft"] for seed in set_data]),
                "facm_aircraft_var": np.var([set_data[seed]["facm_aircraft"] for seed in set_data]),
                "facm_red_mean": np.mean([set_data[seed]["facm_red"] for seed in set_data]),
                "facm_red_var": np.var([set_data[seed]["facm_red"] for seed in set_data]),
                "individual_seed_data_mean": set_data}
        data["score_mean_variance"] = data["score_mean"] - ((2 * ((data["score_var"]) ** 2)) / 2.0)
        return data

    def run_seed(self, all_units, controls, constants, seed, output_path):
        """

        :param all_units:
        :param controls:
        :param constants:
        :param seed:
        :param output_path:
        :return:
        """

        seed_string = self.seedstamp_format % seed
        output_path = os.path.join(output_path, seed_string)
        success = False
        while not success:
            try:
                os.mkdir(output_path)
            except FileExistsError:
                print('This Output Path is not Empty: {0}'.format(output_path))
            else:
                success = True

        open(os.path.join(output_path, 'meta_data.txt'), "w").write(output_path)

        networks = auto_network_architectures(all_units)
        SimulationManager = self.SimulationManager(all_units, networks, constants, output_path,
                                                   start_time=controls['start_time'],
                                                   end_time=controls['end_time'],
                                                   full_data_logging=controls["full_data_logging"])

        # Seed
        random.seed(seed)

        for unit in all_units:
            unit.register(SimulationManager, constants)

        self.run(SimulationManager, controls)
        seed_data = post_process(SimulationManager)
        SimulationManager.data_logger.close_data_logger(SimulationManager)
        return seed_data

    def run(self, simulation_manager, controls):
        """

        :param simulation_manager:
        :param controls:
        :return:
        """
        if self.profile:
            pr = cProfile.Profile()
            pr.enable()
            simulation_manager.run(until=controls['end_time'])
            pr.disable()
            s = io.StringIO()
            sortby = SortKey.CUMULATIVE
            ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
            ps.print_stats()
            print(s.getvalue())
        else:
            simulation_manager.run(until=controls['end_time'])
