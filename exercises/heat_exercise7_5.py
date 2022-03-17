import numpy as np
import matplotlib.pyplot as plt

LENGTH = 0.15
TEMP_SURFACE = 250 + 273
TEMP_INF = 27 + 273
PRANDTL = 0.68908
DYN_VISC = 27.7854 * 10**(-6)
CONDUCTIVITY = 42.172 * 10**(-3)


def reynolds(x, velocity):
    return velocity*x/DYN_VISC

def nusselt(x, velocity):
    return 0.0296 * reynolds(x, velocity)**(4/5)*PRANDTL**(1/3)

def avg_nusselt(velocity=80/3.6):
    return 2* 5/9 * nusselt(LENGTH, velocity)

def heat_transfer(velocity):
    return avg_nusselt(velocity)*CONDUCTIVITY*(TEMP_SURFACE - TEMP_INF)

def plot_heat_transfer():
    vel_min, vel_max = 10/3.6, 100/3.6
    n_points = 501
    velocity = np.linspace(vel_min, vel_max, n_points)
    q = heat_transfer(velocity)

    _, (ax) = plt.subplots(1, 1)
    ax.plot(velocity*3.6, q)
    ax.set_xlabel("Velocity (km/h)")
    ax.set_ylabel("Heat transfer (W/m)")
    ax.set_title("Heat transfer per unit width, motorcycle fin")
    ax.grid()


    plt.show()