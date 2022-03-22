import numpy as np
import matplotlib.pyplot as plt

IDEAL_GAS_CONST = 8.314  # kJ/kg K
MOLAR_MASS = 44.01  # kg/kmol


class FuncData:
    def __init__(self, a, b, label=None):
        self.a = a
        self.b = b
        self.label = label

# T (K), v (m3/kmol)
def ideal_gas(T, v, _, __):
    R = IDEAL_GAS_CONST
    return R*T / v

# T (K), v (m3/kmol), a (kPa m6/kmol2), b (m3/kmol)
def van_der_waal(T, v, a, b):
    R = IDEAL_GAS_CONST
    return R*T / (v-b) - a/v**2


def berthelot(T, v, a, b):
    R = IDEAL_GAS_CONST
    return R * T / (v - b) - a /(T * v**2)

def riedlich_kwong(T, v, a, b):
    R = IDEAL_GAS_CONST
    return R * T / (v - b) - a/(v*(v+b)*T**0.5)

def benedict_webb_rubin(T, v, _, __):
    a = 0.1386
    A = 2.7737
    b = 0.007210
    B = 0.04991
    c = 1.512 * 10**4
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
    func_dict = {
        ideal_gas: FuncData(None, None, "Ideal gas"),
        van_der_waal: FuncData(3.647*100, 0.0428, "van der Waal"),
        berthelot: FuncData(111*10**3, 0.0428, "Berthelot"),
        riedlich_kwong: FuncData(64.43*100, 0.02963, "Riedlich-Kwong"),
        benedict_webb_rubin: FuncData(None, None, "Benedict-Webb-Rubin"),
    }

    T = 240 + 273
    v_min, v_max = 0.2, 1
    # v_min /= MOLAR_MASS
    # v_max /= MOLAR_MASS
    v = np.linspace(v_min, v_max, 501)

    _, (ax) = plt.subplots(1, 1)

    for func, _ in func_dict.items():
        a, b, label = func_dict[func].a, func_dict[func].b, func_dict[func].label
        p = func(T, v, a, b)
        ax.plot(v, p, label=label)

    ax.grid()
    ax.set_xlabel("Specific volume (m3/kmol)")
    ax.set_ylabel("Pressure (kPa)")
    # ax.set_ylim(0, 5000)
    ax.legend()
    plt.show()
