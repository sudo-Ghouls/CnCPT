# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE
import random

import numpy as np

from ArchitectureGeneration.Architecture import Architecture


class ArchitectureBreeder:
    def __init__(self, N, arch_codes, base_arch_code):
        self.ArchCodes = arch_codes
        self.BaseArchCode = base_arch_code
        self.Architectures = {}
        self.LastGenerationData = {}
        self.LastGenerationArchCodes = None
        self.LastGenerationRawResults = None
        self.NSamples = N
        self.LastArchIdx = 0

    def birthArchitectures(self, manager, side):
        population_sample, i = [], 0
        InitialPopulationDraw = random.sample(range(len(self.ArchCodes)), self.NSamples * 5)

        while len(population_sample) < self.NSamples:
            NewCode = self.ArchCodes[InitialPopulationDraw[i]]
            NewCodeString = str(NewCode).replace(' ', '').replace('\n', '').replace('None', '-')
            ArchitectureName = "Architecture {0}".format(
                str(NewCode).replace(' ', '').replace('\n', '').replace('-1', '-'))
            ArchitectureInstance = Architecture.create_from_code(NewCode, manager, side, ArchitectureName)

            # Apply Heuristics
            if manager.HeurCon is not None:
                for heuristic in manager.HeurCon:
                    HeuBool = manager.HeurCon[heuristic](ArchitectureInstance)
                    if HeuBool is True:
                        self.Architectures[NewCodeString] = None
                        population_sample.append(ArchitectureInstance)
            else:
                self.Architectures[NewCodeString] = None
                population_sample.append(ArchitectureInstance)
            i += 1

        return population_sample

    def breedArchitectures(self, manager, side, breed_ratio=.7, predicted_ratio=.3, parent_size=2):
        population_sample, i, total_breed = [], 0, 0
        numBreed = round(self.NSamples * breed_ratio)
        numPredicted = round(self.NSamples * predicted_ratio)
        PopulationDraw = random.sample(range(len(self.ArchCodes)), len(self.ArchCodes))

        # fill  with breeding from last generation
        num_parents = np.max((2,round(self.NSamples*.1)))
        parents_idxs = np.argpartition(self.LastGenerationRawResults, -num_parents)[-num_parents:]
        parents = [self.LastGenerationArchCodes[p_idx] for p_idx in parents_idxs]
        while len(population_sample) < numBreed:
            ArchitectureInstance, break_out = self.breedGeneration(parents, manager, side)
            if break_out:
                break
            population_sample.append(ArchitectureInstance)
            total_breed += 1

        # Incorporate predicted peak performers
        if manager.peak_performing_predictions is not None:
            while len(population_sample) - total_breed < numPredicted:
                pass

        # fill  with random
        while len(population_sample) < self.NSamples:
            NewCode = self.ArchCodes[PopulationDraw[i]]
            NewCodeString = str(NewCode).replace(' ', '').replace('\n', '').replace('None', '-')
            ArchitectureName = "Architecture {0}".format(
                str(NewCode).replace(' ', '').replace('\n', '').replace('-1', '-'))
            ArchitectureInstance = Architecture.create_from_code(NewCode, manager, side, ArchitectureName)
            if NewCodeString not in self.Architectures.keys():
                self.Architectures[NewCodeString] = None
                population_sample.append(ArchitectureInstance)
            i += 1

        return population_sample

    def breedGeneration(self, parents, manager, side):
        loops = 0
        while loops < 100:
            NewCode = []
            for gene_idx in range(0, int(len(self.BaseArchCode)), 2):
                parent_choice = np.random.randint(len(parents))
                gene_choice = list(parents[parent_choice][gene_idx:gene_idx + 2])
                NewCode += gene_choice
            NewCode = np.array(NewCode)
            NewCodeString = str(NewCode).replace(' ', '').replace('\n', '').replace('None', '-')
            ArchitectureName = "Architecture {0}".format(
                str(NewCode).replace(' ', '').replace('\n', '').replace('-1', '-'))
            ArchitectureInstance = Architecture.create_from_code(NewCode, manager, side, ArchitectureName)
            if NewCodeString not in self.Architectures.keys():
                loops = 0
                self.Architectures[NewCodeString] = None
                return ArchitectureInstance, False
            loops += 1
        return None, True

    def updateLastGeneration(self, generation_architectures, generation_results):
        scores = [generation["score"] for generation in generation_results]
        data, ArchCodes = {}, []
        for idx, arch in enumerate(generation_architectures):
            ArchCodeString = str(arch.code).replace(' ', '').replace('\n', '').replace('None', '-')
            ArchResult = scores[idx]
            data[ArchCodeString] = ArchResult
            ArchCodes.append(arch.code)
        self.LastGenerationDataDict = data
        self.LastGenerationArchCodes = ArchCodes
        self.LastGenerationRawResults = np.array(scores)
