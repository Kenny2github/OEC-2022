from __future__ import annotations
from dataclasses import dataclass
from math import hypot
from .enums import NodeType

@dataclass
class Node:
    id: int
    lat: int
    long: int
    type: NodeType
    plastic_amt: int
    risk: float

    def __hash__(self) -> int:
        return hash((self.lat, self.long))

    @classmethod
    def from_csv_row(cls, row: tuple[str, str, str, str, str, str]) -> Node:
        print(row)
        id, lat, long, type, plastic_amt, risk = row
        return cls(int(id), int(lat), int(long),
                   NodeType(type), int(plastic_amt), float(risk))

    def dist(self, other: Node) -> float:
        return hypot(self.lat - other.lat, self.long - other.long)
