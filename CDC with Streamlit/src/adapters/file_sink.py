import json
import os
from src.interfaces.sink import EventSink

class FileSink(EventSink):
    def __init__(self, filename="data/events.jsonl"):
        self.filename = filename
        # NEW: Automatically create the directory if it's missing
        directory = os.path.dirname(self.filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")

    def serialize(self, obj):
        import datetime
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        return obj

    def send(self, payload: dict):
        try:
            with open(self.filename, "a", encoding="utf-8") as f:
                json_line = json.dumps(payload, default=self.serialize)
                f.write(json_line + "\n")
                print(f"📌 DEBUG SINK: {payload}")
        except Exception as e:
            print(f"❌ Error writing to file sink: {e}")

    def send_batch(self, payloads: list[dict]):
        for p in payloads:
            self.send(p)
            
