import os
import pickle

import matplotlib.cm as mplcm
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np

root_dir = r"D:\Thesis\CoralSeaConstrained_MC_3_Gen_15_RS_30_80FACM_20SVSCM\2021-07-16-114710"
gens, gen_order = [], []
for root, dirs, files in sorted(os.walk(root_dir)):
    for file in files:
        if file.endswith(".pkl"):
            gen_number = int(file.strip("Generation_").strip("_Results.pkl"))
            gen = pickle.load(open(os.path.join(root_dir, file), "rb"))
            seeds = set(gen["results"].keys())
            gen_order.append(gen_number)
            gens.append(gen["results"])

gens = [x for _, x in sorted(zip(gen_order, gens), key=lambda pair: pair[0])]

all_data_organized = {}
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
        np.mean((vsm_ships_all_gen[i], vsm_aircraft_all_gen[i], vscm_ships_all_gen[i], vscm_aircraft_all_gen[i])) for i
        in
        range(len(vsm_ships_all_gen))]
    gen_1_red = [
        np.mean((fam_ships_all_gen[i], fam_aircraft_all_gen[i], facm_ships_all_gen[i], facm_aircraft_all_gen[i]))
        for i in range(len(vsm_ships_all_gen))]
    scores = [gen[i]['score_mean'] for i in gen]
    all_data_organized[idx] = {"blue":vscm_blue_all_gen ,
                               "red": facm_red_all_gen,
                               "score_mean": scores}

NUM_COLORS = len(gens)

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
    box_plot_data.append(all_data_organized[gen]["score_mean"])
axs[1].boxplot(box_plot_data)

axs[1].legend()
fig, axs = plt.subplots(2)
axs[0].set_prop_cycle(color=[scalarMap.to_rgba(i) for i in range(NUM_COLORS)])
x, y = [], []
for idx, gen in enumerate(all_data_organized):
    max_value_generation = np.mean(all_data_organized[gen]["score_mean"])
    axs[0].scatter(idx, max_value_generation, label=str(gen))
    x.append(idx)
    y.append(max_value_generation)

z = np.polyfit(x, y, 1)
p = np.poly1d(z)
axs[0].plot(x, list(p(x)),linestyle=':', label="trendline")
axs[0].legend()

axs[1].set_prop_cycle(color=[scalarMap.to_rgba(i) for i in range(NUM_COLORS)])
for gen in all_data_organized:
    gen_avg_blue = np.mean(all_data_organized[gen]["blue"])
    gen_avg_red = np.mean(all_data_organized[gen]["red"])
    axs[1].scatter(gen_avg_blue,
                   gen_avg_red, label=str(gen))
axs[1].set_xlabel("Blue Survivability (%)")
# plt.xlim([0, 100])
axs[1].set_ylabel("Red Attrition (%)")
# plt.ylim([0, 100])
axs[1].legend()

