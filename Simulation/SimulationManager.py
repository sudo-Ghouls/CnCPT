# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE
import itertools
import sys
import time

from simpy.core import *

from CnCPT.Simulation.DataLogging import DataLogger
from CnCPT.Simulation.GeographyPhysics import Geography
from CnCPT.Simulation.Utility.UnitFilter import create_unit_filter


class SimulationManager(Environment):
    """ Class manages the simulation "truth" and progresses time forward

    """

    def __init__(self, units, networks, constants, output_path, start_time=-100000, end_time=-100000):
        super(SimulationManager, self).__init__(initial_time=start_time)
        self.all_units = units
        self.all_units_map = {u.name: u for u in self.all_units}
        self.networks = networks
        self.constants = constants
        self._next_time = None
        self.start_time = start_time
        self.end_time = end_time

        self.start_real_time = time.clock()
        self.current_real_time = time.clock()
        self.elapsed_real_time = self.current_real_time - self.start_real_time

        self.time_step = 0
        self.distances = {}
        self.bearings = {}
        self.unit_filter = create_unit_filter()

        self.output_path = output_path
        self.data_logger = DataLogger(output_path)

        if constants["simulation_map_bounds"] is not None:
            self.simulation_map_bounds = constants["simulation_map_bounds"]
            self.Geography = Geography(self.all_units, self.simulation_map_bounds)
        else:
            self.simulation_map_bounds = ((-180, -180),
                                          (-180, 180),
                                          (180, 180),
                                          (180, -180),
                                          (-180, -180))
            self.Geography = Geography(self.all_units, self.simulation_map_bounds)

    def step(self):
        """Process the next event.

        Raise an :exc:`EmptySchedule` if no further events are available.

        """
        try:
            self._next_time, _, _, event = heappop(self._queue)
        except IndexError:
            raise EmptySchedule()

        # Update Underlying environment characteristics
        sim_time_elapsed = float(self._next_time - self._now)
        self._now = self._next_time
        if sim_time_elapsed > 0:
            self.time_step = sim_time_elapsed
            self.update_environment()  # only update environment when time progresses
            self.all_units_map = {u.name: u for u in self.all_units}  # update unit map
        self.current_real_time = time.clock()
        self.elapsed_real_time = self.current_real_time - self.start_real_time
        # self._now = self._next_time

        # Process callbacks of the event. Set the events callbacks to None
        # immediately to prevent concurrent modifications.
        callbacks, event.callbacks = event.callbacks, None  # type: ignore
        for callback in callbacks:
            callback(event)

        if not event._ok and not hasattr(event, '_defused'):
            # The event has failed and has not been defused. Crash the
            # environment.
            # Create a copy of the failure exception with a new traceback.
            exc = type(event._value)(*event._value.args)
            exc.__cause__ = event._value
            raise exc

    def update_environment(self):
        self.update_status_bar()
        self.update_state()
        self.adjudicate()
        self.sense()
        self.update_unit_contacts()
        self.communicate()
        self.spawn()
        self.propagate()
        self.log()

    def update_status_bar(self):
        fraction_complete = float(self._now - self.start_time) / (self.end_time - self.start_time)
        status = ""
        if fraction_complete >= 1:
            status = "Done.\r\n"
        num_blocks = int(round(25 * fraction_complete))
        bar_string = "#" * num_blocks + "-" * (25 - num_blocks)
        text_1 = "\r[{0}] {1:5.1f}%".format(bar_string, fraction_complete * 100)
        text_time = self._now
        speed = ((self._now - self.start_time) / self.elapsed_real_time)
        text_2 = "[Time: {0}] [Speed: {1} x Realtime] {2}".format(text_time, speed, status)
        text = text_1 + text_2
        try:
            sys.stdout.write((text).encode("utf8"))
        except TypeError:
            sys.stdout.write(text)
        sys.stdout.flush()

    def spawn(self):
        """

        :return:
        """
        for unit in self.all_units:
            if bool(unit.spawn):
                for new_unit_key in unit.spawn:
                    new_unit = unit.spawn[new_unit_key]
                    new_unit.kinematics.set_location(unit=unit)
                    new_unit.register(self, self.constants)
                    self.all_units.append(new_unit)
                unit.spawn = {}

    def adjudicate(self):
        """

        :return:
        """
        if len(self.all_units) == 0:
            return
        units_with_weapons = self.unit_filter.filter(alive=True, armed=True, docked=False)
        for unit in units_with_weapons:
            for weapon in unit.weapons:
                weapon.engage(unit, self)

    def update_state(self):
        """
        This function maintains the state of all units in the scenario
        :return:
        """
        self.Geography.update(self.all_units)
        self.unit_filter.ingest(list(self.all_units))

    def propagate(self):
        """
        This function propagates all units forward in time based on their current velocity and heading
        :return:
        """
        if len(self.all_units) == 0:
            return
        units_to_propagate = self.unit_filter.filter(alive=True, moving=True)

        # for unit in units_to_propagate:
        #     Geography.propagate(unit, self.time_step)
        list(map(Geography.propagate, units_to_propagate, itertools.repeat(self.time_step, len(units_to_propagate))))

    def sense(self, max_retention_time=12000):
        """
        evaluates all the sensing capability on board units in the scenario
        :return:
        """
        if len(self.all_units) == 0:
            return
        units_with_sensors = self.unit_filter.filter(alive=True, has_sensors=True, docked=False)
        for unit in units_with_sensors:
            for sensor in unit.sensors:
                sensor.process(unit, self)
                self.update_contacts(sensor.contacts, self.now, max_retention_time)
                unit.contacts.update(sensor.contacts)

    def update_unit_contacts(self, max_retention_time=12000):
        """
            removes old (based on max retention time and dead contacts from a units contact list (cheats using truth
            data)
        :param max_retention_time: hold time for contacts in seconds
        :return:
        """
        units_with_contacts = self.unit_filter.filter(alive=True, has_contacts=True, docked=False)

        for unit in units_with_contacts:
            self.update_contacts(unit.contacts, self.now, max_retention_time)

    @staticmethod
    def update_contacts(contacts, current_time, max_retention_time):
        keys_to_pop = []
        for contact_key in contacts:
            time_elapsed = current_time - contacts[contact_key].time
            if time_elapsed > max_retention_time:
                keys_to_pop.append(contact_key)
            if contacts[contact_key].truth_unit.alive is False:
                keys_to_pop.append(contact_key)

        for key in keys_to_pop:
            _ = contacts.pop(key)

    def communicate(self):
        """
        This function transmits and receives any information shared via communications in the last timestep
        :return:
        """

    def log(self):
        """

        :return:
        """

        self.data_logger.dump_units_to_file(self)
        self.data_logger.update_formatted_unit_data(self)
