from abc import ABC, abstractmethod
import csv
from docx import Document
import os
from typing import List
from QuoteEngine.QuoteModelFile import QuoteModel


class IngestorInterface(ABC):

    @staticmethod
    @abstractmethod
    def can_ingest(path: str) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def parse(path: str) -> List[QuoteModel]:
        pass


class IngestorCsv(IngestorInterface):
    @staticmethod
    def can_ingest(path: str) -> bool:
        extension = os.path.splitext(path)[1]
        return extension == ".csv"

    @staticmethod
    def parse(path: str) -> List[QuoteModel]:
        with open(path, mode='r') as input_file:
            reader = csv.DictReader(input_file)
            return [QuoteModel(**row) for row in reader]


class IngestorTxt(IngestorInterface):
    @staticmethod
    def can_ingest(path: str) -> bool:
        extension = os.path.splitext(path)[1]
        return extension == ".txt"

    @staticmethod
    def parse(path: str) -> List[QuoteModel]:
        with open(path, mode='r') as input_file:
            reader = input_file.readlines()
            return [QuoteModel(*map(lambda r: r.strip(), row.split("-"))) for row in reader]


class IngestorDocx(IngestorInterface):
    @staticmethod
    def can_ingest(path: str) -> bool:
        extension = os.path.splitext(path)[1]
        return extension == ".docx"

    @staticmethod
    def parse(path: str) -> List[QuoteModel]:
        document = Document(path)
        return [QuoteModel(*map(lambda r: r.strip().strip('\"'), para.text.split("-")))
                for para in document.paragraphs if para.text]


class Ingestor:
    extension_mapping = {
        '.csv': IngestorCsv,
        '.docx': IngestorDocx,
        '.txt': IngestorTxt,
    }

    @staticmethod
    def parse(path: str) -> List[QuoteModel]:
        extension = os.path.splitext(path)[1]
        if extension not in Ingestor.extension_mapping:
            return []
            raise ValueError(f"Ingestor: Extension not supported for extension {extension}, file: {path}")
        ingestor = Ingestor.extension_mapping[extension]
        if ingestor.can_ingest(path=path):  # allows to check more than extension type
            try:
                return ingestor.parse(path=path)
            except BaseException as e:
                raise ValueError(f"Ingestor {ingestor} failed for \t{path}\nwith error:\t{e}")
        raise ValueError(f"Ingestor {ingestor} not implemented for {path}")
