from enum import Enum
from typing import Optional

class NodeType(Enum):
    WASTE = 'waste'
    LOCAL = 'local_sorting_facility'
    REGIONAL = 'regional_sorting_facility'
    RECYCLING = 'regional_recycling_facility'

class WasteType(Enum):
    UNPROCESSED = 'pickup'
    LOCALLY_SORTED = 'local sorted'
    REGIONALLY_SORTED = 'regional sorted'
    PROCESSED = 'done'

PROCESSABLE: dict[NodeType, Optional[WasteType]] = {
    NodeType.WASTE: None,
    NodeType.LOCAL: WasteType.UNPROCESSED,
    NodeType.REGIONAL: WasteType.LOCALLY_SORTED,
    NodeType.RECYCLING: WasteType.REGIONALLY_SORTED,
}
RESULTS = {
    NodeType.LOCAL: WasteType.LOCALLY_SORTED,
    NodeType.REGIONAL: WasteType.REGIONALLY_SORTED,
    NodeType.RECYCLING: WasteType.PROCESSED,
}
