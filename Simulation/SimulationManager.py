# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE
import time

import numpy as np
from simpy.core import *

from Simulation.Communication.core import communicate
from Simulation.DataManagement.DataLogging import DataLogger, log, update_status_bar
from Simulation.Engagement.core import adjudicate
from Simulation.GeographyPhysics.Geography import Geography, propagate
from Simulation.Sensing.core import sense, update_system_contacts
from Simulation.Units.core import spawn, update_state
from Simulation.Utility.UnitFilter import create_unit_filter


class SimulationManager(Environment):
    """ Class manages the simulation "truth" and progresses time forward

    """

    def __init__(self, units, networks, constants, output_path, start_time=-100000, end_time=-100000,
                 full_data_logging=True, seed=0):
        super(SimulationManager, self).__init__(initial_time=start_time)
        self.all_units = units
        self.all_units_map = {u.name: u for u in self.all_units}
        self.networks = networks
        self.constants = constants
        self._next_time = None
        self.start_time = start_time
        self.end_time = end_time
        self.random = np.random.RandomState(seed)

        self.start_real_time = time.clock()
        self.current_real_time = time.clock()
        self.elapsed_real_time = self.current_real_time - self.start_real_time

        self.time_step = 0
        self.distances = {}
        self.bearings = {}
        self.unit_filter = create_unit_filter()

        self.full_data_logging = full_data_logging
        self.output_path = output_path
        self.data_logger = DataLogger(output_path)
        self.kill_log = {}
        self.isr_log = {}
        self.weapon_log = {}
        self.drawdown_log = {"blue_ships": {},
                             "blue_aircraft": {},
                             "red_ships": {},
                             "red_aircraft": {}}

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
        update_status_bar(self)
        update_state(self)
        adjudicate(self)
        sense(self)
        update_system_contacts(self)
        communicate(self)
        spawn(self)
        propagate(self)
        log(self)
