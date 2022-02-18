from interp.general_table import GeneralTable

def task_b() -> None:
    #  t_tab corresponds to table A-2
    t_tab = GeneralTable("tables/saturated_water_temp_table.csv")
    
    temp1 = 34
    temp_water = 20

    cpa = 1.005
    cpv = 1.86

    humid_ratio1 = 0.010
    press = 1
    hfg_20 = t_tab.interpolate_specific_prop("temp", 20, "hfg")

    temp_min, temp_max = temp_water, temp1
    delta_temp = 0.01
    temp2 = temp_min
    old_res = float("inf")
    while temp2 <= temp_max:
        pv2 = t_tab.interpolate_specific_prop("temp", temp2, "press")
        humid_ratio2 = 0.622*pv2/(press-pv2)
        res = (cpa + humid_ratio1*cpv)*(temp1 - temp2)
        res += (humid_ratio2-humid_ratio1)*(-hfg_20 + cpv*(temp_water - temp2))
        if abs(res) < abs(old_res):
            old_res = res
            solution_temp = temp2
        temp2 += delta_temp

    print(round(solution_temp, 2))
    print(round(t_tab.interpolate_specific_prop("temp", solution_temp, "press"), 5))

def task_c() -> None:
    t_tab = GeneralTable("tables/saturated_water_temp_table.csv")
    # # pg2 = 0.0610
    # # print(t_tab.interpolate_props("press", pg2))
    # # t_tab.print_props("press", pg2)
    # # t_tab.print_props("temp", temp2)
    # air_tab = GeneralTable("tables/ideal_gas_prop_air.csv")
    # temp1 = 34
    # temp2 = 20.68
    # temp3 = 26.45
    # t_tab.print_props("temp", temp1)
    # t_tab.print_props("temp", temp2)
    # t_tab.print_props("temp", temp3)
    p_tab = GeneralTable("tables/saturated_water_press_table.csv")
    p_tab.print_props("press", 0.1307)
    t_tab.print_props("press", 0.1307)
