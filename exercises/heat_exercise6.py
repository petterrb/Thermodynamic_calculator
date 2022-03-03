from interp.general_table import GeneralTable
import numpy as np
import matplotlib.pyplot as plt


class Task2():
    def __init__(self) -> None:
        self.table = GeneralTable("tables/thermophys_props_air_atm_press.csv")
        self.temp_inf = 25 + 273  # K
        self.velocity = 10  # m/s
        self.area = (4 * 10 ** (-3)) ** 2  # m^2
        self.char_length = 0.120  # m
        self.width = 0.004  # m
        self.dissipation = 0.030  # W

    def reynolds(self, x: float, temp: float) -> float:
        nu = self.table.interpolate_specific_prop("temp", temp, "nu") * 10**(-6)
        return self.velocity * x / nu

    def nusselt(self, x: float, temp: float) -> float:
        Re = self.reynolds(x, temp)
        Pr = self.table.interpolate_specific_prop("temp", temp, "Pr")
        return 0.04 * Re**0.85 * Pr**(1/3)

    def convection_coefficient(self, x: float, temp: float) -> float:
        Nu = self.nusselt(x, temp)
        kf = self.table.interpolate_specific_prop("temp", temp, "k") * 10**(-3)
        return Nu / x * kf

    def solve(self):
        temp_surface = 273 + 25
        temp_solution = temp_surface
        step = .01
        old_res = float("Inf")
        while temp_surface < 500:
            temp_m = (temp_surface + self.temp_inf) / 2
            h = self.convection_coefficient(self.char_length, temp_m)
            lhs = self.dissipation
            rhs = (temp_surface - self.temp_inf) * self.area * h
            res = abs(lhs - rhs)

            if res < old_res:
                old_res = res
                temp_solution = temp_surface

            temp_surface += step

        return temp_solution


class Task3():
    def __init__(self) -> None:
        self.table = GeneralTable("tables/thermophys_props_air_atm_press.csv")
        self.temp_inf = 25 + 273  # K
        self.area = (4 * 10 ** (-3)) ** 2  # m^2
        self.char_length = 0.120  # m
        self.width = 0.004  # m

    def reynolds(self, x: float, temp: float, vel: float):
        nu = self.table.interpolate_specific_prop("temp", temp, "nu") * 10**(-6)
        return vel * x / nu

    def nusselt(self, x: float, temp: float, vel: float):
        Re = self.reynolds(x, temp, vel)
        Pr = self.table.interpolate_specific_prop("temp", temp, "Pr")
        return 0.04 * Re**0.85 * Pr**(1/3)

    def convection_coefficient(self, x: float, temp: float, vel: float):
        Nu = self.nusselt(x, temp, vel)
        kf = self.table.interpolate_specific_prop("temp", temp, "k") * 10**(-3)
        return Nu / x * kf

    def get_max_power(self, vel, temp_surface=273+85):
        temp_m = (temp_surface + self.temp_inf) / 2
        h = self.convection_coefficient(self.char_length, temp_m, vel)
        max_power = (temp_surface - self.temp_inf) * self.area * h
        return max_power

    def get_max_power_radiation(self, vel, temp_surface=273+85):
        convection_power = self.get_max_power(vel)

        emissivity = 0.8
        sigma = 5.67 * 10**(-8)
        temp_surroundings = 273 + 25
        radiation_power = emissivity * self.area * sigma * (temp_surface**4 - temp_surroundings**4)

        return convection_power + radiation_power

    def plot(self) -> None:
        vel_min, vel_max = 1, 25
        n_points = 501
        vel = np.linspace(vel_min, vel_max, n_points)
        max_power = self.get_max_power(vel)
        max_power_radiation = self.get_max_power_radiation(vel)
        plt.rcParams.update({'font.size': 12})

        __, (ax1, ax2) = plt.subplots(1, 2)
        ax1.plot(vel, max_power*1000, label="Without Radiation")
        ax1.plot(vel, max_power_radiation*1000, label="With Radiation")
        ax1.set_xlabel("Air Velocity [m/s]")
        ax1.set_ylabel("Maximum power dissipation [mW]")
        ax1.set_title("Microchip power dissipation")
        ax1.legend()

        max_power_difference = (max_power_radiation - max_power) / max_power_radiation
        ax2.plot(vel, max_power_difference*100)
        ax2.set_xlabel("Air Velocity [m/s]")
        ax2.set_ylabel("Relative difference (percent)")
        ax2.set_title("Relative difference between radiation and no radiation")

        plt.show()
