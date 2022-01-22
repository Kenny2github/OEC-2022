from dataclasses import dataclass
from .enums import WasteType

@dataclass
class Waste:
    amount: int
    status: WasteType = WasteType.UNPROCESSED

    @property
    def done(self) -> bool:
        return self.status == WasteType.PROCESSED