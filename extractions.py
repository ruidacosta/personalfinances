class ExtractionLine:
    def __init__(self, date=None, description=None, income=None, debit=None) -> None:
        self.date = date
        self.description = description
        self.income = income
        self.debit = debit
        self.category = None

    def __str__(self) -> str:
        return f'(date: {self.date}, description: {self.description}, income: {self.income}, debit: {self.debit}, ' \
               f'category: {self.category})'


class Extraction:
    def __init__(self) -> None:
        pass

    def load_extraction(self, file: str) -> None:
        pass

    def process_extraction(self) -> None:
        pass

    def get_data(self) -> None:
        pass
