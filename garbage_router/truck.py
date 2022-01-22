from dataclasses import dataclass

@dataclass
class Truck:
    unprocessed: int
    locally_sorted: int
    regionally_sorted: int
    recycled: int
