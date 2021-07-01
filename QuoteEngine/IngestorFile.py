from abc import ABC, abstractmethod
from typing import List
from QuoteModelFile import QuoteModel


class IngestorInterface(ABC):

    @abstractmethod
    def can_ingest(self, path: str) -> bool:
        pass

    @abstractmethod
    def parse(self, path: str) -> List[QuoteModel]:
        pass

