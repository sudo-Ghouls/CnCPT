import os
import pickle

import cartopy
import cartopy.crs as ccrs
import cartopy.io.shapereader as shapereader
import matplotlib.pyplot as plt
import matplotlib.transforms
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn import preprocessing

# Load in all data

# path = r"D:\Thesis\CnCPT_Tests\CoralSeaCarrierCarnagePeakArch\CarrierCarnage\2021-07-27-211706"
# path = r"D:\Thesis\CnCPT_Tests\CoralSeaBombsAwayPeakArch\BombsAway\2021-07-27-211703"
# path = r"D:\Thesis\CnCPT_Tests\CoralSeaEndersGamePeakArch\EndersGame\2021-07-27-211700"
""" --------------------------------------------------------  CONFIG  -----------------------------------------------"""
drawdown = False
weapon_stats = False
heatmap = False
exchange_matrix = True
map_bounds = [-18.02904145799271,
              149.9831854228132,
              -5.001921913555804,
              164.9716046029078]
""" -----------------------------------------------------------------------------------------------------------------"""

path = r"D:\Thesis\CoralSeaBaseline\Baseline\2021-07-24-212344"
def run(path, output=None):
    if output is None:
        output = os.path.join(path, "Set_Metrics")
    else:
        output = os.path.join(output, "Set_Metrics")
    try:
        os.mkdir(output)
    except:
        pass

    set_log_path = os.path.join(path, "Simulation_Set_Log.pkl")
    try:
        set_log = pickle.load(open(set_log_path, "rb"))
    except:
        set_log = None
    shpfilename = shapereader.natural_earth(resolution='110m',
                                            category='cultural',
                                            name='admin_0_countries')
    reader = shapereader.Reader(shpfilename)

    seed_logs = []
    for root, dirs, files in sorted(os.walk(path)):
        for dir in dirs:
            seed_log_path = os.path.join(root, dir, "Simulation_Logs.pkl")
            try:
                seed_log = pickle.load(open(seed_log_path, "rb"))
            except:
                break
            seed_logs.append(seed_log)
    MC_Size = len(seed_logs)
    fig_idx = 4

    Blue_Weapon_ranges = {}
    Blue_Weapon_Shooters_indvidual = {}
    Blue_Weapon_Shooters_class = {}

    Red_Weapon_ranges = {}
    Red_Weapon_Shooters_indvidual = {}
    Red_Weapon_Shooters_class = {}

    drawdown_dataframe = pd.DataFrame()
    weapon_log_dataframe = pd.DataFrame()
    kill_log_dataframe = pd.DataFrame()

    # Collect Data from Logs
    for idx, log in enumerate(seed_logs):
        kill_log = log['kill_log']
        isr_log = log['isr_log']
        weapon_log = log['weapon_log']
        drawdown_log = log['drawdown_log']

        # Draw Down
        times, dd_b_ships, dd_b_aircraft, dd_r_ships, dd_r_aircraft = [], [], [], [], []
        for time in drawdown_log["blue_ships"].keys():
            times.append(time)
            dd_b_ships.append(len(drawdown_log["blue_ships"][time]))
            dd_b_aircraft.append(len(drawdown_log["blue_aircraft"][time]))
            dd_r_ships.append(len(drawdown_log["red_ships"][time]))
            dd_r_aircraft.append(len(drawdown_log["red_aircraft"][time]))

        w_0, w_1, w_2, w_3, w_4, w_5, w_6, w_7, = [], [], [], [], [], [], [], []
        w_8, w_9, w_10, w_11, w_12, w_13, w_14, w_15 = [], [], [], [], [], [], [], []
        for wl in weapon_log:
            shot = weapon_log[wl]
            w_0.append(wl)
            w_1.append(bool(int(shot["target_killed"])))
            w_2.append(shot["pk_diceroll"])
            w_3.append(shot["shooter_side"])
            w_4.append(shot["shooter_name"])
            w_5.append(shot["shooter_class"])
            w_6.append(shot["shooter_location_lat"])
            w_7.append(shot["shooter_location_lon"])
            w_8.append(shot["range"])
            w_9.append(shot["target_side"])
            w_10.append(shot["target_name"])
            w_11.append(shot["target_class"])
            w_12.append(shot["target_location_lat"])
            w_13.append(shot["target_location_lon"])
            if shot["shooter_class"] in ['DouglasTBDDevastator', 'DouglasSBDDauntless', 'GrummanF4F3Wildcat',
                                         'AichiD3AType99', 'NakajimaB5NType97', 'A6M2Zero']:
                w_14.append(True)
            else:
                w_14.append(False)
            if shot["target_class"] in ['DouglasTBDDevastator', 'DouglasSBDDauntless', 'GrummanF4F3Wildcat',
                                        'AichiD3AType99', 'NakajimaB5NType97', 'A6M2Zero']:
                w_15.append(True)
            else:
                w_15.append(False)

        weapon_log_dataframe_temp = pd.DataFrame.from_dict({"Shot_UUID": w_0,
                                                            "target_killed": w_1,
                                                            "pk_diceroll": w_2,
                                                            "shooter_side": w_3,
                                                            "shooter_name": w_4,
                                                            "shooter_class": w_5,
                                                            "shooter_location_lat": w_6,
                                                            "shooter_location_lon": w_7,
                                                            "range": w_8,
                                                            "target_side": w_9,
                                                            "target_name": w_10,
                                                            "target_class": w_11,
                                                            "target_location_lat": w_12,
                                                            "target_location_lon": w_13,
                                                            "shooter_is_aircraft": w_14,
                                                            "target_is_aircraft": w_15})

        times = [t / (24 * 60 * 60) for t in times]
        drawdown_dataframe_temp = pd.DataFrame.from_dict({"time": times[1:],
                                                          "blue_ships": dd_b_ships[1:],
                                                          "blue_aircraft": dd_b_aircraft[1:],
                                                          "red_ships": dd_r_ships[1:],
                                                          "red_aircraft": dd_r_aircraft[1:]})

        weapon_log_dataframe = pd.concat([weapon_log_dataframe, weapon_log_dataframe_temp])
        drawdown_dataframe = drawdown_dataframe.append(drawdown_dataframe_temp, ignore_index=True)

        # Kill Log Graphics
        # Weapon Range Distributions
        k_0, k_1, k_2, k_3, k_4, k_5, k_6, k_7, k_8, k_9, k_10, k_11 = [], [], [], [], [], [], [], [], [], [], [], []
        for kill in kill_log:
            kl = kill_log[kill]
            weapon = kl["weapon"]
            shooter_side = kl["shooter_side"]
            range_i = kl["range_m"]

            k_0.append(kl["target"])
            k_1.append(kl["target_side"])
            k_2.append(kl["target_class"])
            k_3.append(kl["target_type"])
            k_4.append(kl["weapon"])
            k_5.append(kl["shooter"])
            k_6.append(kl["shooter_side"])
            k_7.append(kl["shooter_class"])
            k_8.append(kl["shooter_type"])
            k_9.append(kl["time_sec"])
            k_10.append(kl["shooter_side"])
            k_11.append(kl["range_m"])

            if shooter_side == "BLUE":
                Blue_Weapon_ranges.setdefault(weapon, []).append(range_i)
            else:
                Red_Weapon_ranges.setdefault(weapon, []).append(range_i)

        kill_log_dataframe_temp = pd.DataFrame.from_dict({"target": k_0,
                                                          "target_side": k_1,
                                                          "target_class": k_2,
                                                          "target_type": k_3,
                                                          "weapon": k_4,
                                                          "shooter": k_5,
                                                          "shooter_side": k_6,
                                                          "shooter_class": k_7,
                                                          "shooter_type": k_8,
                                                          "time_sec": k_9,
                                                          "shooter_Side": k_10,
                                                          "range_m": k_11})
        kill_log_dataframe = pd.concat([kill_log_dataframe, kill_log_dataframe_temp])

    # DrawDown Plotting
    if drawdown:
        x = drawdown_dataframe.values  # returns a numpy array
        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(x)
        drawdown_dataframe_norm = pd.DataFrame(x_scaled, columns=["time_norm",
                                                                  "blue_ships_norm",
                                                                  "blue_aircraft_norm",
                                                                  "red_ships_norm",
                                                                  "red_aircraft_norm"])
        drawdown_dataframe = pd.concat([drawdown_dataframe, drawdown_dataframe_norm], axis=1)

        plt.figure(0)
        sns.lineplot(data=drawdown_dataframe, x='time', y='blue_ships', color="blue")
        sns.lineplot(data=drawdown_dataframe, x='time', y='red_ships', color="red")
        plt.tight_layout()
        plt.ylim([15,36])
        plt.xlabel("Time (Days)")
        plt.ylabel("Surface Force Structure Drawdown")
        filename = os.path.join(output, "Ship_DrawDown_Plot_abs.png")
        plt.savefig(filename)
        plt.close()
        plt.figure(1)
        sns.lineplot(data=drawdown_dataframe, x='time', y='blue_ships_norm', color="blue")
        sns.lineplot(data=drawdown_dataframe, x='time', y='red_ships_norm', color="red")
        plt.tight_layout()
        plt.ylim([0,1])
        plt.xlabel("Time (Days)")
        plt.ylabel("Surface Force Structure Drawdown (Normalized)")
        filename = os.path.join(output, "Ship_DrawDown_Plot_norm.png")
        plt.savefig(filename)
        plt.close()

        plt.figure(2)
        sns.lineplot(data=drawdown_dataframe, x='time', y='blue_aircraft', color="blue")
        sns.lineplot(data=drawdown_dataframe, x='time', y='red_aircraft', color="red")
        plt.tight_layout()
        plt.xlabel("Time (Days)")
        plt.ylabel("Aerial Force Structure Drawdown")
        filename = os.path.join(output, "Aircraft_DrawDown_Plot_abs.png")
        plt.savefig(filename)
        plt.close()
        plt.figure(3)
        sns.lineplot(data=drawdown_dataframe, x='time', y='blue_aircraft_norm', color="blue")
        sns.lineplot(data=drawdown_dataframe, x='time', y='red_aircraft_norm', color="red")
        plt.tight_layout()
        plt.xlabel("Time (Days)")
        plt.ylabel("Aerial Force Structure Drawdown (Normalized)")
        filename = os.path.join(output, "Aircraft_DrawDown_Plot_norm.png")
        plt.savefig(filename)
        plt.close()

    if weapon_stats:
        blue_ranges_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in Blue_Weapon_ranges.items()]))
        for col in blue_ranges_df.columns:
            plt.figure(fig_idx)
            ax = sns.histplot(data=blue_ranges_df, x=col, color='blue', binwidth=500)
            ax.set_xlim(0, 15000)
            ax.set_ylim(0, 65)
            ax.set_xlabel(" Engagement Range (m)", fontsize=18)
            ax.set_ylabel("Count", fontsize=18)
            filename = os.path.join(output, "US_{0}_histogram.png".format(col))
            plt.tight_layout()
            plt.savefig(filename)
            plt.close()
            fig_idx += 1

        red_ranges_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in Red_Weapon_ranges.items()]))
        for col in red_ranges_df.columns:
            plt.figure(fig_idx)
            ax = sns.histplot(data=red_ranges_df, x=col, color='red', binwidth=500)
            ax.set_xlim(0, 15000)
            ax.set_ylim(0, 65)
            ax.set_xlabel(" Engagement Range (m)", fontsize=18)
            ax.set_ylabel("Count", fontsize=18)
            filename = os.path.join(output, "JAPAN_{0}_histogram.png".format(col))
            plt.tight_layout()
            plt.savefig(filename)
            plt.close()
            fig_idx += 1

    if heatmap:
        weapon_log_dataframe['Shot_UUID_Numeric'] = list(range(len(weapon_log_dataframe.index)))
        weapon_log_dataframe.set_index(["Shot_UUID_Numeric"])

        red_weapons = weapon_log_dataframe[weapon_log_dataframe['shooter_side'] == "RED"]
        red_weapons_sea = red_weapons[red_weapons['shooter_is_aircraft'] == 0]
        red_weapons_air = red_weapons[red_weapons['shooter_is_aircraft'] == 1]

        blue_weapons = weapon_log_dataframe[weapon_log_dataframe['shooter_side'] == "BLUE"]
        blue_weapons_sea = blue_weapons[blue_weapons['shooter_is_aircraft'] == 0]
        blue_weapons_air = blue_weapons[blue_weapons['shooter_is_aircraft'] == 1]

        # Surface Shotmap
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(19.2, 10.8), constrained_layout=True,
                                       subplot_kw={'projection': ccrs.PlateCarree()})
        ax1.set_title("Japanese Surface Force", fontsize=18)
        ax1.set_extent([map_bounds[1], map_bounds[3], map_bounds[0], map_bounds[2]], crs=ccrs.PlateCarree())
        ax1.add_feature(cartopy.feature.OCEAN, zorder=0)
        ax1.add_feature(cartopy.feature.LAND, zorder=0, edgecolor='black')
        _ = sns.kdeplot(red_weapons_sea["shooter_location_lon"], red_weapons_sea["shooter_location_lat"], cmap="Reds",
                        shade=True, alpha=.7, transform=ccrs.PlateCarree(), ax=ax1)

        ax2.set_title("US Surface Force", fontsize=18)
        ax2.set_extent([map_bounds[1], map_bounds[3], map_bounds[0], map_bounds[2]], crs=ccrs.PlateCarree())
        ax2.add_feature(cartopy.feature.OCEAN, zorder=0)
        ax2.add_feature(cartopy.feature.LAND, zorder=0, edgecolor='black')
        _ = sns.kdeplot(blue_weapons_sea["shooter_location_lon"], blue_weapons_sea["shooter_location_lat"],
                        cmap="Blues",
                        shade=True, alpha=.7, transform=ccrs.PlateCarree(), ax=ax2)
        filename = os.path.join(output, "Surface_Shot_Heatmap.png")
        plt.savefig(filename, bbox_inches="tight", pad_inches=0.1)
        plt.close()

        # Aircraft Shotmap
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(19.2, 10.8), constrained_layout=True,
                                       subplot_kw={'projection': ccrs.PlateCarree()})
        ax1.set_title("Japanese Aircraft", fontsize=18)
        ax1.set_extent([map_bounds[1], map_bounds[3], map_bounds[0], map_bounds[2]], crs=ccrs.PlateCarree())
        ax1.add_feature(cartopy.feature.OCEAN, zorder=0)
        ax1.add_feature(cartopy.feature.LAND, zorder=0, edgecolor='black')
        _ = sns.kdeplot(red_weapons_air["shooter_location_lon"], red_weapons_air["shooter_location_lat"], cmap="Reds",
                        shade=True, alpha=.7, transform=ccrs.PlateCarree(), ax=ax1)

        ax2.set_title("US Aircraft", fontsize=18)
        ax2.set_extent([map_bounds[1], map_bounds[3], map_bounds[0], map_bounds[2]], crs=ccrs.PlateCarree())
        ax2.add_feature(cartopy.feature.OCEAN, zorder=0)
        ax2.add_feature(cartopy.feature.LAND, zorder=0, edgecolor='black')
        _ = sns.kdeplot(blue_weapons_air["shooter_location_lon"], blue_weapons_air["shooter_location_lat"],
                        cmap="Blues",
                        shade=True, alpha=.7, transform=ccrs.PlateCarree(), ax=ax2)
        filename = os.path.join(output, "Arial_Shot_Heatmap.png")
        plt.savefig(filename, bbox_inches="tight", pad_inches=0.1)
        plt.close()

        # All Shots Shotmap
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(19.2, 10.8), constrained_layout=True,
                                       subplot_kw={'projection': ccrs.PlateCarree()})
        ax1.set_title("Japanese Force", fontsize=18)
        ax1.set_extent([map_bounds[1], map_bounds[3], map_bounds[0], map_bounds[2]], crs=ccrs.PlateCarree())
        ax1.add_feature(cartopy.feature.OCEAN, zorder=0)
        ax1.add_feature(cartopy.feature.LAND, zorder=0, edgecolor='black')
        _ = sns.kdeplot(red_weapons["shooter_location_lon"], red_weapons["shooter_location_lat"], cmap="Reds",
                        shade=True, alpha=.7, transform=ccrs.PlateCarree(), ax=ax1)

        ax2.set_title("US Force", fontsize=18)
        ax2.set_extent([map_bounds[1], map_bounds[3], map_bounds[0], map_bounds[2]], crs=ccrs.PlateCarree())
        ax2.add_feature(cartopy.feature.OCEAN, zorder=0)
        ax2.add_feature(cartopy.feature.LAND, zorder=0, edgecolor='black')
        _ = sns.kdeplot(blue_weapons["shooter_location_lon"], blue_weapons["shooter_location_lat"],
                        cmap="Blues",
                        shade=True, alpha=.7, transform=ccrs.PlateCarree(), ax=ax2)
        filename = os.path.join(output, "Shot_Heatmap.png")
        plt.savefig(filename, bbox_inches="tight", pad_inches=0.1)
        plt.close()

    if exchange_matrix:
        red_shooter_kl = kill_log_dataframe[kill_log_dataframe["shooter_side"] == "RED"]
        blue_shooter_kl = kill_log_dataframe[kill_log_dataframe["shooter_side"] == "BLUE"]

        unique_red_shooters = set(red_shooter_kl["shooter_type"])
        unique_red_targets = set(red_shooter_kl["target_type"])

        unique_blue_shooters = set(blue_shooter_kl["shooter_type"])
        unique_blue_targets = set(blue_shooter_kl["target_type"])

        red_table_df = pd.DataFrame(columns=unique_red_targets, index=unique_red_shooters)
        for shooter in unique_red_shooters:
            temp_shoot = red_shooter_kl[red_shooter_kl["shooter_type"] == shooter]
            for target in unique_red_targets:
                temp_tar = temp_shoot[temp_shoot["target_type"] == target]
                if len(temp_tar.index) == 0:
                    red_table_df[target][shooter] = 0
                else:
                    red_table_df[target][shooter] = len(temp_tar.index) / MC_Size
        for target in unique_red_targets:
            red_table_df.style.bar(subset=[target], vmin=0, vmax=sum(red_table_df[target]))

        plt.figure()
        ax = plt.subplot(111, frame_on=True)  # no visible frame
        ax.axis('off')
        values = red_table_df.values.astype('|U5')
        values = np.where(values == '0', '', values)
        row_text = ['$\\bf{0}$'.format(val) for val in red_table_df.index.values]
        col_text = ['$\\bf{0}$'.format(val) for val in red_table_df.columns]
        the_table = plt.table(fontsize=24,
                              cellText=values,
                              colLabels=col_text,
                              rowLabels=row_text,
                              rowColours=["lightcoral"] * len(red_table_df.index),
                              rowLoc='center',
                              colColours=["lightblue"] * len(red_table_df.columns),
                              colLoc='center',
                              loc="center")
        the_table.auto_set_column_width(col=list(range(len(col_text))))  # Provide integer list of columns to adjust
        the_table.auto_set_font_size(False)
        the_table.set_fontsize(10)
        plt.gcf().canvas.draw()
        points = the_table.get_window_extent(plt.gcf()._cachedRenderer).get_points()
        nbbox = matplotlib.transforms.Bbox.from_extents(points / plt.gcf().dpi)
        filename = os.path.join(output, "Japan_vs_US_Exchange_Matrix.png")
        plt.savefig(filename, dpi=500, bbox_inches=nbbox, pad_inches=0.3)
        plt.close()

        filename = os.path.join(output, "Japan_vs_US_Exchange_Matrix.html")
        # html = blue_table_df.to_html()
        df_styled = red_table_df.style.format('{:,.5f}').set_properties(**{
            'font': 'Arial', 'color': 'black', 'text-align': 'center'})
        df_styled.set_table_attributes('border="1"')
        text_file = open(filename, "w")
        text_file.write(df_styled.render())
        text_file.close()

        blue_table_df = pd.DataFrame(columns=unique_blue_targets, index=unique_blue_shooters)
        for shooter in unique_blue_shooters:
            temp_shoot = blue_shooter_kl[blue_shooter_kl["shooter_type"] == shooter]
            for target in unique_blue_targets:
                temp_tar = temp_shoot[temp_shoot["target_type"] == target]
                if len(temp_tar.index) == 0:
                    blue_table_df[target][shooter] = 0
                else:
                    blue_table_df[target][shooter] = len(temp_tar.index) / MC_Size
        for target in unique_blue_targets:
            blue_table_df.style.bar(subset=[target], vmin=0, vmax=sum(blue_table_df[target]))

        plt.figure()
        ax = plt.subplot(111, frame_on=True)  # no visible frame
        ax.axis('off')
        values = blue_table_df.values.astype('|U5')
        values = np.where(values == '0', '', values)
        row_text = ['$\\bf{0}$'.format(val) for val in blue_table_df.index.values]
        col_text = ['$\\bf{0}$'.format(val) for val in blue_table_df.columns]
        the_table = plt.table(fontsize=40,
                              cellText=values,
                              colLabels=col_text,
                              rowLabels=row_text,
                              rowColours=["lightblue"] * len(blue_table_df.index),
                              rowLoc='center',
                              colColours=["lightcoral"] * len(blue_table_df.columns),
                              colLoc='center',
                              loc="center")
        the_table.auto_set_column_width(col=list(range(len(col_text))))  # Provide integer list of columns to adjust
        the_table.auto_set_font_size(False)
        the_table.set_fontsize(10)
        plt.gcf().canvas.draw()
        points = the_table.get_window_extent(plt.gcf()._cachedRenderer).get_points()
        nbbox = matplotlib.transforms.Bbox.from_extents(points / plt.gcf().dpi)
        filename = os.path.join(output, "US_vs_Japan_Exchange_Matrix.png")
        plt.savefig(filename, dpi=500, bbox_inches=nbbox, pad_inches=0.3)
        plt.close()

        filename = os.path.join(output, "US_vs_Japan_Exchange_Matrix.html")
        # html = blue_table_df.to_html()
        df_styled = blue_table_df.style.format('{:,.5f}').set_properties(**{
            'font': 'Arial', 'color': 'black', 'text-align': 'center'})
        df_styled.set_table_attributes('border="1"')
        text_file = open(filename, "w")
        text_file.write(df_styled.render())
        text_file.close()


if __name__ == "__main__":
    run(path)
