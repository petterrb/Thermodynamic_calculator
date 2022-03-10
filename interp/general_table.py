def is_number(x: str) -> bool:
    test_x = x.replace('.', '', 1)
    test_x = test_x.replace('-', '', 1)
    return test_x.isdigit()

class GeneralTable:
    def __init__(self, filename: str) -> None:
        self.identifier, self.name, self.header, self.table = self._create_table(filename)
        self.n_rows = len(self.table)
        self.n_cols = len(self.header)
        self.prop_dict = self._create_property_dict()

    # known_prop is the known property, and known_val is its corresponding value.
    def interpolate_props(self, known_prop: str, known_val: float) -> list:
        # exception handling - check if requested property exists in this table.
        all_prop_keys = list(self.prop_dict.keys())
        if known_prop not in all_prop_keys:
            prop_key_string = ""
            for key in all_prop_keys:
                prop_key_string += key + ", "
            raise ValueError(f"Error: {known_prop} is not a valid property. Valid properties are:\n {prop_key_string}")

        # iterate through table to find which two values "known_val" sits in between and retrieve their indices.
        known_prop_index = self.prop_dict[known_prop]
        val1_index, val2_index = 0, 0
        val1, val2 = 0, 0
        for row in range(self.n_rows - 1):
            val1 = self.table[row][known_prop_index]
            val2 = self.table[row + 1][known_prop_index]
            if (val1 <= known_val <= val2) or (val2 <= known_val <= val1):
                val1_index, val2_index = row, row + 1
                break

        # exception handling - check if "known_val" exists within the table
        if not val2_index - val1_index:
            raise ValueError("Error: The specified value is not within the table values.")

        prop_row1, prop_row2 = self.table[val1_index], self.table[val2_index]
        interpolated_values = []

        # complete the interpolation for all properties in table.
        for col in range(self.n_cols):
            other_val1 = prop_row1[col]
            other_val2 = prop_row2[col]
            interp_val = self.__interp_values(known_val, val1, val2, other_val1, other_val2)
            interpolated_values.append(interp_val)

        return interpolated_values

    def interpolate_specific_prop(self, known_prop: str, known_val: float, requested_prop: str) -> float:
        interpolated_values = self.interpolate_props(known_prop, known_val)
        requested_index = self.prop_dict[requested_prop]
        return interpolated_values[requested_index]

    def print_props(self, known_prop: str, known_val: float, n_decimals: int = 6) -> None:
        interpolated_values = self.interpolate_props(known_prop, known_val)
        print("------------------------------------------")
        for prop in range(len(interpolated_values)):
            output_prop = self.header[prop]
            output_val = round(interpolated_values[prop], n_decimals)
            output_val_str = f"{output_val:,}".replace(',', ' ')

            output = [output_prop, output_val_str]
            print("{: <10} {: <10}".format(*output))
        print("------------------------------------------")

    def _create_table(self, filename: str):
        table = []
        with open(filename, 'r') as f:
            all_lines = f.readlines()
            identifier = int(all_lines.pop(0).strip())
            name = all_lines.pop(0).strip()
            header = all_lines.pop(0).split()
            for line in all_lines:
                table.append(line.split())

        for row in range(len(table)):
            for col in range(len(table[row])):
                if is_number(table[row][col]):
                    table[row][col] = float(table[row][col])

        return identifier, name, header, table

    def _create_property_dict(self) -> dict:
        prop_dict = {}
        for col in range(self.n_cols):
            prop_dict[self.header[col]] = col

        return prop_dict

    def __interp_values(self, x, x1, x2, y1, y2):
        return y1 + (x - x1) * (y2 - y1) / (x2 - x1)
