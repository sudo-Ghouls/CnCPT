# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


class CONOPCon:
    def __init__(self, unitList, CONOPList):
        """
            Used for generating Composition constraints of an Architecture
        :param unitList: list of unit classes for use in force composition
        :param CONOPList: list of lists of CONOPs for unit classes; outer list same length as unitList
        """
        self.units = {}
        for idx, unit in enumerate(unitList):
            self.units[unit] = ConopConstraint(CONOPList[idx])


class ConopConstraint:
    def __init__(self,CONOPList):
        """
            Used for holding Unit constraint attributes
        :param lowerBound:
        :param upperBound:
        :param Polygon:
        """
        self.CONOPs = CONOPList
        self.maxNumConop = len(CONOPList)
