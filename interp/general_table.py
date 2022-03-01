class GeneralTable:
    def __init__(self, filename: str) -> None:
        self.identifier, self.name, self.header, self.table = self._create_table(filename)
        # self.table = self._create_table(filename)
        # self.identifier = self.table.pop(0)
        # self.name = self.table.pop(0)
        # self.header = self.table.pop(0)
        self.nrows = len(self.table)
        self.ncols = len(self.header)
        self.prop_dict = self._create_property_dict()


    # kprop is the known property, and kval is its corresponding value.
    def interpolate_props(self, kprop: str, kval: float) -> list:
        # exception handling - check if requested property exists in this table.
        all_prop_keys = list(self.prop_dict.keys())
        if kprop not in all_prop_keys:
            prop_key_string = ""
            for key in all_prop_keys:
                prop_key_string += key + ", "
            raise ValueError(f"Error: {kprop} is not a valid property. Valid properties are:\n {prop_key_string}")
        
        # iterate through table to find which two values "kval" sits in between and retrieve their indicies.
        kprop_index = self.prop_dict[kprop]
        index_error = True
        for row in range(self.nrows-1):
            val1 = self.table[row][kprop_index]
            val2 = self.table[row+1][kprop_index]
            if (val1 <= kval <= val2) or (val2 <= kval <= val1):
                val1_index, val2_index = row, row+1
                index_error = False
                break
        
        # exception handling - check if "kval" exists within the table
        if index_error:
            raise ValueError("Error: The specified value is not within the table values.")

        prop_row1, prop_row2 =  self.table[val1_index], self.table[val2_index]
        interpolated_values = []

        # complete the interpolation for all properties in table.
        for col in range(self.ncols):
            other_val1 = prop_row1[col]
            other_val2 = prop_row2[col]
            interp_val = self.__interp_values(kval, val1, val2, other_val1, other_val2)
            interpolated_values.append(interp_val)

        return interpolated_values


    def interpolate_specific_prop(self, kprop: str, kval: float, reqprop: str) -> float:
        interpolated_values = self.interpolate_props(kprop, kval)
        reqindex = self.prop_dict[reqprop]
        return interpolated_values[reqindex]


    def print_props(self, kprop: str, kval: float, n_decimals: int=6) -> None:
        interpolated_values = self.interpolate_props(kprop, kval)
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
                is_number = table[row][col].replace('.', '', 1).isdigit()
                if is_number:
                    table[row][col] = float(table[row][col])

        return identifier, name, header, table


    def _create_property_dict(self) -> dict:
        prop_dict = {}
        for col in range(self.ncols):
            prop_dict[self.header[col]] = col

        return prop_dict
    
    
    def __interp_values(self, x, x1, x2, y1, y2):
        return y1 + (x-x1)*(y2-y1)/(x2-x1)