import time
import signal
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import MYSQL_CONFIG, SERVER_ID, API_URL, OFFSET_FILE
from offset_manager import load_offset, save_offset
from src.adapters.mysql_reader import MySQLBinlogReader
from src.adapters.kafka_sink import ConsoleSink
from src.core.processor import CDCProcessor
from src.adapters.file_sink import FileSink

class App:
    def __init__(self):
        self.running = True
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)

        # 1. Load State
        log_file, log_pos = load_offset(OFFSET_FILE)
        
        # 2. Initialize Adapters (The "Plug-ins")
        self.reader = MySQLBinlogReader(MYSQL_CONFIG, SERVER_ID, {"file": log_file, "pos": log_pos})
        # self.sink = ConsoleSink()
        self.sink = FileSink("data/events.jsonl")
        
        # 3. Initialize Core Logic
        self.processor = CDCProcessor(self.sink)

    def shutdown(self, signum, frame):
        print("\nGraceful shutdown initiated...")
        self.running = False

    def run(self):
        print("🚀 Pipeline Active...")
        try:
            for event in self.reader.fetch_events(self):
                if not self.running: break
                
                # Process the data
                self.processor.process_row(
                    event['type'], event['schema'], event['table'], event['data']
                )

                # Update offset in memory/file
                save_offset(OFFSET_FILE, event['log_file'], event['log_pos'])
                
        except Exception as e:
            print(f"Critical Error: {e}")
        finally:
            self.reader.close()
            print("Fetching complete!. ")
            sys.exit(0)

if __name__ == "__main__":
    app = App()
    app.run()