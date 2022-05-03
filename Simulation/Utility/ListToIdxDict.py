# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

def ListToIdxDict(list,starting_idx=0):
    MappingDict = {}
    for i,item in enumerate(list):
        MappingDict[item] = int(starting_idx+i)
    return MappingDict