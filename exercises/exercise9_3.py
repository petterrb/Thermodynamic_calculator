import numpy as np
import matplotlib.pyplot as plt

IDEAL_GAS_CONST = 8.314
MOLAR_MASS = 44.01
SPECIFIC_GAS_CONSTANT = IDEAL_GAS_CONST / MOLAR_MASS
BAR_COEFFICIENT = 10**(-5)


class Pair:
    def __init__(self, a, b):
        self.a = a
        self.b = b


def ideal_gas(T, v, _, __):
    return SPECIFIC_GAS_CONSTANT * T / v * BAR_COEFFICIENT

def van_der_waal(T, v, a, b):
    return SPECIFIC_GAS_CONSTANT * T / (v - b) * - a/v**2

def berthelot(T, v, a, b):
    return IDEAL_GAS_CONST * T / (v - b) * 0.01 - a /(T * v**2)

def riedlich_kwong(T, v, a, b):
    return IDEAL_GAS_CONST * T / (v - b) * 0.01 - a/(v*(v+b)*T**0.5)

def benedict_webb_rubin(T, v, _, __):
    a = 0.1386
    A = 2.7737
    b = 0.007210
    B = 0.04991
    c = 1.512 * 104**4
    C = 1.404 * 10**5
    alpha = 8.47 * 10**(-5)
    gamma = 0.00539
    R = IDEAL_GAS_CONST
    terms = list()
    terms.append(R * T / v)
    terms.append((B*R*T - A - C/T**2)/v**2)
    terms.append((b*R*T - a)/v**3)
    terms.append(a*alpha/v**6)
    terms.append(c/(v**3*T**2)*(1+gamma/v**2)*np.exp(-gamma/v**2))

    return sum(terms)

def plot_state_funcs():
    ab_dict = {
        ideal_gas: Pair(None, None),
        # van_der_waal: Pair(3.647*100, 0.0428),
        # berthelot: Pair(57.3, 9.72*10**(-4)),
        # riedlich_kwong: Pair(64.43, 0.02963),
        # benedict_webb_rubin: Pair(None, None)
    }

    label_dict = {
        ideal_gas: "Ideal gas",
        # van_der_waal: "van der Waal",
        # berthelot: "Berthelot",
        # riedlich_kwong: "Riedlich-Kwong",
        # benedict_webb_rubin: "Benedict-Webb-Rubin"
    }

    T = 240
    v_min, v_max = 10**(-3), 0.05
    v = np.linspace(v_min, v_max, 501)

    _, (ax) = plt.subplots(1, 1)

    for func, _ in ab_dict.items():
        a, b = ab_dict[func].a, ab_dict[func].b
        label = label_dict[func]
        ax.plot(v, func(T, v*MOLAR_MASS, a, b), label=label)

    ax.grid()
    ax.set_xlabel("Specific volume (m3/kg)")
    ax.set_ylabel("Pressure (bar)")
    ax.legend()
    plt.show()