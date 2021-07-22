import os
import pickle

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

root_dir = r"D:\Thesis\CoralSeaConstrained\2021-07-01-113325"
gens = []
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".pkl"):
            gen = pickle.load(open(os.path.join(root_dir, file), "rb"))
            gens.append(gen)

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
plt.show()
a = 1
