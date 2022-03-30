from interp.general_table import GeneralTable
import numpy as np
import matplotlib.pyplot as plt


def get_fluid_prop(prop_name: str):
    temp = 300
    file_name = "tables/thermophys_props_sat_water.csv"

    table = GeneralTable(file_name)
    return table.interpolate_specific_prop("temp", temp, prop_name)


def reynolds(u_m):
    nu = get_fluid_prop("vf") * get_fluid_prop("mu_f")
    D = 0.25
    return u_m * D / nu


def friction_factor(u_m):
    Re = reynolds(u_m)
    return (0.79*np.log(Re)-1.64)**(-2)


def pressure_drop(u_m):
    f = friction_factor(u_m)
    vf = get_fluid_prop("vf")
    D = 0.25
    dx = 1000
    return f*u_m**2 / (2*vf*D) * dx


def power(u_m):
    dp = pressure_drop(u_m)
    D = 0.25
    return dp * np.pi/4 * D**2 * u_m


def plot_graphs():
    _, (ax1, ax2) = plt.subplots(1, 2)
    velocity = np.linspace(0.05, 1.5, 501)
    ax1.plot(velocity, pressure_drop(velocity)/1000)
    ax1.grid()
    ax1.set_xlabel("Velocity (m/s)")
    ax1.set_ylabel("Pressure drop (kPa)")
    ax1.set_title("Pressure drop in pipe")

    ax2.plot(velocity, power(velocity)/1000)
    ax2.grid()
    ax2.set_xlabel("Velocity (m/s)")
    ax2.set_ylabel("Power requirement (kW)")
    ax2.set_title("Pump power requirement")

    plt.show()
