import numpy as np
import matplotlib.pyplot as plt
from interp.general_table import GeneralTable

OIL_TABLE = GeneralTable("tables/thermophys_props_engine_oil_atm_press.csv")
VELOCITY_INF = 0.1
LENGTH = 1
TEMP_FILM = 273 + (100 + 20) / 2


def reynolds(x):
    dyn_visc = OIL_TABLE.interpolate_specific_prop("temp", TEMP_FILM, "nu")
    return VELOCITY_INF * x / dyn_visc

def boundary_layer(x):
    return 5*x/np.sqrt(reynolds(x))

def thermal_boundary_layer(x):
    prandtl_number = OIL_TABLE.interpolate_specific_prop("temp", TEMP_FILM, "Pr")
    return boundary_layer(x) * prandtl_number**(-1/3)

def surface_shear_stress(x):
    density = OIL_TABLE.interpolate_specific_prop("temp", TEMP_FILM, "rho")
    return 0.5 * density * VELOCITY_INF**2 * 0.664 * reynolds(x)**(-0.5)

def conv_coefficient(x):
    conductivity = OIL_TABLE.interpolate_specific_prop("temp", TEMP_FILM, "k")
    prandtl_number = OIL_TABLE.interpolate_specific_prop("temp", TEMP_FILM, "Pr")
    dyn_visc = OIL_TABLE.interpolate_specific_prop("temp", TEMP_FILM, "nu")
    return 0.332 * conductivity * prandtl_number**(1/3) * np.sqrt(VELOCITY_INF/dyn_visc) * 1/np.sqrt(x)

def heat_flux(x):
    temp_surface, temp_inf = 100 + 273, 20 + 273
    return  conv_coefficient(x)*(temp_surface - temp_inf)

def plot_problem1():
    function_list = [boundary_layer, thermal_boundary_layer, surface_shear_stress, conv_coefficient, heat_flux]
    x_label = "x (m)"
    y_label_list = ["y (m)", "y (m)", "tau (N/m^2)", "h (W/m^2 K)", "q' (W/m)"]
    title_list = [
        "Velocity Boundary Layer",
        "Thermal Boundary Layer",
        "Surface Shear Stress",
        "Convection Coefficient",
        "Heat Flux"
    ]

    x = np.linspace(0, 1, 501)
    for i, func in enumerate(function_list):
        fig, (ax) = plt.subplots()
        ax.plot(x, func(x))
        ax.set_title(title_list[i])
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label_list[i])
        ax.grid()
        fig.savefig(f"figures/fig_1_{i+1}")

