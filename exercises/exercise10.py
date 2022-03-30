import numpy as np


def const_vol_integral_indefinite_u(T, gas: list):
    R = 8.314
    (a, b, g, d, e) = gas
    return ((a-1)*T + b/2*T**2 + g/3*T**3 + d/4*T**4 + e/5*T**5)*R


def const_vol_integral_u(T1, T2, gas: list):
    return const_vol_integral_indefinite_u(T2, gas) - const_vol_integral_indefinite_u(T1, gas)


def const_temp_integral_u(T, v1, v2, a, b):
    return 3/(2*np.sqrt(T)) * a/b * np.log(v1*(v2+b)/(v2*(v1+b)))


def delta_u(T1, T2, v1, v2, v3, a, b, gas: list):
    u_1x = const_temp_integral_u(T1, v1, v3, a, b)
    u_yx = const_vol_integral_u(T1, T2, gas)
    u_y2 = const_temp_integral_u(T2, v3, v2, a, b)
    return u_1x + u_yx + u_y2


def const_vol_integral_indefinite_s(T, gas: list):
    R = 8.314
    (a, b, g, d, e) = gas
    return ((a-1)*np.log(T) + b*T + g/2*T**2 + d/3*T**3 + e/4*T**4)*R


def const_vol_integral_s(T1, T2, gas: list):
    return const_vol_integral_indefinite_s(T2, gas) - const_vol_integral_indefinite_s(T1, gas)


def const_temp_integral_s(T, v1, v2, a, b):
    R = 8.314
    return R*np.log((v2-b)/(v1-b)) + a/(2*b)*np.log(v2*(v1+b)/(v1*(v2+b)))*T**(-3/2)


def delta_s(T1, T2, v1, v2, v3, a, b, gas: list):
    s_1x = const_temp_integral_s(T1, v1, v3, a, b)
    s_yx = const_vol_integral_s(T1, T2, gas)
    s_y2 = const_temp_integral_s(T2, v3, v2, a, b)
    return s_1x + s_yx + s_y2


def pv(T, v, a, b):
    R = 8.314
    return R*T*v/(v-b) - a/(v+b)*T**(-0.5)


def delta_pv(T1, T2, v1, v2, a, b):
    return pv(T2, v2, a, b) - pv(T1, v1, a, b)


def delta_h(T1, T2, v1, v2, v3, a, b, gas: list):
    return delta_u(T1, T2, v1, v2, v3, a, b, gas) + delta_pv(T1, T2, v1, v2, a, b)


def calc_changes():
    M = 44.01
    co2 = [2.401, 8.735, -6.607, 2.002, 0.000]
    for i, val in enumerate(co2):
        co2[i] = val*10**(-3*i)

    a, b = 64.43 * 10**2, 0.02963
    T1, T2 = 280, 320
    v1, v2, v3 = 0.01*M, 0.02*M, 10*M
    print(delta_u(T1, T2, v1, v2, v3, a, b, co2)/M)
    print(delta_s(T1, T2, v1, v2, v3, a, b, co2)/M)
    print(delta_h(T1, T2, v1, v2, v3, a, b, co2)/M)
