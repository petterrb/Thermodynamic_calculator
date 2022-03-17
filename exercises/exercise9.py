IDEAL_GAS_CONST = 8.314


def f_van_der_waal(temp, press, v, a, b):
    return IDEAL_GAS_CONST * temp / (v - b) * 0.01 - a/v**2 - press

def df_van_der_waal(temp, _, v, a, b):
    return -IDEAL_GAS_CONST * temp / (v - b)**2  * 0.01 + 2*a/v**3

def f_riedlich_kwong(temp, press, v, a, b):
    return IDEAL_GAS_CONST * temp / (v - b) * 0.01 - a/(v*(v+b)*temp**0.5) - press

def df_riedlich_kwong(temp, _, v, a, b):
    return -IDEAL_GAS_CONST * temp / (v - b)**2  * 0.01 + a*(2*v+b) / (v**2*(v+b)**2) * 1 / temp**0.5


def newtons_method(choice=0, tol=0.00001):
    temp = 400 + 273
    press = 200
    a, b = 5.531, 0.0305
    M = 18.02

    v = 0.001 * M
    specific_vol_old = v
    diff = float("Inf")

    func, dfunc = None, None
    if choice == 0:
        func = f_van_der_waal
        dfunc = df_van_der_waal
    elif choice == 1:
        func = f_riedlich_kwong
        dfunc = df_riedlich_kwong
        a, b = 142.59, 0.02111
    while diff > tol:
        f = func(temp, press, v, a, b)
        df = dfunc(temp, press, v, a, b)
        v = specific_vol_old - f/df
        diff = abs(v - specific_vol_old)
        specific_vol_old = v

    return v / M