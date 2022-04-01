import numpy as np
import matplotlib.pyplot as plt

def temp_mean(x, constants):
    (D, L, q0_flux, m, cp, Tm_i, h) = constants
    P = np.pi*D
    return -q0_flux*L*P/(np.pi*m*cp) * np.cos(np.pi*x/L) + Tm_i


def temp_surface(x, constants):
    (D, L, q0_flux, m, cp, Tm_i, h) = constants
    Ts = q0_flux/h * np.sin(np.pi*x/L)
    Ts += temp_mean(x, constants)
    return Ts


def plot_graphs():
    D = 0.04  # m
    L = 4  # m
    q0_flux = 10e4  # W/m2
    m = 0.025  # kg/s
    cp = 4180  # J/kgK
    Tm_i = 2 + 273  # K
    h = 10e3  # W/m2K
    constants = [D, L, q0_flux, m, cp, Tm_i, h]

    x = np.linspace(0, L, 401)
    Tm = temp_mean(x, constants)
    Ts = temp_surface(x, constants)
    _, (ax) = plt.subplots(1, 1)
    ax.plot(x, Tm, label="Mean temperature")
    ax.plot(x, Ts, label="Surface temperature")

    ax.grid()
    ax.legend()
    ax.set_xlabel("x (m)")
    ax.set_ylabel("T (K)")
    plt.show()


