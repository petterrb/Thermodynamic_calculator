from interp.general_table import GeneralTable

class SaturatedWaterTemp(GeneralTable):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)