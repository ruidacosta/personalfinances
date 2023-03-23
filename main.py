import argparse
import os
import sys
import extract
import configparser
import storage as stg
from extractions import ExtractionLine

__version__ = '0.1'


class Style:
    RED: str = '\033[91m'
    GREEN: str = '\033[92m'
    BOLD: str = '\033[1m'
    ENDC: str = '\033[0m'


# File types
FT_CONFIG = 1
FT_EXTRACT = 2


def process_arguments():
    parser = argparse.ArgumentParser(
        description='This allow us to load transactions from home banking report into Personal Finances app. This app '
                    'could be a Google Spreadsheet, or other (not developed yet in this version).'
    )
    parser.add_argument('file_path', type=str, help='path to the excel file with extraction')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__, help='show version')
    parser.add_argument('-c', '--config', action='store', dest='config', help='path to configuration file')
    args = parser.parse_args()
    return vars(args)


def check_exists_valid(file: str, file_type: int) -> bool:
    if os.path.exists(file) and os.path.isfile(file):
        # check is valid config file
        if file_type == FT_CONFIG:
            return True
        elif file_type == FT_EXTRACT:
            return True
        else:
            return True
    else:
        return False


def print_error(error_msg: str) -> None:
    print(f'{Style.RED}{Style.BOLD}Error:{Style.ENDC}{Style.RED} {error_msg}{Style.ENDC}')


def load_config_file(config_file: str) -> configparser.ConfigParser:
    if not check_exists_valid(config_file, FT_CONFIG):
        print_error(f'{config_file} is not a valid config file.')
        sys.exit(1)
    else:
        config = configparser.ConfigParser() 
        config.read(config_file)
        return config


def create_config(args: dict[str, str]):
    config = configparser.ConfigParser()
    return config


def load_extract(file_data: str) -> list[ExtractionLine]:
    if not check_exists_valid(file_data, FT_EXTRACT):
        print_error(f'{file_data} is not a valid data file.')
        sys.exit(1)
    extraction = extract.extraction(extract.CREDITO_AGRICOLA)
    extraction.load_extraction(file_data)
    extraction.process_extraction()
    return extraction.get_data()


def process_extract(data: list[ExtractionLine]) -> list[ExtractionLine]:
    return data


def store_data(data: list[ExtractionLine], config: configparser.ConfigParser) -> None:
    storage = stg.storage(stg.GOOGLE_SPREADSHEET, config)
    storage.save(data)


def main():
    args = process_arguments()
    print('Starting...')
    if args['config']:
        print(f"Reading configuration file {args['config']}...")
        config = load_config_file(args['config'])
    else:
        print('Reading parameters...')
        config = create_config(args)
    print(f"Extracting data from file {args['file_path']}...")
    data = load_extract(args['file_path'])
    print(f'Processing data...')
    data = process_extract(data)
    print('Storing data...')
    store_data(data, config)
    print('Done')


if __name__ == '__main__':
    main()
