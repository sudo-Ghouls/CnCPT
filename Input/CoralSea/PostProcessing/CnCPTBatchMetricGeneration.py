import itertools
import os
import pickle

import matplotlib.cm as mplcm
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from networkx.utils import pairwise
# root_dir = r"D:\Thesis\CnCPT_Tests\CoralSeaBombsAway\2021-07-26-211012"
# root_dir = r"D:\Thesis\CnCPT_Tests\CoralSeaCarrierCarnage\2021-07-26-174640"
root_dir = r"D:\Thesis\CnCPT_Tests\CoralSeaEndersGame\2021-07-26-103401"
output = os.path.join(root_dir, "CnCPT_Metrics")
""" --------------------------------------------------------  CONFIG  -----------------------------------------------"""
CnCPT_Distriubution = True
TradespaceQuartile = True
StackedGen = False
MCVar = False
family_anecestry_tree = True
ancestry_only = False
""" -----------------------------------------------------------------------------------------------------------------"""

try:
    os.mkdir(output)
except:
    pass
gens, gen_order, fig_idx = [], [], 0
arch, p1, p2, gen, score = [], [], [], [], []
family_tree_log_path = os.path.join(root_dir, "CnCPT_Family_Tree.pkl")
try:
    family_tree_log = pickle.load(open(family_tree_log_path, "rb"))
except:
    family_tree_log = None

for root, dirs, files in sorted(os.walk(root_dir)):
    for file in files:
        if file.endswith(".pkl"):
            if "CnCPT_Family_Tree.pkl" not in file:
                gen_number = int(file.strip("Generation_").strip("_Results.pkl"))
                geni = pickle.load(open(os.path.join(root_dir, file), "rb"))
                seeds = set(geni["results"].keys())
                gen_order.append(gen_number)
                gens.append(geni["results"])

CnCPT_Dataframe = pd.DataFrame()
CnCPT_Dataframe_MandV = pd.DataFrame()
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
                               "Score": score})

top_architectures = ancestry.sort_values(by=['Score'])[-10:]
top_architectures = top_architectures[['Arch','Generation','Score']]
filename = os.path.join(output, "CnCPT_Top_Architectures.txt")
top_architectures.to_csv(filename, index=None, sep=' ', mode='a')

if not ancestry_only:
    gens = [x for _, x in sorted(zip(gen_order, gens), key=lambda pair: pair[0])]
    for idx, generation in enumerate(gens):
        d, d0, d00, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10 = [], [], [], [], [], [], [], [], [], [], [], [], []
        d11, d12, d13, d14, d15, d16, d17, d18, d19, d20, d21, d22 = [], [], [], [], [], [], [], [], [], [], [], []
        for arch_key in generation:
            gen_data = generation[arch_key]
            d.append(arch_key)
            d0.append(gen_data['score_mean'])
            d00.append(gen_data['score_mean_variance'])
            d1.append(gen_data['score_var'])
            d2.append(gen_data['vsm_ships_mean'])
            d3.append(gen_data['vsm_ships_var'])
            d4.append(gen_data['vsm_aircraft_mean'])
            d5.append(gen_data['vsm_aircraft_var'])
            d6.append(gen_data['vscm_ships_mean'])
            d7.append(gen_data['vscm_ships_var'])
            d8.append(gen_data['vscm_aircraft_mean'])
            d9.append(gen_data['vscm_aircraft_var'])
            d10.append(gen_data['vscm_blue_mean'])
            d11.append(gen_data['vscm_blue_var'])
            d12.append(gen_data['fam_ships_mean'])
            d13.append(gen_data['fam_ships_var'])
            d14.append(gen_data['fam_aircraft_mean'])
            d15.append(gen_data['fam_aircraft_var'])
            d16.append(gen_data['facm_ships_mean'])
            d17.append(gen_data['facm_ships_var'])
            d18.append(gen_data['facm_aircraft_mean'])
            d19.append(gen_data['facm_aircraft_var'])
            d20.append(gen_data['facm_red_mean'])
            d21.append(gen_data['facm_red_var'])
            d22.append(idx)

        CnCPT_Dataframe_temp = pd.DataFrame.from_dict(
            {'arch_key': d, 'score_mean': d0, 'score_mean_variance': d00, 'score_var': d1, 'vsm_ships_mean': d2,
             'vsm_ships_var': d3, 'vsm_aircraft_mean': d4, 'vsm_aircraft_var': d5, 'vscm_ships_mean': d6,
             'vscm_ships_var': d7, 'vscm_aircraft_mean': d8, 'vscm_aircraft_var': d9, 'vscm_blue_mean': d10,
             'vscm_blue_var': d11, 'fam_ships_mean': d12, 'fam_ships_var': d13, 'fam_aircraft_mean': d14,
             'fam_aircraft_var': d15, 'facm_ships_mean': d16, 'facm_ships_var': d17, 'facm_aircraft_mean': d18,
             'facm_aircraft_var': d19, 'facm_red_mean': d20, 'facm_red_var': d21, 'generation': d22})
        CnCPT_Dataframe = pd.concat([CnCPT_Dataframe, CnCPT_Dataframe_temp])
        CnCPT_Dataframe_MandV_temp = pd.Series(
            {'score_mean': np.mean(d0), 'score_mean_variance': np.mean(d00),
             'score_var': np.mean(d1), 'vsm_ships_mean': np.mean(d2),
             'vsm_ships_var': np.mean(d3), 'vsm_aircraft_mean': np.mean(d4), 'vsm_aircraft_var': np.mean(d5),
             'vscm_ships_mean': np.mean(d6),
             'vscm_ships_var': np.mean(d7), 'vscm_aircraft_mean': np.mean(d8), 'vscm_aircraft_var': np.mean(d9),
             'vscm_blue_mean': np.mean(d10),
             'vscm_blue_var': np.mean(d11), 'fam_ships_mean': np.mean(d12), 'fam_ships_var': np.mean(d13),
             'fam_aircraft_mean': np.mean(d14),
             'fam_aircraft_var': np.mean(d15), 'facm_ships_mean': np.mean(d16), 'facm_ships_var': np.mean(d17),
             'facm_aircraft_mean': np.mean(d18),
             'facm_aircraft_var': np.mean(d19), 'facm_red_mean': np.mean(d20), 'facm_red_var': np.mean(d21),
             'generation': int(np.mean(d22))}, name=int(np.mean(d22)))
        CnCPT_Dataframe_MandV = pd.concat([CnCPT_Dataframe_MandV, CnCPT_Dataframe_MandV_temp], axis=1, sort=False)

    CnCPT_Dataframe_MandV = CnCPT_Dataframe_MandV.transpose()
    CnCPT_Dataframe["score_var_abs"] = np.abs(CnCPT_Dataframe["score_var"])
    NUM_COLORS = len(gens)
    cm = plt.get_cmap('rainbow')
    cNorm = colors.Normalize(vmin=0, vmax=NUM_COLORS - 1)
    scalarMap = mplcm.ScalarMappable(norm=cNorm, cmap=cm)



if CnCPT_Distriubution:
    x = CnCPT_Dataframe['score_mean'].values  # returns a numpy array
    max_x_data = max(x)
    min_x_data = min(x)
    plt.figure(fig_idx, figsize=(10, 2 * len(gens)))
    ax = sns.histplot(data=CnCPT_Dataframe, x='score_mean', binwidth=1, color="black")
    ax.set_xlabel("Score",fontsize = 18)
    ax.set_ylabel("Count", fontsize=18)
    ax.set_xlim([min_x_data - 1, max_x_data + 1])
    plt.tight_layout()
    filename = os.path.join(output, "Combined_Score_Distribution_Histogram.png")
    plt.savefig(filename)
    plt.close()
    fig_idx += 1

    cmap = [scalarMap.to_rgba(i) for i in range(NUM_COLORS)]
    plt.figure(fig_idx, figsize=(10, 2 * len(gens)))
    for i in range(len(gens)):
        plt.subplot(len(gens), 1, i + 1)
        ax = sns.histplot(data=CnCPT_Dataframe[CnCPT_Dataframe["generation"] == i], x='score_mean', binwidth=1,
                          color=cmap[i])
        ax.set_xlim([min_x_data - 1, max_x_data + 1])
        ax.set_ylabel("Generation {0}".format(i+1),fontsize = 18)
        ax.set_xlabel("Score",fontsize = 18)

    plt.tight_layout()
    filename = os.path.join(output, "Score_Distribution_Histogram.png")
    plt.savefig(filename)
    plt.close()
    fig_idx += 1

if TradespaceQuartile:
    all_data_organized = {}
    num_gen = max(ancestry['Generation'])
    for idx, gen in enumerate(gens):
        vsm_ships_all_gen = [gen[i]['vsm_ships_mean'] for i in gen]
        vsm_aircraft_all_gen = [gen[i]['vsm_aircraft_mean'] for i in gen]
        vscm_ships_all_gen = [gen[i]['vscm_ships_mean'] for i in gen]
        vscm_aircraft_all_gen = [gen[i]['vscm_aircraft_mean'] for i in gen]
        fam_ships_all_gen = [gen[i]['fam_ships_mean'] for i in gen]
        fam_aircraft_all_gen = [gen[i]['fam_aircraft_mean'] for i in gen]
        facm_ships_all_gen = [gen[i]['facm_ships_mean'] for i in gen]
        facm_aircraft_all_gen = [gen[i]['facm_aircraft_mean'] for i in gen]
        facm_red_all_gen = [gen[i]['facm_red_mean'] for i in gen]
        vscm_blue_all_gen = [gen[i]['vscm_blue_mean'] for i in gen]
        gen_1_blue = [
            np.mean((vsm_ships_all_gen[i], vsm_aircraft_all_gen[i], vscm_ships_all_gen[i], vscm_aircraft_all_gen[i]))
            for i
            in
            range(len(vsm_ships_all_gen))]
        gen_1_red = [
            np.mean((fam_ships_all_gen[i], fam_aircraft_all_gen[i], facm_ships_all_gen[i], facm_aircraft_all_gen[i]))
            for i in range(len(vsm_ships_all_gen))]
        scores = [gen[i]['score_mean'] for i in gen]
        all_data_organized[idx] = {"blue": vscm_blue_all_gen,
                                   "red": facm_red_all_gen,
                                   "score_mean": scores}

    fig, axs = plt.subplots(2, figsize=(9.6, 10.8))
    max_blue, min_blue = max(all_data_organized[1]["blue"]), min(all_data_organized[1]["blue"])
    max_red, min_red = max(all_data_organized[1]["red"]), min(all_data_organized[1]["red"])
    axs[0].set_prop_cycle(color=[scalarMap.to_rgba(i) for i in range(NUM_COLORS)])
    for gen in all_data_organized:
        maxb, minb = max(all_data_organized[gen]["blue"]), min(all_data_organized[gen]["blue"])
        maxr, minr = max(all_data_organized[gen]["red"]), min(all_data_organized[gen]["red"])
        if maxb > max_blue:
            max_blue = maxb
        if maxr > max_red:
            max_red = maxr
        if minb < min_blue:
            min_blue = minb
        if minr < min_red:
            min_red = minr
        axs[0].scatter(all_data_organized[gen]["blue"],
                       all_data_organized[gen]["red"], edgecolors="black",
                       label="Generation {0}".format(str(gen + 1)))

    axs[0].set_xlabel("Blue Survivability (%)")
    axs[0].set_xlim([min_blue - 1, max_blue + 1])
    axs[0].set_ylabel("Red Attrition (%)")
    axs[0].set_ylim([min_red - 1, max_red + 1])
    axs[0].legend()
    plt.tight_layout(pad=1.5)

    axs[1].set_prop_cycle(color=[scalarMap.to_rgba(i) for i in range(NUM_COLORS)])
    box_plot_data = []
    # for gen in all_data_organized:
    #     box_plot_data.append(all_data_organized[gen]["score_mean"])
    # axs[1].boxplot(box_plot_data)
    cmap = [scalarMap.to_rgba(i) for i in range(NUM_COLORS)]
    for gen in all_data_organized:
        bp = axs[1].boxplot(all_data_organized[gen]["score_mean"],
                            positions=[gen + 1],
                            widths=(.5),
                            patch_artist=True)
        for patch in bp['boxes']:
            patch.set(color='black')
            patch.set(facecolor=cmap[gen])

    axs[1].set_xlabel("Generation")
    axs[1].set_ylabel("Score")
    filename = os.path.join(output, "Tradespace_Quartile_1.png")
    plt.savefig(filename)
    fig_idx += 1
    plt.close()

    fig, axs = plt.subplots(2, figsize=(9.6, 10.8))
    axs[0].set_prop_cycle(color=[scalarMap.to_rgba(i) for i in range(NUM_COLORS)])
    x, y_mean, y_min, y_max = [], [], [], []
    for idx, gen in enumerate(all_data_organized):
        mean_value_generation = np.mean(all_data_organized[gen]["score_mean"])
        min_value_generation = np.min(all_data_organized[gen]["score_mean"])
        max_value_generation = np.max(all_data_organized[gen]["score_mean"])
        data_y = all_data_organized[gen]["score_mean"]
        gen_idx = [idx + 1] * len(data_y)
        axs[0].scatter(gen_idx, data_y, label=str(gen + 1), edgecolors="black")
        x.append(idx + 1)
        y_mean.append(mean_value_generation)
        y_min.append(min_value_generation)
        y_max.append(max_value_generation)

    z = np.polyfit(x, y_max, 1)
    p = np.poly1d(z)
    axs[0].plot(x, list(p(x)), linestyle=':', label="max_trendline", color="green", linewidth=2)
    z = np.polyfit(x, y_mean, 1)
    p = np.poly1d(z)
    axs[0].plot(x, list(p(x)), linestyle='-.', label="mean_trendline", color="black", linewidth=2)
    z = np.polyfit(x, y_min, 1)
    p = np.poly1d(z)
    axs[0].plot(x, list(p(x)), linestyle=':', label="min_trendline", color="red", linewidth=2)

    custom_lines = [Line2D([0], [0], linestyle=':', color='green'),
                    Line2D([0], [0], linestyle='-.', color='black'),
                    Line2D([0], [0], linestyle=':', color='red')]

    axs[0].legend(custom_lines, ['Maximum Score Trendline', 'Mean Score Trendline', "Minimum Score Trendline"])
    axs[0].set_xticks(range(1, num_gen + 1))
    axs[0].set_xlabel("Generation")
    axs[0].set_ylabel("Score")

    axs[1].set_prop_cycle(color=[scalarMap.to_rgba(i) for i in range(NUM_COLORS)][3:])
    gen_colors = [scalarMap.to_rgba(i) for i in range(NUM_COLORS)]
    for idx, gen in enumerate(all_data_organized):
        data_gen = ancestry[ancestry['Generation'] == idx + 1]
        data_breed = data_gen[data_gen['Parent_1'].notnull()]
        data_breed = data_breed["Score"].tolist()
        if len(data_breed) != 0:
            gen_idx = [idx + 1] * len(data_breed)
            axs[1].scatter(gen_idx, data_breed, label="{0} - Breed".format(str(gen + 1)), color="black")
    for idx, gen in enumerate(all_data_organized):
        data_gen = ancestry[ancestry['Generation'] == idx + 1]
        data_rand = data_gen[data_gen['Parent_1'].isnull()]
        data_rand = data_rand["Score"].tolist()
        gen_idx = [idx + 1] * len(data_rand)
        axs[1].scatter(gen_idx, data_rand, label="{0} - Random".format(str(gen + 1)), edgecolors="black", color="white")

    axs[1].set_xlabel("Generation")
    axs[1].set_ylabel("Score")
    custom_lines = [Line2D([0], [0], marker='o', color='w', label='Scatter',
                           markerfacecolor='black', markersize=10, markeredgecolor="black"),
                    Line2D([0], [0], marker='o', color='w', label='Scatter',
                           markerfacecolor='white', markersize=10, markeredgecolor="black")]
    axs[1].legend(custom_lines, ['Generated via Breeding', 'Generated via Random Draw'])
    axs[1].set_xticks(range(1, num_gen + 1))
    filename = os.path.join(output, "Tradespace_Quartile_2.png")
    plt.tight_layout(pad=1.5)
    plt.savefig(filename)
    fig_idx += 1
    plt.close()

if StackedGen:
    fig, axs = plt.subplots(1, len(gens))
    fig.supxlabel('Generation')
    for i in range(len(gens)):
        for set in gens[i]["results"]:
            score = gens[i]["results"][set]['score']
            axs[i].set_xlim(0, 1)
            axs[i].set_ylim(0, 100)
            axs[i].add_patch(Rectangle((0, score - .5), 1, 1))
            if i == 0:
                axs[i].set_ylabel("Score [0-100]")
                axs[i].set_yticks([0, 25, 50, 75, 100])
            else:
                axs[i].set_ylabel("")
                axs[i].set_yticks([])
            axs[i].set_xlabel(i)
            axs[i].set_xticks([])
    plt.tight_layout()
    filename = os.path.join(output, "Stacked_Generation.png")
    plt.savefig(filename)
if MCVar:
    fig, axs = plt.subplots(2, round(len(gens) / 2))
    # fig, axs = plt.subplots(1, 1)
    # fig.supxlabel('Generation')
    NUM_COLORS = 10
    cm = plt.get_cmap('rainbow')
    cNorm = colors.Normalize(vmin=0, vmax=NUM_COLORS - 1)
    scalarMap = mplcm.ScalarMappable(norm=cNorm, cmap=cm)
    for i in range(len(gens)):
        for h, set in enumerate(gens[i]["results"]):
            set_score = gens[i]["results"][set]['score_mean']
            seed_data = gens[i]["results"][set]["individual_seed_data_mean"]
            vsm_ships_all_seed_data = [seed_data[j]['vsm_ships'] for j in seed_data]
            vsm_aircraft_all_seed_data = [seed_data[j]['vsm_aircraft'] for j in seed_data]
            vscm_ships_all_seed_data = [seed_data[j]['vscm_ships'] for j in seed_data]
            vscm_aircraft_all_seed_data = [seed_data[j]['vscm_aircraft'] for j in seed_data]
            fam_ships_all_seed_data = [seed_data[j]['fam_ships'] for j in seed_data]
            fam_aircraft_all_seed_data = [seed_data[j]['fam_aircraft'] for j in seed_data]
            facm_ships_all_seed_data = [seed_data[j]['facm_ships'] for j in seed_data]
            facm_aircraft_all_seed_data = [seed_data[j]['facm_aircraft'] for j in seed_data]
            seed_data_1_blue = [
                np.mean((vsm_ships_all_seed_data[j], vsm_aircraft_all_seed_data[j], vscm_ships_all_seed_data[j],
                         vscm_aircraft_all_seed_data[j])) for j
                in
                range(len(vsm_ships_all_seed_data))]
            seed_data_1_red = [
                np.mean((fam_ships_all_seed_data[j], fam_aircraft_all_seed_data[j], facm_ships_all_seed_data[j],
                         facm_aircraft_all_seed_data[j]))
                for j in range(len(vsm_ships_all_seed_data))]
            j, k = divmod(i, round(len(gens) / 2))
            axs[j, k].scatter(seed_data_1_blue,
                              seed_data_1_red, label=set,
                              color=scalarMap.to_rgba(h))
            axs[j, k].set_xlim(0, 100)
            axs[j, k].set_ylim(0, 100)
    plt.tight_layout()
    filename = os.path.join(output, "MC_Variance.png")
    plt.savefig(filename)

if family_anecestry_tree:
    num_gen = max(ancestry['Generation'])
    num_sets_per_gen = len(ancestry[ancestry['Generation'] == 1])
    subset_sizes = [num_sets_per_gen] * num_gen
    index = ancestry.index
    uniqueArchs = dict.fromkeys(ancestry['Arch'])
    arch_id_ref = dict(zip(uniqueArchs, range(len(uniqueArchs))))
    custom_labels = {}


    def multilayered_graph(*subset_sizes):
        extents = pairwise(itertools.accumulate((0,) + subset_sizes))
        layers = [range(start, end) for start, end in extents]
        layers = layers[::-1]
        G, gen = nx.Graph(), num_gen
        child_nodes, parent_nodes = [], []
        best_score, best_score_node = 0, 0
        for (i, layer) in enumerate(layers):
            for idx in layer:
                generation = ancestry['Generation'][idx]
                arch_name = ancestry['Arch'][idx]
                custom_labels[idx] = arch_id_ref[arch_name]
                G.add_node(idx, layer=i, generation=(num_gen + 1) - generation, color='whitesmoke')
        for layer in layers:
            for node in layer:
                if ancestry["Score"][node] > best_score:
                    best_score = ancestry["Score"][node]
                    best_score_node = node
                parent_1 = ancestry["Parent_1"][node]
                parent_2 = ancestry["Parent_2"][node]
                if parent_1 is not None:
                    condition = ancestry[(ancestry['Arch'] == parent_1) & (ancestry['Generation'] == gen - 1)]
                    parent_idx = condition.index.tolist()[0]
                    child_nodes.append(node)
                    parent_nodes.append(parent_idx)
                    G.add_edge(node, parent_idx)
                    condition = ancestry[(ancestry['Arch'] == parent_2) & (ancestry['Generation'] == gen - 1)]
                    parent_idx = condition.index.tolist()[0]
                    parent_nodes.append(parent_idx)
                    G.add_edge(node, parent_idx)
            gen -= 1
        for node in child_nodes:
            G.nodes[node]['color'] = 'lightsalmon'
        for node in parent_nodes:
            G.nodes[node]['color'] = 'skyblue'
        G.nodes[best_score_node]['color'] = 'gold'
        return G


    G = multilayered_graph(*subset_sizes)
    color = [data["color"] for v, data in G.nodes(data=True)]
    pos = nx.multipartite_layout(G, subset_key="generation", align="horizontal")
    array_op = lambda x: (x[0] * 1, x[1] * 2.0)
    pos = {p: np.array(array_op(pos[p])) for p in pos}
    plt.figure(figsize=(28, 21))
    nx.draw(G, pos, node_color=color, with_labels=False, node_size=1500)
    nx.draw_networkx_labels(G, pos, custom_labels, font_size=18)
    reference_node_linear_pos = range(0, len(G.nodes), num_sets_per_gen)
    i, gen_label_dict, x_off_set_amount, y_off_set_amount = 1, {}, None, None
    for i, l_idx in enumerate(reference_node_linear_pos):
        if x_off_set_amount is None and y_off_set_amount is None:
            x_off_set_amount = abs(pos[l_idx][0] - pos[l_idx + 1][0])
            y_off_set_amount = 0
        y_pos = pos[l_idx][1] - y_off_set_amount
        if l_idx != 0:
            x_pos = pos[l_idx - 1][0] - x_off_set_amount
        else:
            x_pos = pos[l_idx + num_sets_per_gen - 1][0] - x_off_set_amount
        gen_label_dict["Generation {0}".format(i + 1)] = (x_pos, y_pos)
    for entry in gen_label_dict:
        x, y = gen_label_dict[entry]
        plt.text(x, y, entry, rotation="vertical", verticalalignment='center', fontsize=16,
                 bbox=dict(facecolor='whitesmoke', alpha=0.5, ))
    filename = os.path.join(output, "Family_Tree.png")
    plt.savefig(filename)
