import os
import pickle

import matplotlib.cm as mplcm
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np

root_dir = r"D:\Thesis\CoralSeaConstrained_MC_3_Gen_15_RS_30_80FACM_20SVSCM\2021-07-16-114710"
gens = []
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".pkl"):
            gen = pickle.load(open(os.path.join(root_dir, file), "rb"))
            gens.append(gen)

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
plt.show()
