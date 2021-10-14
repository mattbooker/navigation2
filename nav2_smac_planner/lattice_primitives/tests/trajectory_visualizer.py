import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


def plot_arrow(x, y, yaw, length=1.0, fc="r", ec="k"):
    """
    Plot arrow
    """
    plt.arrow(x, y, length * np.cos(yaw), length *
              np.sin(yaw), width=0.05*length, length_includes_head=True)
    plt.plot(x, y)
    plt.plot(0, 0)


def read_trajectories_data(file_path):

    with open(file_path) as data_file:
        trajectory_data = json.load(data_file)

    return trajectory_data


cur_file_path = Path(__file__)
trajectory_file_path = cur_file_path.parent.parent / "output.json"


trajectory_data = read_trajectories_data(trajectory_file_path)
min_x = min([min([pose[0] for pose in primitive["poses"]]) for primitive in trajectory_data["primitives"]])
max_x = max([max([pose[0] for pose in primitive["poses"]]) for primitive in trajectory_data["primitives"]])

min_y = min([min([pose[1] for pose in primitive["poses"]]) for primitive in trajectory_data["primitives"]])
max_y = max([max([pose[1] for pose in primitive["poses"]]) for primitive in trajectory_data["primitives"]])

heading_angles = trajectory_data["lattice_metadata"]["heading_angles"]

for primitive in trajectory_data["primitives"]:
    arrow_length = (primitive["arc_length"] +
                    primitive["straight_length"]) / len(primitive["poses"])

    if arrow_length == 0:
        arrow_length = max_x / len(primitive["poses"])

    xs = [pose[0] for pose in primitive["poses"]]
    ys = [pose[1] for pose in primitive["poses"]]

    for x, y, yaw in primitive["poses"]:
        plot_arrow(x, y, yaw, length=arrow_length)

    plt.scatter(xs, ys)
    plt.grid(True)
    plt.axis('square')

    left_x, right_x = plt.xlim()
    left_y, right_y = plt.ylim()
    plt.xlim(1.2*min_x, 1.2*max_x)
    plt.ylim(1.2*min_y, 1.2*max_y)

    start_angle = np.rad2deg(heading_angles[primitive["start_angle_index"]])
    end_angle = np.rad2deg(heading_angles[primitive["end_angle_index"]])

    plt.title(f'Trajectory ID: {primitive["trajectory_id"]}')
    plt.figtext(
        0.7, 0.9, f'Start: {start_angle}\nEnd: {end_angle}')

    plt.show()
