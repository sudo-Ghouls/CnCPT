# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CnCPT Thesis
# Fall 2020 - EM.THE

import datetime
import os

import numpy as np
import pp

import FitnessAssessment.FitnessCutoffEvaluation as FitnessCutoffEvaluation
import FitnessAssessment.FitnessUtilityCalculation as FitnessUtilityCalculation
import FitnessAssessment.FitnessVarianceEvaluation as FitnessVarianceEvaluation
from ArchitectureGeneration.ArchitectureBreeder import ArchitectureBreeder
from ArchitectureGeneration.ArchitectureCodeGeneration import generateBaseArchCode, generateAllArchCodes
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


def ContainedRunController(output_path, all_units, controls, seeds, name):
    new_run_controller = RunController(output_path)
    run_score = new_run_controller.run_set(all_units, controls, seeds=seeds, name=name)
    return run_score


class Manager:
    def __init__(self, filepath, CompCon, CONOPCon, HeurCon, FixedArchGenerator):
        self.filepath = filepath
        self.CompCon = CompCon
        self.CONOPCon = CONOPCon
        self.HeurCon = HeurCon
        self.seeds = list(range(1))
        self.FixedArchGenerator = FixedArchGenerator

        # Arch Code Related
        self.max_num_per_unit = None
        self.num_loc_polys = None
        self.conop_con_list = None
        self.max_conop_per_unit = None
        self.base_arch_code = generateBaseArchCode(self)

        # Model Related
        self.model_features = None
        self.labels_log = None
        self.labels_reg = None
        self.peak_performing_predictions = None
        self.models = PredictionModelManager()

        # Parallel Python
        self.server = pp.Server(ppservers=())

        # Fitness Cutoffs
        self.utility_threshold = None
        self.variance_threshold = None
        self.cutoff_metric = None
        self.max_generations = None

    def runCnCPT(self, controls, run_size=10, output_path=''):
        datestring = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
        output_path = os.path.join(output_path, datestring)
        satisfied, generation = False, 1

        # Update Fitness Cutoffs based on controls
        self.utility_threshold = controls.pop("utility_threshold", None)
        self.variance_threshold = controls.pop("variance_threshold", None)
        self.cutoff_metric = controls.pop("cutoff_metric", None)
        self.max_generations = controls.pop("max_generations", None)
        if {self.utility_threshold, self.variance_threshold, self.cutoff_metric, self.max_generations} is None:
            raise Exception("No Cutoff criteria defined; please inlcude utility_threshold, variance_threshold or "
                            "cutoff_generations in controls")

        # generate all possible architecture codes
        arch_codes = generateAllArchCodes(self)
        my_breeder = ArchitectureBreeder(run_size, arch_codes)
        while not satisfied:
            # Birth or Breed
            if bool(my_breeder.Architectures):
                population_sample = my_breeder.breedArchitectures(self, SideEnum.BLUE)
            else:
                population_sample = my_breeder.birthArchitectures(self, SideEnum.BLUE)

            sample_results = self.runPopulationSample(generation, population_sample, controls, output_path, my_breeder)
            self.updateResults(population_sample, sample_results, my_breeder)

            # Update Model Variables
            # train classification model; asses out of sample performance
            # for model in self.models["Classification"]:
            #     predictor = self.models["Classification"][model]["model"]
            #     self.models["Classification"][model]["scores"] = cross_val_score(predictor, self.model_features,
            #                                                                      self.labels_log, cv=5,
            #                                                                      scoring='accuracy')
            #
            # for model in self.models["Regression"]:
            #     predictor = self.models["Regression"][model]["model"]
            #     self.models["Regression"][model]["scores"] = cross_val_score(predictor, self.model_features,
            #                                                                  self.labels_reg, cv=5,
            #                                                                  scoring='neg_root_mean_squared_error')

            # Asses Cutoff parameters
            utility = FitnessUtilityCalculation.process(self.model_features, self.labels_log, self.labels_reg)
            variance = FitnessVarianceEvaluation.process(self.model_features, self.labels_log, self.labels_reg)
            cutoff = FitnessCutoffEvaluation.process(self.model_features, self.labels_log, self.labels_reg)
            satisfied = self.determine_satisfaction(utility, variance, cutoff, generation)

            generation += 1

    def runPopulationSample(self, generation, population_sample, controls, output_path, my_breeder):
        # run Simulation on Architectures
        jobs = []
        results = []
        print("-----------------------------------\n"
              "**** Running Generation {0} ****\n"
              "-----------------------------------".format(generation))
        for job_idx, VariableArch in enumerate(population_sample):
            FixedArchUnits = self.FixedArchGenerator()
            controls['architecture_name'] = VariableArch.name
            all_units = {'Variable': VariableArch.units,
                         'Fixed': FixedArchUnits}
            jobs.append(self.server.submit(ContainedRunController,
                                           (output_path, all_units, controls, self.seeds, VariableArch.name),
                                           (),
                                           ('CnCPT.Simulation.RunController',)))
            print("Starting Simulation Job {0}: {1}".format(job_idx, VariableArch.name))
            # RunController(output_path).run_set(all_units, controls, seeds=self.seeds, name=VariableArch.name)
        print("\n**** Simulations for Generation {0} Underway; Results: ****".format(generation))

        # Return Average Score from set
        for job_idx, job in enumerate(jobs):
            set_results = job()
            result = np.average(set_results)
            results.append(result)
            print("- Job {0} Finished".format(job_idx))

        return results

    def updateResults(self, population_sample, results, my_breeder):
        my_breeder.updateLastGeneration(population_sample, results)
        # Update breeder and model results
        for arch_idx, arch in enumerate(population_sample):
            arch_result = results[arch_idx]
            CodeString = str(arch.code).replace(' ', '').replace('\n', '').replace('None', '-')
            my_breeder.Architectures[CodeString] = arch_result

            if self.model_features is None:
                self.model_features = np.array(arch.code)
                self.labels_log = np.array([arch_result])
                self.labels_reg = np.array([PredictionModelManager.determineResultCategory(arch_result)])
            else:
                self.model_features = np.vstack((self.model_features, arch.code))
                self.labels_log = np.vstack((self.labels_log, arch_result))
                self.labels_reg = np.vstack(
                    (self.labels_reg, PredictionModelManager.determineResultCategory(arch_result)))

    def determine_satisfaction(self, utility, variance, cutoff, generation):
        if utility > self.utility_threshold:
            return True
        if variance < self.variance_threshold:
            return True
        if cutoff > self.cutoff_metric:
            return True
        if generation > self.max_generations:
            return True
        return False
