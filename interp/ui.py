import os
from interp.general_table import GeneralTable


class InterpMenu:
    def __init__(self) -> None:
        self.table_dict = self.__generate_tables()

    # Returns a list of all file names within the table folder.
    def __retrieve_files(self) -> list:
        root_dir = "tables"
        file_list = list()

        for _, _, files in os.walk(root_dir):
            for file_name in files:
                # rel_dir = os.path.relpath(dir_, root_dir)
                # rel_file = os.path.join(rel_dir, file_name)
                rel_file = os.path.join(root_dir, file_name)
                file_list.append(rel_file)

        return file_list

    # Creates a dictionary where the keys are identifiers (A-2, A-3, etc.) and the values
    # are the actual tables of the type GeneralTable
    def __generate_tables(self) -> dict:
        files = self.__retrieve_files()
        table_dict = dict()
        for filename in files:
            table = GeneralTable(filename)
            table_dict[table.identifier] = table

        return table_dict

    def __get_options(self) -> list:
        options = list()
        for identifier in sorted(self.table_dict):
            table = self.table_dict[identifier]
            # new_line = f"{table.identifier}: {table.name}"
            new_line = [table.identifier, table.name]
            options.append("{: <6} {: <6}".format(*new_line))

        return options

    def __print_options(self) -> None:
        print("Choose table you wish to retrieve data from:\n")
        options = self.__get_options()
        for opt in options:
            print(opt)

        print()

    def __get_table(self, identifier: str) -> GeneralTable:
        try:
            table = self.table_dict[int(identifier)]
        except:
            raise ValueError(f"Error: no table in the database corresponds to the identifier: {identifier}")

        return table

    def menu(self) -> None:
        user_input = ""
        print("Welcome to Petter's Thermodynamic Interpolation Tool (PTIT for short)")
        print("You can type 'quit' to exit the program")
        while user_input.lower() != "quit":
            self.__print_options()
            try:
                user_input = input()
                if user_input != "quit":
                    table = self.__get_table(user_input)
                    print(f"You have chosen: {table.name}")
                    known_property = input("Known property: ")
                    known_value = float(input("Value: "))
                    table.print_props(known_property, known_value)

            except ValueError as error:
                print(f"\n{error}\n")
