# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CnCPT Thesis
# Fall 2020 - EM.THE

import datetime
import json
import os
import pickle

import numpy as np
import pp

from ArchitectureGeneration.Architecture import Architecture
from ArchitectureGeneration.ArchitectureBreeder import ArchitectureBreeder
from ArchitectureGeneration.ArchitectureCodeGeneration import generateBaseArchCode, generateAllArchCodes
from FitnessAssessment import FitnessCutoffEvaluation
from FitnessAssessment import FitnessUtilityCalculation
from FitnessAssessment import FitnessVarianceEvaluation
from FitnessPrediction.PredictionModelManager import PredictionModelManager
from Simulation.RunController import RunController
from Simulation.Utility.SideEnum import SideEnum


class FakeServer(object):
    def __init__(self, ncpus="autodetect", ppservers=()):
        pass

    def submit(self, fn, params, localfunctions=None, externalmodules=None):
        result = fn(*params)
        return lambda: result


pp.Server = FakeServer


def ContainedRunController(output_path, CONOPCon, CompCon, LeadershipPriority, FixedArchGenerator,
                           VariableArch, controls, constants, seeds, name):
    new_run_controller = RunController(output_path)
    performance_data, set_output_path = new_run_controller.run_set_CnCPT(CONOPCon, CompCon, LeadershipPriority,
                                                                         FixedArchGenerator,
                                                                         VariableArch, controls, seeds=seeds, name=name,
                                                                         constants=constants)
    with open(os.path.join(set_output_path, "Simulation_Set_Log.pkl"), 'wb') as f:
        pickle.dump(performance_data, f)
    return performance_data


class Manager:
    def __init__(self, filepath, CompCon, CONOPCon, HeurCon, FixedArchGenerator, LeadershipPriority=None, MC_size=1):
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
        self.CnCPT_family_tree = []

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
        self.generation = 1
        self.generations_prior_to_breeding = 3

    def runCnCPT(self, controls, constants, run_size=10, output_path='', breed_method="crossover",
                 breeding_metric="score_mean"):
        try:
            os.mkdir(output_path)
        except FileExistsError:
            pass
        datestring = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
        output_path = os.path.join(output_path, datestring)
        self.output_path = output_path
        satisfied = False

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
        self.dump_config(run_size, breed_method)
        while not satisfied:
            # Birth or Breed
            if bool(my_breeder.Architectures):
                population_sample = my_breeder.breedArchitectures(self, SideEnum.BLUE, breed_method=breed_method)
            else:
                population_sample = my_breeder.birthArchitectures(self, SideEnum.BLUE)

            sample_results = self.runPopulationSample(self.generation, population_sample, controls, constants,
                                                      output_path,
                                                      my_breeder)

            self.updateResults(population_sample, sample_results, my_breeder, self.generation, metric=breeding_metric)

            # Asses Cutoff parameters
            utility = FitnessUtilityCalculation.process(self.model_features, self.labels_class, self.labels_reg)
            variance = FitnessVarianceEvaluation.process(self.model_features, self.labels_class, self.labels_reg)
            cutoff = FitnessCutoffEvaluation.process(self.model_features, self.labels_class, self.labels_reg)
            satisfied = self.determine_satisfaction(utility, variance, cutoff, self.generation)

            self.generation += 1
        with open(os.path.join(self.output_path, "CnCPT_Family_Tree.pkl"), 'wb') as f:
            pickle.dump(self.CnCPT_family_tree, f)

    def runSpecificCode(self, controls, constants, ArchName, ArchCode, ArchSide, seeds, output_path,
                        contains_neg_1=True):
        if contains_neg_1:
            ArchCode = ArchCode.replace('-1', '-')
        VariableArchRef = Architecture.create_arch_from_string(ArchCode, self.CONOPCon, self.CompCon,
                                                               self.LeadershipPriority, ArchSide, ArchName)
        VariableArchRef.generate_arch_figures(output_path)
        new_run_controller = RunController(output_path)
        performance_data, set_output_path = new_run_controller.run_set_CnCPT(self.CONOPCon, self.CompCon,
                                                                             self.LeadershipPriority,
                                                                             self.FixedArchGenerator, VariableArchRef,
                                                                             controls, seeds=seeds,
                                                                             name=VariableArchRef.name,
                                                                             constants=constants)
        with open(os.path.join(set_output_path, "Simulation_Set_Log.pkl"), 'wb') as f:
            pickle.dump(performance_data, f)

    def runPopulationSample(self, generation, population_sample, controls, constants, output_path, my_breeder):
        # run Simulation on Architectures
        jobs, results = [], []
        print("-----------------------------------\n"
              "**** Running Generation {0} ****\n"
              "-----------------------------------".format(generation))
        for job_idx, VariableArch in enumerate(population_sample):
            controls['architecture_name'] = VariableArch.name
            print("Starting Simulation Job {0}: {1}".format(job_idx, VariableArch.name))
            jobs.append(self.server.submit(ContainedRunController,
                                           (output_path, self.CONOPCon, self.CompCon, self.LeadershipPriority,
                                            self.FixedArchGenerator, VariableArch, controls, constants, self.seeds,
                                            VariableArch.name),
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

    def updateResults(self, population_sample, population_results, my_breeder, generation, metric="score_mean"):
        my_breeder.updateLastGeneration(population_sample, population_results, metric)
        self.results[generation] = {}
        # Update breeder and model results
        for arch_idx, arch in enumerate(population_sample):
            arch_result = population_results[arch_idx][metric]
            CodeString = str(arch.ArchCode).replace(' ', '').replace('\n', '').replace('None', '-')
            self.results[generation][CodeString] = population_results[arch_idx]  # save off all results
            my_breeder.Architectures[CodeString] = arch_result
            arch_features = self.add_aggregate_features(arch.ArchCode)
            self.CnCPT_family_tree.append([CodeString, arch.parents, generation, arch_result])

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
        if generation >= self.max_generations:
            return True
        return False

    def add_aggregate_features(self, arch_code):
        """ This method adds additonal featurs to the arch code based on aggregation of units, behaviors, and geometries
        realized.
        """
        full_arch_code = np.array(arch_code)
        full_arch_code = full_arch_code.astype(int)
        return full_arch_code

    def dump_config(self, run_size, breed_method):
        try:
            os.mkdir(self.output_path)
        except FileExistsError:
            pass
        with open(os.path.join(self.output_path, "CnCPT_Parameters.cfg"), 'w') as f:
            data = {"run_size": str(run_size),
                    "breed_method": str(breed_method),
                    "seeds": str(self.seeds),
                    "max_num_per_unit": str(self.max_num_per_unit),
                    "num_loc_polys": str(self.num_loc_polys),
                    "conop_con_list": str(self.conop_con_list),
                    "max_conop_per_unit": str(self.max_conop_per_unit),
                    "base_arch_code": str(self.base_arch_code),
                    "minimum_generations_for_prediction": str(self.minimum_generations_for_prediction),
                    "utility_threshold": str(self.utility_threshold),
                    "variance_threshold": str(self.variance_threshold),
                    "cutoff_metric": str(self.cutoff_metric),
                    "max_generations": str(self.max_generations)}
            json.dump(data, f, indent=4)