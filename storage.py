import configparser
import math
import gspread

from gspread.utils import ValueInputOption

from extractions import ExtractionLine


class Style:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'


GOOGLE_SPREADSHEET = 1


class Storage:
    def __init__(self, config: configparser.ConfigParser) -> None:
        self.config = config

    def save(self, data: list[ExtractionLine]) -> None:
        pass


class GoogleSpreadsheetStorage(Storage):
    def __init__(self, config: configparser.ConfigParser) -> None:
        super().__init__(config)
        if config.has_section('CREDENTIALS'): 
            self.credentials_file = config['CREDENTIALS']['file'] if config.has_option('CREDENTIALS', 'file') else ''
        else:
            error_msg = f'There is no CREDENTIALS section in config file.'
            print(f'{Style.RED}{Style.BOLD}Error:{Style.ENDC}{Style.RED} {error_msg}{Style.ENDC}')
            return
        if config.has_section('GOOGLE_SPREADSHEET'):
            self.spreadsheet_name = config['GOOGLE_SPREADSHEET']['name'] if config.has_option('GOOGLE_SPREADSHEET', 'name') else ''
            self.worksheet_name = config['GOOGLE_SPREADSHEET']['worksheet'] if config.has_option('GOOGLE_SPREADSHEET', 'worksheet') else ''
            try:
                self.service = gspread.service_account(filename=self.credentials_file)
            except Exception as ex:
                error_msg = f'Could not start the service :: {ex}'
                print(f'{Style.RED}{Style.BOLD}Error:{Style.ENDC}{Style.RED} {error_msg}{Style.ENDC}')
            try:
                self.spreadsheet = self.service.open(self.spreadsheet_name)
            except Exception as ex:
                error_msg = f'Could not open the spreadsheet :: {ex}'
                print(f'{Style.RED}{Style.BOLD}Error:{Style.ENDC}{Style.RED} {error_msg}{Style.ENDC}')
            try:
                self.worksheet = self.spreadsheet.worksheet(self.worksheet_name)
                self.__read_lines()
            except Exception as ex:
                error_msg = f'Could not read the data :: {ex}'
                print(f'{Style.RED}{Style.BOLD}Error:{Style.ENDC}{Style.RED} {error_msg}{Style.ENDC}')
        else:
            error_msg = f'There is no GOOGLE_SPREADSHEET section in config file.'
            print(f'{Style.RED}{Style.BOLD}Error:{Style.ENDC}{Style.RED} {error_msg}{Style.ENDC}')

    def save(self, data: list[ExtractionLine]) -> None:
        to_add: list[list[str]] = []
        for row in data:
            print(row)
            if self.__row_exists(row):
                tmp = [
                    row.date.strftime('%Y-%m-%d'), # Date
                    row.description, # Description
                    '', # Category
                    '' if math.isnan(row.income) else row.income, # Income
                    '' if math.isnan(row.debit) else row.debit # Debit
                ]
                to_add.append(tmp)
        self.worksheet.append_rows(to_add, ValueInputOption.user_entered)

    def __row_exists(self, row: ExtractionLine) -> bool:
        for line in self.values:
            if (
                # This comparative is not good
                    row.date.strftime('%Y-%m-%d') == line[0] and
                    row.description == line[1] and
                    not (row.debit if not math.isnan(row.debit) else '') != (
                            line[4] if line[4] == '' else float(line[4][1:].replace(',',''))) and
                    not (row.income if not math.isnan(row.income) else '') != (
                            line[3] if line[3] == '' else float(line[3][1:].replace(',','')))
            ):
                return False
        return True

    def __read_lines(self) -> None:
        self.values = self.worksheet.get_values()[1:]


def storage(storage_type: int, config: configparser.ConfigParser):
    storages = {
        GOOGLE_SPREADSHEET: GoogleSpreadsheetStorage
    }
    return storages[storage_type](config)


def main():
    pass


if __name__ == '__main__':
    main()
