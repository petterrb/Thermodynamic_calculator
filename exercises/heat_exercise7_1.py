import numpy as np
import matplotlib.pyplot as plt
import enum

FREE_STREAM_VEL = 2  # m/s

class Fluid(enum.Enum):
    AIR = 0
    ENGINE_OIL = 1

DYN_VISC = {Fluid.AIR: 15.89*10**(-6), Fluid.ENGINE_OIL: 16.90*10**(-6)}
PRANDTL_NUMBER = {Fluid.AIR: 0.707, Fluid.ENGINE_OIL: 233}

def reynolds(x, fluid):
    return FREE_STREAM_VEL * x / DYN_VISC[fluid]


def vel_boundary_layer(x, fluid):
    Re = reynolds(x, fluid)
    return 5*x / np.sqrt(Re)

def thermal_boundary_layer(x, fluid):
    return vel_boundary_layer(x, fluid) * PRANDTL_NUMBER[fluid]**(-1/3)

def nusselt_number(x, fluid):
    Re = reynolds(x, fluid)
    Pr = PRANDTL_NUMBER[fluid]
    return 0.332 * Re**0.5 * Pr**(1/3)


def plot_bound(bound_type="velocity"):
    x_c_air = 3.97
    x_c_oil = 4.23
    n_points = 501
    x_air = np.linspace(0, x_c_air, n_points)
    x_oil = np.linspace(0, x_c_oil, n_points)
    x = {Fluid.AIR: x_air, Fluid.ENGINE_OIL: x_oil}
    label = {Fluid.AIR: "air", Fluid.ENGINE_OIL: "engine oil"}

    _, (ax) = plt.subplots(1, 1)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.grid()

    if bound_type == "velocity":
        for fluid in Fluid:
            ax.plot(x[fluid], vel_boundary_layer(x[fluid], fluid), label=label[fluid])
            ax.set_title("Velocity boundary layer for air and engine oil")
    elif bound_type == "thermal":
        for fluid in Fluid:
            ax.plot(x[fluid], thermal_boundary_layer(x[fluid], fluid), label=label[fluid])
            ax.set_title("Thermal boundary layer for air and engine oil")

    elif bound_type == "nusselt":
        for fluid in Fluid:
            ax.plot(x[fluid], nusselt_number(x[fluid], fluid), label=label[fluid])
            ax.set_title("Nusselt number for air and engine oil")
            ax.set_ylabel("Nu")


    ax.legend()
    plt.show()
