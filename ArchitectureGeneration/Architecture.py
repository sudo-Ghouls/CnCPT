# Author: Thomas C.F. Goolsby - tgoolsby@mit.edu
# This file was created in support of the CNCPT Thesis
# Fall 2020 - EM.THE
import os

import matplotlib.pyplot as plt
import networkx as nx

from Simulation.Communication.Network import Network
from Simulation.Units.UnitGroup import UnitGroup
from Simulation.Utility.graph_related import hierarchy_pos


class Architecture:
    def __init__(self, units, name, side=None, ArchCode=None, parents=None):
        self.units = units
        self.name = name
        self.side = side
        self.ArchCode = ArchCode
        self.parents = parents

    @staticmethod
    def create_from_code(ArchCode, CONOPCon, CompCon, LeadershipPriority, side, name, parents=None):
        units_ungrouped, units_grouped, code_idx, polygon_groups = [], [], 0, {}
        unit_keys = CompCon.units.keys()
        max_num_per_unit = [CompCon.units[unit].maxNumber for unit in unit_keys]
        for class_idx, UnitClass in enumerate(unit_keys):
            for unit_idx in range(max_num_per_unit[class_idx]):
                if ArchCode[code_idx] >= 0:
                    unit_name = "{0}_{1}_{2}".format(side.name, UnitClass.__name__, unit_idx)
                    unit_behavior = CONOPCon.units[UnitClass].CONOPs[ArchCode[code_idx]]
                    spawn_polygon = CompCon.units[UnitClass].Polygons[ArchCode[code_idx + 1]]
                    new_unit = UnitClass(name=unit_name, behavior=unit_behavior, spawn_polygon=spawn_polygon, side=side)
                    update_polygon_group(new_unit, spawn_polygon, polygon_groups)
                    units_ungrouped.append(new_unit)
                code_idx += 2

        sort_polygon_group_by_leadership(polygon_groups, LeadershipPriority)
        for idx, polygon_group in enumerate(polygon_groups):
            polygon_unit_group = UnitGroup.construct_unit_group(polygon_group,
                                                                polygon_groups[polygon_group],
                                                                leader=polygon_groups[polygon_group][0])
            units_grouped += polygon_unit_group
        Network(name, units_grouped)
        return Architecture(units_grouped, name, side, ArchCode, parents)

    @staticmethod
    def create_arch_from_string(arch_code, CONOPCon, CompCon, LeadershipPriority, side, name="Default"):
        """ example arch_code = "202213011323--232110--13--0201----1312--22231322001101--0300----00"
        """
        arch_code_int = []
        for val in arch_code:
            if val == '-':
                arch_code_int.append(-1)
            else:
                arch_code_int.append(int(val))
        ArchInstance = Architecture.create_from_code(arch_code_int, CONOPCon, CompCon, LeadershipPriority, side, name)
        return ArchInstance

    def generate_arch_figures(self, output_path):
        unit_data_graph = nx.Graph()
        area_data_graph = nx.Graph()
        behavior_data_graph = nx.Graph()
        unit_names, leaders, behaviors, areas = [], [], [], []
        for unit in self.units:
            names = unit.name.split('_')
            unit_name = names[1][0:2] + names[-1]
            unit_names.append(unit_name)
            if unit.group is not None:
                names = unit.group.leader.name.split('_')
                group_leader_name = names[1][0:2] + names[-1]
                leaders.append(group_leader_name)
                area_name = unit.group.name.replace(self.side.name + "_", '').replace("_", ' ')
                areas.append(area_name)
            else:
                leaders.append(None)
                areas.append(None)
            bname = unit.my_brain.__name__.replace('behavior_', '')
            behaviors.append(bname)
        unique_leaders = set(leaders)
        unique_behaviors = set(behaviors)
        unique_areas = set(areas)
        unit_data_graph.add_node("Leaders", color="whitesmoke")
        area_data_graph.add_node("Areas", color="lightgreen")
        behavior_data_graph.add_node("Behaviors", color="lightskyblue")
        for name in unit_names:
            unit_data_graph.add_node(name, color="whitesmoke")
            area_data_graph.add_node(name, color="whitesmoke")
            behavior_data_graph.add_node(name, color="whitesmoke")
        for area in unique_areas:
            area_data_graph.add_node(area, color="lightgreen")
            area_data_graph.add_edge("Areas", area, color="lightgreen")
        for behavior in unique_behaviors:
            behavior_data_graph.add_node(behavior, color="lightskyblue")
            behavior_data_graph.add_edge("Behaviors", behavior, color="lightskyblue")
        for leader in unique_leaders:
            unit_data_graph.add_edge("Leaders", leader, color="black")
        for idx, name in enumerate(unit_names):
            if name != leaders[idx]:
                unit_data_graph.add_edge(leaders[idx], name, color='black')
            area_data_graph.add_edge(areas[idx], name, color='lightgreen')
            behavior_data_graph.add_edge(behaviors[idx], name, color='lightskyblue')
        for idx, data in enumerate([(unit_data_graph, "Leaders"),
                                    (area_data_graph, "Areas"),
                                    (behavior_data_graph, "Behaviors")]):
            data_graph = data[0]
            n_color = [data['color'] for v, data in data_graph.nodes(data=True)]
            e_color = [data[2]['color'] for data in data_graph.edges(data=True)]
            plt.figure(figsize=(12, 5))
            nx.draw(data_graph, node_color=n_color, edge_color=e_color, with_labels=True, node_size=1000,
                    pos=hierarchy_pos(data_graph, width=2, vert_gap=2, vert_loc=1, root=data[1]))
            filename = os.path.join(output_path, "Architecture_Overview_Graphic_{0}.png".format(idx))
            plt.savefig(filename)
            plt.close()
        a = 1


def update_polygon_group(unit, spawn_polygon, polygon_groups_dict):
    if spawn_polygon.name in polygon_groups_dict.keys():
        polygon_groups_dict[spawn_polygon.name].append(unit)
    else:
        polygon_groups_dict[spawn_polygon.name] = [unit]


def sort_polygon_group_by_leadership(polygon_groups, leadership_priority):
    rank_map, rank = {}, 1
    for unit_class in leadership_priority:
        rank_map[unit_class] = rank
        rank += 1

    for polygon_group in polygon_groups:
        units = polygon_groups[polygon_group]
        units_rank = [rank_map[unit.__class__] for unit in units]
        units_sorted = [u for _, u in sorted(zip(units_rank, units), key=lambda x: x[0])]
        polygon_groups[polygon_group] = units_sorted
