from interp.general_table import GeneralTable


class Task3:
    def __init__(self):
        self.table = GeneralTable("tables/ideal_gas_prop_selected_gases.csv")
        self.h_formation_dict = self.create_enthalpy_of_formation_dict()
        self.T2 = 273 + 350  # K
        self.T_ref = 273 + 15  # K
        self.cp_ethanol = 100.4  # kJ/kmol K
        self.n2_tot = 4.47 * 10 ** (-4)  # kmol
        self.n3_tot = 4.76 * 10 ** (-4)  # kmol
        self.n2 = self.create_n2_dict()
        self.n3 = self.create_n3_dict()

    def create_enthalpy_of_formation_dict(self) -> dict:
        h_formation_dict = dict()
        h_formation_dict["O2"] = 0
        h_formation_dict["N2"] = 0
        h_formation_dict["CO2"] = -393520
        h_formation_dict["H2O"] = -241820
        h_formation_dict["C2H50H"] = -235310
        return h_formation_dict

    def create_n2_dict(self):
        n2 = dict()
        den = 1 + 3 * (1 + 3.76)
        n2["O2"] = 3 / den
        n2["N2"] = 3 * 3.76 / den
        n2["CO2"] = 0
        n2["H2O"] = 0
        n2["C2H50H"] = 1 / den

        for key, value in n2.items():
            n2[key] = value * self.n2_tot

        return n2

    def create_n3_dict(self):
        n3 = dict()
        den = 2 + 3 + 11.28
        n3["O2"] = 0
        n3["N2"] = 11.28 / den
        n3["CO2"] = 2 / den
        n3["H2O"] = 3 / den
        n3["C2H50H"] = 0

        for key, value in n3.items():
            n3[key] = value * self.n3_tot

        return n3

    def get_delta_h(self, temp, requested_prop):
        h_temp = self.table.interpolate_specific_prop("temp", temp, requested_prop)
        h_ref = self.table.interpolate_specific_prop("temp", self.T_ref, requested_prop)
        return h_temp - h_ref

    def calc_energy_term(self, element: str, temp: float, n_moles: float):
        h_0f = self.h_formation_dict[element]
        delta_h = self.get_delta_h(temp, "h_" + element)
        pV = n_moles * 8.314 * temp
        return n_moles * (h_0f + delta_h - pV)

    def calc_ethanol_energy_term(self):
        h_0f = self.h_formation_dict["C2H50H"]
        delta_h = self.cp_ethanol * (self.T2 - self.T_ref)
        pV = self.n2["C2H50H"] * 8.314 * self.T2
        return self.n2["C2H50H"] * (h_0f + delta_h - pV)

    def calc_rhs(self, temp):
        react_O2 = self.calc_energy_term("O2", self.T2, self.n2["O2"])
        react_N2 = self.calc_energy_term("N2", self.T2, self.n2["N2"])
        react_C2H50H = self.calc_ethanol_energy_term()

        prod_CO2 = self.calc_energy_term("CO2", temp, self.n3["CO2"])
        prod_H2O = self.calc_energy_term("H2O", temp, self.n3["H2O"])
        prod_N2 = self.calc_energy_term("N2", temp, self.n2["N2"])

        return prod_CO2 + prod_H2O + prod_N2 - (react_O2 + react_N2 + react_C2H50H)

    def solve(self):
        T3 = 2500
        T_solution = T3
        T_max = 3000
        temp_iteration = 1
        old_res = float("Inf")

        while T3 < T_max:
            res = abs(self.calc_rhs(T3))
            if res < old_res:
                old_res = res
                T_solution = T3

            T3 += temp_iteration

        return T_solution
