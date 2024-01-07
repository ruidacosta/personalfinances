import pandas as pd

from extractions import Extraction, ExtractionLine


class CAExtraction(Extraction):
    def __init__(self):
        super().__init__()
        self.temp_data = []
        self.data = []

    def load_extraction(self, file: str) -> None:
        excel_data = pd.read_excel(file, skiprows=5, skipfooter=3, parse_dates=[0])
        data = pd.DataFrame(excel_data)
        self.temp_data = data.values.tolist()

    def process_extraction(self) -> None:
        # revert the extraction
        self.temp_data.reverse()
        # convert from DataFrame to list
        for row in self.temp_data:
            line = ExtractionLine(row[0], row[2], row[4], row[3])
            self.data.append(line)
        self.__process_category()

    def __process_category(self) -> None:
        pass

    def get_data(self) -> list[ExtractionLine]:
        return self.data

