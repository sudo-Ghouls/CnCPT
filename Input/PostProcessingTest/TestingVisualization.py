import os
import pickle

import matplotlib.cm as mplcm
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np

root_dir = r"D:\Thesis\CoralSea\2021-06-30-174827"
gens = []
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".pkl"):
            gen = pickle.load(open(os.path.join(root_dir, file), "rb"))
            gens.append(gen["results"])

all_data_organized = {}
for idx, gen in enumerate(gens):
    vsm_ships_all_gen = [gen[i]['vsm_ships'] for i in gen]
    vsm_aircraft_all_gen = [gen[i]['vsm_aircraft'] for i in gen]
    vscm_ships_all_gen = [gen[i]['vscm_ships'] for i in gen]
    vscm_aircraft_all_gen = [gen[i]['vscm_aircraft'] for i in gen]
    fam_ships_all_gen = [gen[i]['fam_ships'] for i in gen]
    fam_aircraft_all_gen = [gen[i]['fam_aircraft'] for i in gen]
    facm_ships_all_gen = [gen[i]['facm_ships'] for i in gen]
    facm_aircraft_all_gen = [gen[i]['facm_aircraft'] for i in gen]
    gen_1_blue = [
        np.mean((vsm_ships_all_gen[i], vsm_aircraft_all_gen[i], vscm_ships_all_gen[i], vscm_aircraft_all_gen[i])) for i
        in
        range(len(vsm_ships_all_gen))]
    gen_1_red = [
        np.mean((fam_ships_all_gen[i], fam_aircraft_all_gen[i], facm_ships_all_gen[i], facm_aircraft_all_gen[i]))
        for i in range(len(vsm_ships_all_gen))]
    scores = [gen[i]['score'] for i in gen]
    all_data_organized[idx] = {"blue": gen_1_blue,
                               "red": gen_1_red,
                               "score": scores}

NUM_COLORS = 21

cm = plt.get_cmap('rainbow')
cNorm = colors.Normalize(vmin=0, vmax=NUM_COLORS - 1)
scalarMap = mplcm.ScalarMappable(norm=cNorm, cmap=cm)
fig, axs = plt.subplots(2)
fig.suptitle('Vertically stacked subplots')

# old way:
# ax.set_color_cycle([cm(1.*i/NUM_COLORS) for i in range(NUM_COLORS)])
# new way:
axs[0].set_prop_cycle(color=[scalarMap.to_rgba(i) for i in range(NUM_COLORS)])
for gen in all_data_organized:
    axs[0].scatter(all_data_organized[gen]["blue"],
                   all_data_organized[gen]["red"], label=str(gen))

axs[0].set_xlabel("Blue Survivability (%)")
# plt.xlim([0, 100])
axs[0].set_ylabel("Red Attrition (%)")
# plt.ylim([0, 100])
axs[0].legend()

axs[1].set_prop_cycle(color=[scalarMap.to_rgba(i) for i in range(NUM_COLORS)])
box_plot_data = []
for gen in all_data_organized:
    box_plot_data.append(all_data_organized[gen]["score"])
axs[1].boxplot(box_plot_data)

axs[1].legend()

plt.show()

test = 1
