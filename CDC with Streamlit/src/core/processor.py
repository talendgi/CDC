from src.interfaces.sink import EventSink
from src.core.event_models import CDCEvent

class CDCProcessor:
    def __init__(self, sink: EventSink):
        self.sink = sink

    def process_row(self, event_type: str, schema: str, table: str, row_data: dict):
        # Business Logic / Data Cleaning goes here
        event = CDCEvent(
            event_type=event_type,
            schema=schema,
            table=table,
            data=row_data
        )
        self.sink.send(event.to_dict())