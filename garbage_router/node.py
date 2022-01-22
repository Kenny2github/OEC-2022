from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Node:
    id: int
    lat: int
    long: int
    type: str
    plastic_amt: int
    risk: float

    @classmethod
    def from_csv_row(cls, row: tuple[str, str, str, str, str, str]) -> Node:
        id, lat, long, type, plastic_amt, risk = row
        return cls(int(id), int(lat), int(long),
                   type, int(plastic_amt), float(risk))