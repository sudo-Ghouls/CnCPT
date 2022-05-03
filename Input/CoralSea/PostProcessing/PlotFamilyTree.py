import itertools
import os
import pickle

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from networkx.utils import pairwise

path = "/Users/fleminggoolsby/Documents/MIT/System Design & Management/Thesis_Working_Area/CnCPT/Input/CoralSea/PostProcessing"
family_tree_log_path = os.path.join(path, "CnCPT_Family_Tree.pkl")
try:
    family_tree_log = pickle.load(open(family_tree_log_path, "rb"))
except:
    family_tree_log = None

# make the data frame
arch, p1, p2, gen, score= [], [], [], [],[]
ancestry = pd.DataFrame()

for architecture in family_tree_log:
    arch.append(architecture[0])
    gen.append(architecture[2])
    score.append(architecture[3])
    if architecture[1] is None:
        p1.append(None)
        p2.append(None)
    else:
        p1.append(architecture[1][0])
        p2.append(architecture[1][1])

ancestry = ancestry.from_dict({"Arch": arch,
                               "Parent_1": p1,
                               "Parent_2": p2,
                               "Generation": gen,
                               "Score":score})

num_gen = max(ancestry['Generation'])
subset_sizes = [30] * num_gen
subset_color = ["gold"] * num_gen
index = ancestry.index
uniqueArchs = dict.fromkeys(ancestry['Arch'])
arch_id_ref = dict(zip(uniqueArchs, range(len(uniqueArchs))))
custom_labels = {}


def multilayered_graph(*subset_sizes):
    extents = pairwise(itertools.accumulate((0,) + subset_sizes))
    layers = [range(start, end) for start, end in extents]
    layers = layers[::-1]
    G, gen = nx.Graph(), num_gen
    for (i, layer) in enumerate(layers):
        for idx in layer:
            generation = ancestry['Generation'][idx]
            arch_name = ancestry['Arch'][idx]
            custom_labels[idx] = arch_id_ref[arch_name]
            G.add_node(idx, layer=i, generation=(num_gen + 1) - generation, color='gold')
    for layer in layers:
        for node in layer:
            parent_1 = ancestry["Parent_1"][node]
            parent_2 = ancestry["Parent_2"][node]
            if parent_1 is not None:
                condition = ancestry[(ancestry['Arch'] == parent_1) & (ancestry['Generation'] == gen - 1)]
                parent_idx = condition.index.tolist()[0]
                G.nodes[node]['color'] = 'red'
                G.nodes[parent_idx]['color'] = 'blue'
                G.add_edge(node, parent_idx)
                condition = ancestry[(ancestry['Arch'] == parent_2) & (ancestry['Generation'] == gen - 1)]
                parent_idx = condition.index.tolist()[0]
                G.nodes[node]['color'] = 'red'
                G.nodes[parent_idx]['color'] = 'blue'
                G.add_edge(node, parent_idx)
        gen -= 1
    return G


G = multilayered_graph(*subset_sizes)
color = [data["color"] for v, data in G.nodes(data=True)]
pos = nx.multipartite_layout(G, subset_key="generation", scale=.1, align="horizontal")
plt.figure(figsize=(19, 6))
nx.draw(G, pos, node_color=color, with_labels=False, node_size=500)
nx.draw_networkx_labels(G, pos, custom_labels)
plt.axis("equal")
plt.show()

a = 1
