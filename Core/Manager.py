# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CnCPT Thesis
# Fall 2020 - EM.THE

import datetime
import os
import random as r
from enum import Enum

import numpy as np
import pandas as pd
import pp
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import Lasso
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Ridge
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from CnCPT.ArchitectureGenerator.ArchitectureBreeder import ArchitectureBreeder
from CnCPT.Simulation.RunController import RunController
from CnCPT.Simulation.Utility.SideEnum import SideEnum


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
        self.base_arch_code = self.generateBaseArchCode()

        # Model Related
        self.model_features = None
        self.labels_log = None
        self.labels_reg = None
        self.peak_performing_predictions = None
        self.models = self.initialize_models()

        # Parallel Python
        self.server = pp.Server(ppservers=())

    def runCnCPT(self, controls, run_size=10, output_path=''):
        datestring = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
        output_path = os.path.join(output_path, datestring)
        converged, generation = False, 1

        # generate all possible architecture codes
        arch_codes = self.generateAllArchCodes()
        my_breeder = ArchitectureBreeder(run_size, arch_codes)
        while not converged:
            # Birth or Breed
            if bool(my_breeder.Architectures):
                population_sample = my_breeder.breedArchitectures(self, SideEnum.BLUE)
            else:
                population_sample = my_breeder.birthArchitectures(self, SideEnum.BLUE)

            sample_results = self.runPopulationSample(generation, population_sample, controls, output_path, my_breeder)
            self.updateResults(population_sample, sample_results, my_breeder)
            if generation >= 5:
                converged = True

            # asses fitness
            # FitnessCutoffEvaluation
            # FitnessUtilityCalculation
            # FitnessVarianceEvaluation

            # Update Model Variables
            # train classification model; asses out of sample perforamcne
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
                self.labels_reg = np.array([self.determineResultCategory(arch_result)])
            else:
                self.model_features = np.vstack((self.model_features, arch.code))
                self.labels_log = np.vstack((self.labels_log, arch_result))
                self.labels_reg = np.vstack((self.labels_reg, self.determineResultCategory(arch_result)))

    @staticmethod
    def determineResultCategory(result):
        if result > 75:
            return PerformanceCategory.GREAT
        if result > 50:
            return PerformanceCategory.ACCEPTABLE
        if result > 25:
            return PerformanceCategory.POOR
        if result > 0:
            return PerformanceCategory.TERRIBLE

    def generateBaseArchCode(self):
        comp_con_list = self.CompCon.units.keys()
        self.max_num_per_unit = [self.CompCon.units[unit].maxNumber for unit in comp_con_list]
        self.num_loc_polys = [int(len(self.CompCon.units[unit].Polygons)) for unit in comp_con_list]
        self.conop_con_list = self.CONOPCon.units.keys()
        self.max_conop_per_unit = [self.CONOPCon.units[unit].maxNumConop for unit in self.conop_con_list]
        base_arch_code = []
        for idx, Unit in enumerate(comp_con_list):
            base_arch_code.extend([self.max_conop_per_unit[idx], self.num_loc_polys[idx]] * (
                self.max_num_per_unit[idx]))  # two b/c one 0 for behavior one 0 for loc
        return base_arch_code

    def generateAllArchCodes(self):
        comp_con_list = self.CompCon.units.keys()
        lower_bound_per_unit = [self.CompCon.units[unit].lowerBound for unit in comp_con_list]
        upper_bound_per_unit = [self.CompCon.units[unit].upperBound for unit in comp_con_list]
        ArchCodes = self.GenerateArchCode(self.base_arch_code, lower_bound_per_unit, upper_bound_per_unit,
                                          self.num_loc_polys,
                                          self.max_conop_per_unit)
        return ArchCodes

    def MaximumIdxFromCons(self, NumLocPolys, MaxConopPerUnit):
        all_cons = np.concatenate((NumLocPolys, MaxConopPerUnit))
        return max(all_cons)

    def GenerateArchCode(self, BaseArchCode, LowerBoundPerUnit, UpperBoundPerUnit, NumLocPolys, MaxConopPerUnit):
        possible_arch_codes, arch_codes = [], []

        for Col in range(len(BaseArchCode)):
            if Col % 2 == 0:
                options = [None] + list(range(BaseArchCode[Col]))  # Behavior Choice
            else:
                options = list(range(BaseArchCode[Col]))
            if len(possible_arch_codes) == 0:
                possible_arch_codes = np.vstack(np.array(r.choices(options, k=10000)))
            else:
                possible_arch_codes = np.concatenate(
                    (possible_arch_codes, np.vstack(np.array(r.choices(options, k=10000)))), axis=1)
            # Loop ever every second column setting value equal to None if related Behavior is None
            if Col % 2 == 1:
                for Row in range(np.size(possible_arch_codes, 0)):
                    if possible_arch_codes[Row, Col - 1] is None:
                        possible_arch_codes[Row, Col] = None

        for ArchCode in possible_arch_codes:
            if self.ValidArch(ArchCode, LowerBoundPerUnit, UpperBoundPerUnit, NumLocPolys, MaxConopPerUnit):
                if len(arch_codes) == 0:
                    arch_codes = ArchCode
                else:
                    arch_codes = np.append(arch_codes, ArchCode, axis=0)
        arch_codes = np.reshape(arch_codes, (int(int(len(arch_codes)) / len(BaseArchCode)), len(BaseArchCode)))
        arch_codes = pd.DataFrame(arch_codes).drop_duplicates().values
        return arch_codes

    def ValidArch(self, ArchCode, LowerBoundPerUnit, UpperBoundPerUnit, NumLocPolys, MaxConopPerUnit):
        # ArchCode = np.array([1,2,3,4,5,6,7,8,9,10])
        if next(iter(set(ArchCode))) is None:
            return False
        start_idx = 0
        for Unit_i in range(len(LowerBoundPerUnit)):
            max_num_of_unit_i = UpperBoundPerUnit[Unit_i]
            end_idx = start_idx + max_num_of_unit_i * 2
            # Check if Behavior Columns are Valid
            unit_i_behaviors = ArchCode[start_idx:end_idx:2]
            if next(iter(set(unit_i_behaviors))) is None:
                if LowerBoundPerUnit[Unit_i] > 0:
                    return False
            else:
                if len([i for i in unit_i_behaviors if i is not None]) < LowerBoundPerUnit[Unit_i]:
                    return False
                if max([i for i in unit_i_behaviors if i is not None]) > MaxConopPerUnit[Unit_i] - 1:
                    return False
            # Check if Location Columns are Valid
            unit_i_locations = ArchCode[start_idx + 1:end_idx:2]
            if next(iter(set(unit_i_locations))) is None:
                if LowerBoundPerUnit[Unit_i] > 0:
                    return False
            else:
                if len([i for i in unit_i_locations if i is not None]) < LowerBoundPerUnit[Unit_i]:
                    return False
                if max([i for i in unit_i_locations if i is not None]) > NumLocPolys[Unit_i] - 1:
                    return False

            unit_i_info = np.vstack((unit_i_behaviors, unit_i_locations))
            for i in range(np.size(unit_i_info, 1)):
                if len(set(unit_i_info[:, i])) > 1:
                    if None in set(unit_i_info[:, i]):
                        return False
            start_idx = end_idx
        return True

    @staticmethod
    def initialize_models():
        models = {"Classification": {},
                  "Regression": {}}
        # Initialize All Classification Models
        models['Classification']["LogisticRegression"] = {"model": LogisticRegression()}
        models['Classification']["LinearDiscriminantAnalysis"] = {"model": LinearDiscriminantAnalysis()}
        models['Classification']["KNeighborsClassifier"] = {"model": KNeighborsClassifier()}
        models['Classification']["GaussianNB"] = {"model": GaussianNB()}
        models['Classification']["DecisionTreeClassifier"] = {"model": DecisionTreeClassifier()}
        models['Classification']["SVC"] = {"model": SVC()}

        # Initialize All Regression Models
        models['Regression']["LinearRegression"] = {"model": LinearRegression()}
        models['Regression']["Ridge"] = {"model": Ridge()}
        models['Regression']["Lasso"] = {"model": Lasso()}
        models['Regression']["ElasticNet"] = {"model": ElasticNet()}
        models['Regression']["MLPRegressor"] = {"model": MLPRegressor()}
        return models


class PerformanceCategory(Enum):
    GREAT = 1
    ACCEPTABLE = 2
    POOR = 3
    TERRIBLE = 4
