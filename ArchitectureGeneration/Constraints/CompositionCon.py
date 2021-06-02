# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE


class CompositionCon:
    def __init__(self, unitList, lowerBoundList, upperBoundList, locPolygonList):
        """
            Used for generating Composition constraints of an Architecture
        :param unitList: list of unit classes for use in force composition
        :param upperBoundList: list of int for lower bound of number of unit class; same length as unitList
        :param lowerBoundList: list of int for upper bound of number of unit class; same length as unitList
        :param locPolygonList: list of polygons for location start of unit class; same length as unitList
        """
        self.units = {}
        for idx, unit in enumerate(unitList):
            self.units[unit] = unitConstraint(lowerBoundList[idx], upperBoundList[idx], locPolygonList[idx])


class unitConstraint:
    def __init__(self, lowerBound, upperBound, Polygons):
        """
            Used for holding Unit constraint attributes
        :param lowerBound:
        :param upperBound:
        :param Polygon:
        """
        self.lowerBound = lowerBound
        self.upperBound = upperBound
        self.Polygons = Polygons
        self.maxNumber = upperBound
