# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE

from copy import deepcopy


def auto_network_architectures(all_units):
    networks = []
    return networks


class Network:
    def __init__(self, name, units):
        """

        :param name:
        :param units:
        """
        self.name = name
        self.units = units
        self.unit_map = {u.name: u for u in self.units}
        for unit in units:
            unit.network = self

    def send_message(self, message, sender, receiver):
        """

        :param message:
        :param sender:
        :param receiver:
        :return:
        """
        new_message = message
        new_message.network = self
        new_message.sender = sender
        new_message.receiver = receiver
        receiver.new_messages.append(new_message)

    def broadcast_message(self, message, sender):
        """

        :param message:
        :param sender:
        :return:
        """
        for receiver in self.units:
            new_message = deepcopy(message)
            new_message.network = self
            new_message.sender = sender
            new_message.receiver = receiver
            receiver.new_messages.append(new_message)
