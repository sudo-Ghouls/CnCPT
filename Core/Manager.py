# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CnCPT Thesis
# Fall 2020 - EM.THE

import datetime
import os
import pickle
import random

import numpy as np
import pp

from ArchitectureGeneration.ArchitectureBreeder import ArchitectureBreeder
from ArchitectureGeneration.ArchitectureCodeGeneration import generateBaseArchCode, generateAllArchCodes
from FitnessAssessment import FitnessCutoffEvaluation
from FitnessAssessment import FitnessUtilityCalculation
from FitnessAssessment import FitnessVarianceEvaluation
from FitnessPrediction.PredictionModelManager import PredictionModelManager
from Simulation.RunController import RunController
from Simulation.Utility.SideEnum import SideEnum


# class FakeServer(object):
#     def __init__(self, ncpus="autodetect", ppservers=()):
#         pass
#
#     def submit(self, fn, params, localfunctions=None, externalmodules=None):
#         result = fn(*params)
#         return lambda: result
#
#
# pp.Server = FakeServer


def ContainedRunController(output_path, all_units, controls, constants, seeds, name):
    new_run_controller = RunController(output_path)
    run_score = new_run_controller.run_set(all_units, controls, seeds=seeds, name=name, constants=constants)
    # import pickle
    # x = pickle.dumps(all_units)
    # y = pickle.loads(x)
    # new_run_controller.run_set(all_units, controls, seeds=seeds, name=name)
    return run_score


class Manager:
    def __init__(self, filepath, CompCon, CONOPCon, HeurCon, FixedArchGenerator, LeadershipPriority=None, seed=0,
                 MC_size=1):
        self.filepath = filepath
        self.output_path = None  # updated upon execution
        self.CompCon = CompCon
        self.CONOPCon = CONOPCon
        self.HeurCon = HeurCon
        self.LeadershipPriority = LeadershipPriority
        self.seeds = list(range(MC_size))
        self.FixedArchGenerator = FixedArchGenerator

        # Arch Code Related
        self.max_num_per_unit = None
        self.num_loc_polys = None
        self.conop_con_list = None
        self.max_conop_per_unit = None
        self.base_arch_code = generateBaseArchCode(self)

        # Model Related
        self.results = {}
        self.model_features = None
        self.labels_class = None
        self.labels_reg = None
        self.peak_performing_predictions = None
        self.minimum_generations_for_prediction = 3
        self.model_manager = PredictionModelManager()

        # Parallel Python
        self.server = pp.Server(ppservers=())

        # Fitness Cutoffs
        self.utility_threshold = None
        self.variance_threshold = None
        self.cutoff_metric = None
        self.max_generations = None

        # Seed Random Generators
        random.seed(seed)
        np.random.seed(seed)

    def runCnCPT(self, controls, constants, run_size=10, output_path=''):
        datestring = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
        output_path = os.path.join(output_path, datestring)
        self.output_path = output_path
        satisfied, generation = False, 1

        # Update Fitness Cutoffs based on controls
        self.utility_threshold = controls.pop("utility_threshold", None)
        self.variance_threshold = controls.pop("variance_threshold", None)
        self.cutoff_metric = controls.pop("cutoff_metric", None)
        self.max_generations = controls.pop("max_generations", None)
        if {self.utility_threshold, self.variance_threshold, self.cutoff_metric, self.max_generations} is None:
            raise Exception("No Cutoff criteria defined; please include utility_threshold, variance_threshold or "
                            "cutoff_generations in controls")

        # generate all possible architecture codes
        arch_codes = generateAllArchCodes(self)
        my_breeder = ArchitectureBreeder(run_size, arch_codes, self.base_arch_code)
        while not satisfied:
            # Birth or Breed
            if bool(my_breeder.Architectures):
                population_sample = my_breeder.breedArchitectures(self, SideEnum.BLUE)
            else:
                population_sample = my_breeder.birthArchitectures(self, SideEnum.BLUE)

            sample_results = self.runPopulationSample(generation, population_sample, controls, constants, output_path,
                                                      my_breeder)
            self.updateResults(population_sample, sample_results, my_breeder, generation)

            # Update Prediction Models
            # if generation > self.minimum_generations_for_prediction:
            #     self.model_manager.update_models(generation, population_sample, sample_results,
            #                                      self.model_features, self.labels_class, self.labels_reg)

            # Asses Cutoff parameters
            utility = FitnessUtilityCalculation.process(self.model_features, self.labels_class, self.labels_reg)
            variance = FitnessVarianceEvaluation.process(self.model_features, self.labels_class, self.labels_reg)
            cutoff = FitnessCutoffEvaluation.process(self.model_features, self.labels_class, self.labels_reg)
            satisfied = self.determine_satisfaction(utility, variance, cutoff, generation)

            generation += 1

    def runPopulationSample(self, generation, population_sample, controls, constants, output_path, my_breeder):
        # run Simulation on Architectures
        jobs, results = [], []
        print("-----------------------------------\n"
              "**** Running Generation {0} ****\n"
              "-----------------------------------".format(generation))
        for job_idx, VariableArch in enumerate(population_sample):
            FixedArchUnits = self.FixedArchGenerator()
            controls['architecture_name'] = VariableArch.name
            all_units = VariableArch.units + FixedArchUnits
            print("Starting Simulation Job {0}: {1}".format(job_idx, VariableArch.name))
            jobs.append(self.server.submit(ContainedRunController,
                                           (output_path, all_units, controls, constants, self.seeds, VariableArch.name),
                                           (),
                                           ('Simulation.RunController',)))
            # RunController(output_path).run_set(all_units, controls, seeds=self.seeds, name=VariableArch.name)
        print("\n**** Simulations for Generation {0} Underway; Results: ****".format(generation))
        # Return Average Score from set
        for job_idx, job in enumerate(jobs):
            set_results = job()
            results.append(set_results)
            print("- Job {0} Finished".format(job_idx))
        return results

    def updateResults(self, population_sample, population_results, my_breeder, generation):
        my_breeder.updateLastGeneration(population_sample, population_results)
        self.results[generation] = {}
        # Update breeder and model results
        for arch_idx, arch in enumerate(population_sample):
            arch_result = population_results[arch_idx]["score"]
            CodeString = str(arch.code).replace(' ', '').replace('\n', '').replace('None', '-')
            self.results[generation][CodeString] = population_results[arch_idx]  # save off all results
            my_breeder.Architectures[CodeString] = arch_result
            arch_features = self.add_aggregate_features(arch.code)

            if self.model_features is None:
                self.model_features = arch_features
                self.labels_reg = np.array(arch_result)
                self.labels_class = np.array([PredictionModelManager.determineResultCategory(arch_result)])
            else:
                self.model_features = np.vstack((self.model_features, arch_features))
                self.labels_reg = np.vstack((self.labels_reg, arch_result))
                self.labels_class = np.vstack(
                    (self.labels_class, PredictionModelManager.determineResultCategory(arch_result)))
        with open(os.path.join(self.output_path, "Generation_{0}_Results.pkl".format(generation)), 'wb') as f:
            data = {"results": self.results[generation],
                    "model_features": self.model_features,
                    "labels_reg": self.labels_reg,
                    "labels_class": self.labels_class}
            pickle.dump(data, f)

    def determine_satisfaction(self, utility, variance, cutoff, generation):
        if self.utility_threshold is not None and utility > self.utility_threshold:
            return True
        if self.variance_threshold is not None and variance < self.variance_threshold:
            return True
        if self.cutoff_metric is not None and cutoff > self.cutoff_metric:
            return True
        if generation > self.max_generations:
            return True
        return False

    def add_aggregate_features(self, arch_code):
        """ This method adds additonal featurs to the arch code based on aggregation of units, behaviors, and geometries
        realized.
        """
        start_idx, unit_idxs, num_units_realized, realized_unit_idxs = 0, {}, {}, {}
        unit_behaviors, unit_geometries = {}, {}
        comp_con = self.CompCon
        conop_con = self.CONOPCon
        full_arch_code = np.array(arch_code)

        for unit in conop_con.units:
            unit_behaviors[unit] = np.zeros((1, conop_con.units[unit].maxNumConop))[0]

        for unit in comp_con.units:
            unit_info = comp_con.units[unit]
            end_idx = start_idx + (unit_info.maxNumber * 2)
            unit_idxs[unit] = (start_idx, end_idx)
            start_idx = end_idx
            unit_geometries[unit] = np.zeros((1, len(comp_con.units[unit].Polygons)))[0]
        for unit in unit_idxs:
            unit_idx = unit_idxs[unit]
            unit_arch_code_section = full_arch_code[unit_idx[0]:unit_idx[1]]
            num_units_realized[unit] = int(len([i for i in unit_arch_code_section if i >= 0]) / 2)
            realized_unit_idxs[unit] = [i for i in range(unit_idx[0], unit_idx[1]) if full_arch_code[i] >= 0]
        new_code_section_units_realized = np.array([num_units_realized[unit] for unit in num_units_realized])
        for unit in realized_unit_idxs:
            i = 0
            for _ in range(int(len(realized_unit_idxs[unit]) / 2)):
                behavior = full_arch_code[realized_unit_idxs[unit][i]] - 1
                unit_behaviors[unit][behavior] += 1
                geometry = full_arch_code[realized_unit_idxs[unit][i + 1]] - 1
                unit_geometries[unit][geometry] += 1
                i += 2
        new_code_section_behaviors_realized = np.hstack([unit_behaviors[unit] for unit in unit_behaviors])
        new_code_section_geometry_realized = np.hstack([unit_geometries[unit] for unit in unit_geometries])
        new_code_features = np.hstack(
            (new_code_section_units_realized, new_code_section_behaviors_realized, new_code_section_geometry_realized))
        full_arch_code = np.hstack((full_arch_code, new_code_features))
        full_arch_code = full_arch_code.astype(int)
        return full_arch_code
