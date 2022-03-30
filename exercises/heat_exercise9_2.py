from interp.general_table import GeneralTable
import numpy as np
import matplotlib.pyplot as plt


def get_fluid_prop(fluid_name: str, prop_name: str):
    temp = 308
    file_dict = {
        "air": "tables/thermophys_props_air_atm_press.csv",
        "water": "tables/thermophys_props_sat_water.csv",
        "oil": "tables/thermophys_props_engine_oil_atm_press.csv"
    }
    table = GeneralTable(file_dict[fluid_name])
    return table.interpolate_specific_prop("temp", temp, prop_name)


def reynolds(v, fluid_name: str):
    if fluid_name == "air" or fluid_name == "oil":
        nu = get_fluid_prop(fluid_name, "nu")
    else:
        nu = get_fluid_prop(fluid_name, "vf") * get_fluid_prop(fluid_name, "mu_f")
    D = 0.01
    return v * D / nu


def nusselt(v, fluid_name: str):
    Re = reynolds(v, fluid_name)
    pr_str = "Pr_f" if fluid_name == "water" else "Pr"
    Pr = get_fluid_prop(fluid_name, pr_str)
    Nu = 0.62 * Re ** 0.5 * Pr ** (1 / 3) / (1 + (0.4 / Pr) ** (2 / 3)) ** 0.25
    Nu *= (1 + (Re / 282000) ** (5 / 8)) ** (4 / 5)
    Nu += 0.3

    return Nu


def heat_rate(v, fluid_name: str):
    k_str = "kf" if fluid_name == "water" else "k"
    k = get_fluid_prop(fluid_name, k_str)
    Nu = nusselt(v, fluid_name)
    temp_diff = 30
    return np.pi * Nu * k * temp_diff


def plot_heat():
    fluid_names = ["air", "water", "oil"]
    _, (ax) = plt.subplots(1, 1)
    velocity = np.linspace(0.5, 10, 501)
    for fluid in fluid_names:
        ax.plot(velocity, heat_rate(velocity, fluid)/1000, label=fluid)

    ax.grid()
    ax.set_xlabel("Velocity (m/s)")
    ax.set_ylabel("q' (kW/m)")
    ax.legend()
    plt.show()
