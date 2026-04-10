import requests
from src.interfaces.sink import EventSink

# class KafkaSink(EventSink):
#     def __init__(self, api_url):
#         self.api_url = api_url

#     def send(self, payload: dict):
#         try:
#             response = requests.post(self.api_url, json=payload, timeout=5)
#             response.raise_for_status()
#         except Exception as e:
#             print(f"Failed to send to API: {e}")

#     def send_batch(self, payloads: list[dict]):
#         # Implementation for bulk API calls
#         pass

class ConsoleSink(EventSink):
    def send(self, payload: dict):
        print(f"📌 DEBUG SINK: {payload}")

    def send_batch(self, payloads: list[dict]):
        pass