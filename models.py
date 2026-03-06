from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Coordinates:
    lat: float
    lng: float


@dataclass
class Cafe:
    name: str
    address: str
    coordinates: Coordinates
    rating: Optional[float] = None
    opened_date: Optional[str] = None
    place_id: Optional[str] = None
    tags: list[str] = field(default_factory=list)

    def display(self, rank: int) -> str:
        parts = [f"{rank}. {self.name} — {self.address}"]
        if self.opened_date:
            parts.append(f"(Opened: {self.opened_date})")
        if self.rating is not None:
            parts.append(f"★ {self.rating}")
        return " ".join(parts)
