from dataclasses import dataclass, asdict
from datetime import datetime, timezone

@dataclass
class CDCEvent:
    event_type: str
    schema: str
    table: str
    data: dict
    timestamp: str = None

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_dict(self):
        return asdict(self)