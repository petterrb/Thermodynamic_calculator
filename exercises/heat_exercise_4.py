import numpy as np
import matplotlib.pyplot as plt


class Cylinder:
    def __init__(self):
        self.r1 = 0.008  # m
        self.r2 = 0.011  # m
        self.r3 = 0.014  # m

        self.q = 10e8  # W/m3

        self.T_inf = 600  # K
        self.T2 = 931  # K
        self.T3 = 701.8  # K

        self.k_g = 3  # W/mK
        self.k_Th = 57  # W/mK

        self.h = 2000  # W/m2K


def temp_Th(r, c: Cylinder):
    c1 = c.q/(2*c.k_Th)*c.r1**2
    c2 = c.T2 + c.q/(2*c.k_Th)*(c.r2**2/2 - c.r1**2*np.log(c.r2))
    return -c.q/(4*c.k_Th)*r**2 + c1*np.log(r) + c2

