import numpy as np
import matplotlib.pyplot as plt
import enum


class Fluid(enum.Enum):
    AIR = 0
    WATER = 1
    ENGINE_OIL = 2
    MERCURY = 3

PRANDTL_NUMBER = {Fluid.AIR: 0.707, Fluid.WATER: 5.83, Fluid.ENGINE_OIL: 6400, Fluid.MERCURY: 0.0248}
DYN_VISC = {
    Fluid.AIR: 15.89 * 10**(-6),
    Fluid.WATER: 1.003 * 10**(-3) * 855 * 10**(-6),
    Fluid.ENGINE_OIL: 550 * 10**(-6),
    Fluid.MERCURY: 0.1125 * 10**(-6)
}


VELOCITY = 1

def vel_boundary_layer(x, fluid: Fluid):
    reynolds = VELOCITY*x/DYN_VISC[fluid]
    return 5*x/np.sqrt(reynolds)

def thermal_boundary_layer(x, fluid: Fluid):
    return vel_boundary_layer(x, fluid) * PRANDTL_NUMBER[fluid]**(-1/3)

def problem4() -> None:
    plt.rcParams.update({'font.size': 12})

    fluid_name = {Fluid.AIR: "air", Fluid.WATER: "water", Fluid.ENGINE_OIL: "engine oil", Fluid.MERCURY: "mercury"}
    fluid_color = {Fluid.AIR: "lightblue", Fluid.WATER: "blue", Fluid.ENGINE_OIL: "brown", Fluid.MERCURY: "gray"}

    x_min, x_max1 = 0, 0.040
    n_points = 501
    x = np.linspace(x_min, x_max1, n_points)
    fig, (ax1, ax2) = plt.subplots(2, 1)

    factor = 1000
    for fluid in Fluid:
        label_velocity = f"{fluid_name[fluid]} (velocity)"
        label_thermal = f"{fluid_name[fluid]} (thermal)"
        ax1.plot(x*factor, vel_boundary_layer(x, fluid)*factor, label=label_velocity, color=fluid_color[fluid])
        ax1.plot(x*factor, thermal_boundary_layer(x, fluid)*factor, label=label_thermal, color=fluid_color[fluid], linestyle="--")

        ax2.plot(x*factor, vel_boundary_layer(x, fluid)*factor, label=label_velocity, color=fluid_color[fluid])
        ax2.plot(x*factor, thermal_boundary_layer(x, fluid)*factor, label=label_thermal, color=fluid_color[fluid], linestyle="--")

    for ax in [ax1, ax2]:
        ax.set_xlabel("x (mm)")
        ax.set_ylabel("Boundary layer thickness (mm)")
        ax.grid()

    ax1.legend()
    ax2.set_ylim(0, 5)
    fig.suptitle("Velocity and Thermal Boundary Layers over a Flat Plate")

    plt.show()




