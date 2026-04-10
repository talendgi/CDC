from abc import ABC, abstractmethod

class EventSink(ABC):
    @abstractmethod
    def send(self, payload: dict):
        """Send a single payload to the destination."""
        pass

    @abstractmethod
    def send_batch(self, payloads: list[dict]):
        """Send a batch of payloads for better throughput."""
        pass