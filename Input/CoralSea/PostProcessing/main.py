import os
import pickle

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Load in all data
path = r"D:\Thesis\CoralSeaBaseline\Baseline\2021-07-24-123648"
set_log_path = os.path.join(path, "Simulation_Set_Log.pkl")
try:
    set_log = pickle.load(open(set_log_path, "rb"))
except:
    set_log = None

seed_logs = []
for root, dirs, files in sorted(os.walk(path)):
    for dir in dirs:
        seed_log_path = os.path.join(root, dir, "Simulation_Logs.pkl")
        try:
            seed_log = pickle.load(open(seed_log_path, "rb"))
        except:
            break
        seed_logs.append(seed_log)
fig_idx = 1

Blue_Weapon_ranges = {}
Blue_Weapon_Shooters_indvidual = {}
Blue_Weapon_Shooters_class = {}

Red_Weapon_ranges = {}
Red_Weapon_Shooters_indvidual = {}
Red_Weapon_Shooters_class = {}

for idx, log in enumerate(seed_logs):
    kill_log = log['kill_log']
    isr_log = log['isr_log']
    weapon_log = log['weapon_log']
    drawdown_log = log['drawdown_log']


    # Kill Log Graphics

    # Weapon Range Distributions
    for kill in kill_log:
        kl = kill_log[kill]
        target_side = kl["Target_Side"]
        time_sec = kl["Time_sec"]
        weapon = kl["Weapon"]
        shooter = kl["Shooter"]
        shooter_class = kl["Shooter_Class"]
        shooter_side = kl["Shooter_Side"]
        range = kl["Range_m"]

        if shooter_side == "BLUE":
            Blue_Weapon_ranges.setdefault(weapon, []).append(range)
            Blue_Weapon_Shooters_indvidual.setdefault(shooter, []).append(1)
            Blue_Weapon_Shooters_class.setdefault(shooter_class, []).append(1)
        else:
            Red_Weapon_ranges.setdefault(weapon, []).append(range)
            Red_Weapon_Shooters_indvidual.setdefault(shooter, []).append(1)
            Red_Weapon_Shooters_class.setdefault(shooter_class, []).append(1)

for key in Blue_Weapon_Shooters_indvidual:
    Blue_Weapon_Shooters_indvidual[key] = sum(Blue_Weapon_Shooters_indvidual[key]) / (len(seed_logs) + 1)
for key in Blue_Weapon_Shooters_class:
    Blue_Weapon_Shooters_class[key] = sum(Blue_Weapon_Shooters_class[key]) / (len(seed_logs) + 1)
for key in Red_Weapon_Shooters_indvidual:
    Red_Weapon_Shooters_indvidual[key] = sum(Red_Weapon_Shooters_indvidual[key]) / (len(seed_logs) + 1)
for key in Red_Weapon_Shooters_class:
    Red_Weapon_Shooters_class[key] = sum(Red_Weapon_Shooters_class[key]) / (len(seed_logs) + 1)

blue_ranges_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in Blue_Weapon_ranges.items()]))
for col in blue_ranges_df.columns:
    plt.figure(fig_idx)
    ax = sns.histplot(data=blue_ranges_df, x=col, color='blue', binwidth=500)
    ax.set_xlim(0, 15000)
    fig_idx += 1
#
# pd.DataFrame.from_dict(Blue_Weapon_ranges)
# pd.DataFrame.from_dict(Blue_Weapon_ranges)

red_ranges_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in Red_Weapon_ranges.items()]))
for col in red_ranges_df.columns:
    plt.figure(fig_idx)
    ax = sns.histplot(data=red_ranges_df, x=col, color='red', binwidth=500)
    ax.set_xlim(0, 15000)
    fig_idx += 1

plt.show()
a = 1
# pd.DataFrame.from_dict(Blue_Weapon_ranges)
# pd.DataFrame.from_dict(Blue_Weapon_ranges)
# pd.DataFrame.from_dict(Blue_Weapon_ranges)
