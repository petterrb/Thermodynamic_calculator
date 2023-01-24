import numpy as np
import matplotlib.pyplot as plt
from interp.general_table import GeneralTable
from interp.ui import InterpMenu

def get_property_axes(table: GeneralTable, x_prop, y_props) -> plt.Axes:
    plt.rcParams.update({'font.size': 12})

    _, (ax) = plt.subplots(1, 1)
    x = table.get_all_values(x_prop)
    for prop in y_props:
        y = table.get_all_values(prop)
        ax.plot(x, y, label=prop)

    return ax

def plot_property(ax: plt.Axes, xlabel: str, ylabel: str) -> None:
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid()
    ax.legend()
    plt.show()


def main():
    menu = InterpMenu()
    table = menu.get_table("2")
    prop_x = "temp"
    prop_y1 = "vf"
    prop_y2 = "vg"

    ax = get_property_axes(table, prop_x, [prop_y1, prop_y2])
    plot_property(ax, "Temperature (Celsius)", "sf and sg")
