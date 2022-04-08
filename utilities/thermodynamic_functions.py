import numpy as np


IDEAL_GAS_CONSTANT = 8.314 #  kJ/kmol*K


def ideal_gas_coefficient_multiplication(gas:list):
    new_gas = list()
    for i, val in enumerate(gas):
        new_gas.append(val*10**(-3*i))
    return new_gas


def integrate_cp_indefinite(temp, gas: list):
    (a, b, g, d, e) = gas
    return (a*temp + b/2*temp**2 + g/3*temp**3 + d/4*temp**4 + e/5*temp**5)*IDEAL_GAS_CONSTANT


def delta_h(temp1, temp2, gas: list):
    return integrate_cp_indefinite(temp2, gas) - integrate_cp_indefinite(temp1, gas)


def delta_s(temp1, temp2, press1, press2, gas:list):
    s1, s2 = 0, 0
    for i, c in enumerate(gas):
        s1 += c*temp1**i
        s2 += c*temp2**i

    return s2 - s1 - IDEAL_GAS_CONSTANT*np.log(press2/press1)
