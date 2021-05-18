# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

import numpy as np

from CnCPT.Simulation.Utility.SideEnum import SideEnum


class UnitFilter:
    """ Base class for filtering units

    Used to quickly and efficiently filter the units in the simulation

    """

    def __init__(self, labels, mask):
        """
        Initialize Unit Filter.
        :param names (array of strings): key words describing the masking functions to apply
        :param mask(function): method that returns list  of booleans for each "names" key word
        """
        self._filter_map = dict(zip(labels, range(len(labels))))
        self._vector_method = np.vectorize(mask)
        self._units = None
        self._mask = None

    def ingest(self, units):
        """
        Ingest new units into filter
        :param units (array/list): iterable of units
        """
        self._units = np.array(units)
        if self._units.size > 0:
            self._mask = np.array(self._vector_method(self._units), dtype=bool).transpose()

    def filter(self, **kwargs):
        if self._units is None or self._units.size == 0:
            return []
        mask = np.ones(self._mask.shape[0], dtype=bool)
        for name, value in kwargs.items():
            idx = self._filter_map[name]
            if value:
                mask &= self._mask[:, idx]
            else:
                mask &= ~self._mask[:, idx]
        return self._units[mask]

    @staticmethod
    def unit_mask(unit):
        blue = unit.side == SideEnum.BLUE
        red = unit.side == SideEnum.RED
        green = unit.side == SideEnum.GREEN
        return unit.alive, unit.moving(), blue, red, green, unit.docked, unit.sensors is not None, unit.weapons is not None, bool(unit.contacts)


def create_unit_filter():
    labels = ("alive", "moving", "blue", "red", "green", "docked", "has_sensors", "armed", "has_contacts")
    return UnitFilter(labels, UnitFilter.unit_mask)
