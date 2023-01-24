import csv
import numpy as np
import matplotlib.pyplot as plt

class Substance:
    def __init__(self, gas: str, v: float, cp):
        self.v = v  # stochiometric coefficient
        self.cp = cp
        self.M, self.h, self.g, self.s, self.HHV, self.LHV = get_prop(gas)


def get_prop(gas: str):
    filename = "other_data/thermochem_props_substances_std.csv"
    prop_data = list()
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        for row in reader:
            if row[1] == gas:
                prop_data = row[2:]
                for i, val in enumerate(prop_data):
                    prop_data[i] = float(val)

    if not len(prop_data):
        raise ValueError(f"No substance with the name {gas}")

    return prop_data


def sum_enthalpy_formation(gases: list):
    h = 0
    for gas in gases:
        h += gas.v * gas.h
    return h

def sum_absolute_entropy(gases: list):
    s = 0
    for gas in gases:
        s += gas.v * gas.s
    return s

def sum_specific_heat(gases: list):
    cp = 0
    for gas in gases:
        cp += gas.v * gas.cp
    return cp

def gibbs_free_energy(gases: list, temp):
    temp0 = 298
    sum_h = sum_enthalpy_formation(gases)
    sum_s = sum_absolute_entropy(gases)
    sum_cp = sum_specific_heat(gases)

    delta_G = sum_h
    delta_G += (temp - temp0) * sum_cp
    delta_G -= temp * sum_s
    delta_G -= temp * np.log(temp/temp0) * sum_cp

    return delta_G

def equilibrium_const_log(gases: list, temp):
    delta_G = gibbs_free_energy(gases, temp)
    return np.exp(-delta_G / (8.314 * temp))

def plot_equilibrium_const(gases: list, temp_range=[298, 3500]):
    (temp_min, temp_max) = temp_range
    temp = np.linspace(temp_min, temp_max, 501)
    logK = equilibrium_const_log(gases, temp)

    __, (ax) = plt.subplots(1, 1)
    ax.plot(temp, logK)
    ax.grid()
    ax.set_yscale('log')
    ax.set_xlabel('Temperature (K)')
    ax.set_ylabel('equilibrium constant (-)')
    plt.show()




def main():
    co = Substance("CO(g)", 1, 29)
    h2 = Substance("H2(g)", 3, 30)
    ch4 = Substance("CH4(g)", -1, 50)
    h2o = Substance("H2O(g)", -1, 36)

    gases = [co, h2, ch4, h2o]
    temp = 1500

    plot_equilibrium_const(gases)

    # oxygen1 = Substance("O2(g)", -1, 29.497)
    # oxygen2 = Substance("O(g)", 2, 29.497)
    # gases = [oxygen1, oxygen2]
    # temp = 298

    # delta_G = gibbs_free_energy(gases, temp)
    #
    # K = np.exp(-delta_G/(8.314*temp))
    #
    # return np.log10(K)



