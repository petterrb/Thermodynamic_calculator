from interp.general_table import GeneralTable


def main() -> None:
    sat_water_temp_tab = "tables/saturated_water_temp_table.csv"
    sat_water_press_tab = "tables/saturated_water_press_table.csv"
    
    table_water_temp = GeneralTable(sat_water_temp_tab)
    table_water_press = GeneralTable(sat_water_press_tab)

    print(table_water_temp.interpolate_props("temp", 25))
    print(table_water_temp.interpolate_specific_prop("temp", 25.01, "hfg"))

if __name__ == "__main__":
    main()