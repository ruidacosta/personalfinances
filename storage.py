import configparser
import math
import os.path
import pickle
from typing import Any

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

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


def get_credentials(file, scopes) -> Any:
    credentials = None
    dir_path = os.path.dirname(os.path.realpath(file))
    if os.path.exists(dir_path + '/token.pickle'):
        with open(dir_path + '/token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(file, scopes=scopes)
            credentials = flow.run_local_server(port=0)
        with open(dir_path + '/token.pickle', 'wb') as token:
            pickle.dump(credentials, token)
    return credentials


DISCOVERY_SERVICE_URL = 'https://sheets.googleapis.com/$discovery/rest?version=v4'


class GoogleSpreadsheetStorage(Storage):
    def __init__(self, config: configparser.ConfigParser) -> None:
        super().__init__(config)
        if config.has_section('GOOGLE_SPREADSHEET'):
            SHEETS_READ_WRITE_SCOPE = 'https://www.googleapis.com/auth/spreadsheets'
            SCOPES = [SHEETS_READ_WRITE_SCOPE]
            self.spreadsheet_id = (
                config['GOOGLE_SPREADSHEET']['id'] if config.has_option('GOOGLE_SPREADSHEET', 'id') else ''
            )
            credential_file = (
                config['CREDENTIALS']['file'] if config.has_option('CREDENTIALS', 'file') else ''
            )
            self.credentials = get_credentials(credential_file, SCOPES)
            self.sheet = (
                config['GOOGLE_SPREADSHEET']['sheet'] if config.has_option('GOOGLE_SPREADSHEET', 'sheet') else ''
            )
            self.__read_lines()
        else:
            error_msg = f'There is no GOOGLE_SPREADSHEET section in config file.'
            print(f'{Style.RED}{Style.BOLD}Error:{Style.ENDC}{Style.RED} {error_msg}{Style.ENDC}')

    def save(self, data: list[ExtractionLine]) -> None:
        to_add: list[list[str]] = []
        for row in data:
            if self.__row_exists(row):
                tmp = [
                    row.date.strftime('%Y-%m-%d'),  # Date
                    row.description,  # Description
                    '',  # category
                    '' if math.isnan(row.income) else row.income,  # Income
                    '' if math.isnan(row.debit) else row.debit  # Debit
                ]
                to_add.append(tmp)
        service = build('sheets', 'v4', credentials=self.credentials, discoveryServiceUrl=DISCOVERY_SERVICE_URL)
        service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range=self.sheet + '!A:Z',
            body={
                'majorDimension': 'ROWS',
                'values': to_add
            },
            valueInputOption='USER_ENTERED'
        ).execute()

    def __row_exists(self, row: ExtractionLine) -> bool:
        for line in self.values:
            if (
                # This comparative is not good
                    row.date.strftime('%Y-%m-%d') == line[0] and
                    row.description == line[1] and
                    not (row.debit if not math.isnan(row.debit) else '') != (
                            line[4] if line[4] == '' else float(line[4][1:])) and
                    not (row.income if not math.isnan(row.income) else '') != (
                            line[3] if line[3] == '' else float(line[3][1:]))
            ):
                return False
        return True

    def __read_lines(self) -> None:
        service = build('sheets', 'v4', credentials=self.credentials, discoveryServiceUrl=DISCOVERY_SERVICE_URL)
        result = service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=self.sheet + '!A2:Z'
        ).execute()
        self.values = result.get('values', [])


def storage(storage_type: int, config: configparser.ConfigParser):
    storages = {
        GOOGLE_SPREADSHEET: GoogleSpreadsheetStorage
    }
    return storages[storage_type](config)


def main():
    pass


if __name__ == '__main__':
    main()
