# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from Simulation.Communication.Message import MessageType


def communicate(self):
    """
    This function transmits and receives any information shared via communications in the last timestep
    :return:
    """
    alive_and_active_units = self.unit_filter.filter(alive=True, docked=False)
    for unit in alive_and_active_units:
        for message in unit.new_messages:
            if message.type is MessageType.ISR_CONTACT:
                unit.contacts.update(message.content)
            else:
                unit.tasks.add(message.content)
