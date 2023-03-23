import creditoagricola


CREDITO_AGRICOLA = 1


def extraction(extract_type: int):
    extractors = {
        CREDITO_AGRICOLA: creditoagricola.CAExtraction
    }
    return extractors[extract_type]()


def main():
    pass


if __name__ == '__main__':
    main()
