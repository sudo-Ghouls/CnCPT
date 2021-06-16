import json
import tkinter
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog

import cartopy.crs as ccrs
import cartopy.io.shapereader as shapereader
import matplotlib.animation
import matplotlib.pyplot as plt

# output =  r"C:\Users\Thomas Goolsby\iCloudDrive\Documents\MIT\System Design & Management\Thesis_Working_Area\CnCPT\Output\CoralSea\Baseline\2021-04-04-223114\0\animation.gif"
# formatted_unit_data_path = r"C:\Users\Thomas Goolsby\iCloudDrive\Documents\MIT\System Design & Management\Thesis_Working_Area\CnCPT\Output\CoralSea\Baseline\2021-04-04-223114\0\formatted_unit_data.log"
# unit_data_file_path = r"C:\Users\Thomas Goolsby\iCloudDrive\Documents\MIT\System Design & Management\Thesis_Working_Area\CnCPT\Output\CoralSea\Baseline\2021-04-04-223114\0\unit_data.log"

root = Tk()
root.withdraw()
folder_selected = filedialog.askdirectory()

output = folder_selected + "/animation.gif"
formatted_unit_data_path = folder_selected + "/formatted_unit_data.log"
with open(formatted_unit_data_path) as json_data:
    data = json.load(json_data)
    unit_data = data["UnitData"]
    map_bounds = data["MapBounds"]
unit_data_file_path = folder_selected + "/unit_data.log"
with open(unit_data_file_path) as json_data:
    raw_unit_data = json.load(json_data)['data'][0:-1]

unit_names, unit_sides, unit_types = [], {}, {}
for unit in raw_unit_data:
    unit_names.append(unit['name'])
    unit_sides[unit['name']] = (unit['side'])
    unit_types[unit['name']] = (unit['type'])
unit_names = set(unit_names)
unit_side_color_map = {'RED': 'red',
                       'BLUE': 'blue',
                       'GREEN': 'green'}
unit_colors = [unit_side_color_map[unit_sides[name]] for name in unit_names]
for idx, name in enumerate(unit_names):
    if unit_colors[idx] == 'red':
        if "DiveBomber" in unit_types[name]:
            unit_colors[idx] = 'firebrick'
        if "Fighter" in unit_types[name]:
            unit_colors[idx] = 'darksalmon'
        if "TorpedoBomber" in unit_types[name]:
            unit_colors[idx] = 'mediumvioletred'
    elif unit_colors[idx] == 'blue':
        if "DiveBomber" in unit_types[name]:
            unit_colors[idx] = 'royalblue'
        if "Fighter" in unit_types[name]:
            unit_colors[idx] = 'deepskyblue'
        if "TorpedoBomber" in unit_types[name]:
            unit_colors[idx] = 'navy'
    else:
        pass

shpfilename = shapereader.natural_earth(resolution='110m',
                                        category='cultural',
                                        name='admin_0_countries')
reader = shapereader.Reader(shpfilename)

fig = plt.figure(figsize=(19.2, 10.8))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([map_bounds[1], map_bounds[3], map_bounds[0], map_bounds[2]], crs=ccrs.PlateCarree())
ax.stock_img()
ax.coastlines()

x, y = [], []
map_fig = ax.scatter(x, y)
plt.ylim([map_bounds[0], map_bounds[2]])
plt.xlim([map_bounds[1], map_bounds[3]])
unit_lines = {}

plotlays, plotcols = [len(unit_names)], unit_colors
for idx, name in enumerate(unit_names):
    lobj = ax.plot([], [], lw=2, color=plotcols[idx])[0]
    unit_lines[name] = {"lineObj": lobj,
                        "x_data": [],
                        "y_data": []}


def init_function():
    unit_lines = {}
    plotlays, plotcols = [len(unit_names)], unit_colors
    for idx, name in enumerate(unit_names):
        lobj = ax.plot([], [], lw=2, color=plotcols[idx])[0]
        unit_lines[name] = {"lineObj": lobj,
                            "x_data": [],
                            "y_data": []}
    for name in unit_lines:
        unit_lines[name]["lineObj"].set_data(unit_lines[name]["x_data"], unit_lines[name]["y_data"])
    return [unit_lines[unit]['lineObj'] for unit in unit_lines.keys()]


def animate(idx):
    time = list(unit_data.keys())[idx]
    for unit in unit_data[time]:
        if unit_data[time][unit]['alive']:
            new_x = unit_data[time][unit]['location_y']
            new_y = unit_data[time][unit]['location_x']
            unit_lines[unit]["x_data"].append(new_x)
            unit_lines[unit]["y_data"].append(new_y)
            unit_lines[unit]["x_data"] = unit_lines[unit]["x_data"][-10:]
            unit_lines[unit]["y_data"] = unit_lines[unit]["y_data"][-10:]
            unit_lines[unit]["lineObj"].set_data(unit_lines[unit]["x_data"], unit_lines[unit]["y_data"])
        else:
            new_x = unit_data[time][unit]['location_y']
            new_y = unit_data[time][unit]['location_x']
            unit_lines[unit]["x_data"] = [new_x]
            unit_lines[unit]["y_data"] = [new_y]
            new_lobj = ax.plot(new_x, new_y, lw=5, color="k", marker='X')[0]
            unit_lines[unit]["lineObj"] = new_lobj

    if idx == len(unit_data.keys()) - 1:
        for idx, name in enumerate(unit_names):
            unit_lines[name]["x_data"] = []
            unit_lines[name]["y_data"] = []
        # restart()
    return [unit_lines[unit]['lineObj'] for unit in unit_lines.keys()]


ani = matplotlib.animation.FuncAnimation(fig, animate, init_func=init_function, frames=len(unit_data.keys()),
                                         interval=100, repeat=False, save_count=len(unit_data.keys()))


def restart():
    root = tkinter.Tk()
    root.withdraw()
    result = tkinter.messagebox.askyesno("Restart", "Do you want to restart animation?")
    if result:
        ani.frame_seq = ani.new_frame_seq()
        ani.event_source.start()
    else:
        plt.close()


plt.show()
# ani.save(output, progress_callback=lambda i, n: print(f'Saving frame {i} of {n}'))
