import utilities.thermodynamic_functions as tf
import numpy as np


class Gas:
    def __init__(self, cp_coeffs, stoch_coeff, enthalpy_formation):
        self.cp_coeffs = cp_coeffs
        self.stoch_coeff = stoch_coeff
        self.enthalpy_formation = enthalpy_formation


def calc_delta_enthalpy(temp, temp_ref=298):
    methane = Gas([3.826, -3.979, 24.558, -22.733, 6.963], -1, -74850)
    water = Gas([4.070, -1.108, 4.152, -2.964, 0.807], -1, -241820)
    carbon_monoxide = Gas([3.710, -1.619, 3.692, -2.032, 0.240],1 , -110530)
    hydrogen = Gas([3.057, 2.677, -5.810, 5.521, -1.812], 3, 0)
    gases = [methane, water, carbon_monoxide, hydrogen]
    delta_enthalpy = 0
    for gas in gases:
        gas.cp_coeffs = tf.ideal_gas_coefficient_multiplication(gas.cp_coeffs)
        delta_enthalpy += gas.stoch_coeff * (gas.enthalpy_formation + tf.delta_h(temp_ref, temp, gas.cp_coeffs))

    return delta_enthalpy


def calc_J(gas, temp_ref=298):
    J = gas.enthalpy_formation
    for i, coeff in enumerate(gas.cp_coeffs):
        J -= coeff*temp_ref**(i+1) / (i+1)

    return J


def lnK_indefinite(gas, temp, temp_ref):
    (a, b, g, d, e) = gas.cp_coeffs
    J = calc_J(gas, temp_ref)
    val = -J/temp
    val += a*np.log(temp)
    val += b/2 * temp
    val += g/6 * temp**2
    val += d/12 * temp**3
    val += e/20 * temp**4
    return gas.stoch_coeff * tf.IDEAL_GAS_CONSTANT * val


def calc_K(temp, temp_ref=298):
    methane = Gas([3.826, -3.979, 24.558, -22.733, 6.963], -1, -74850)
    water = Gas([4.070, -1.108, 4.152, -2.964, 0.807], -1, -241820)
    carbon_monoxide = Gas([3.710, -1.619, 3.692, -2.032, 0.240], 1, -110530)
    hydrogen = Gas([3.057, 2.677, -5.810, 5.521, -1.812], 3, 0)
    gases = [methane, water, carbon_monoxide, hydrogen]
    lnK = 0

    for gas in gases:
        gas.cp_coeffs = tf.ideal_gas_coefficient_multiplication(gas.cp_coeffs)
        lnK += lnK_indefinite(gas, temp, temp_ref) - lnK_indefinite(gas, temp_ref, temp_ref)

    return np.exp(lnK)