from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import (
    DeleteRowsEvent,
    WriteRowsEvent,
    UpdateRowsEvent
)
import json
import datetime
import time
import requests
import sys
from config import *
from offset_manager import load_offset, save_offset


def serialize(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    return obj


def send_to_sink(payload):
    if SINK_TYPE == "file":
        with open("cdc_output.json", "a") as f:
            f.write(json.dumps(payload, default=serialize) + "\n")

    elif SINK_TYPE == "api":
        try:
            requests.post(API_URL, json=payload)
        except Exception as e:
            print("API error:", e)


def process_event(event_type, schema, table, data):
    payload = {
        "event_type": event_type,
        "schema": schema,
        "table": table,
        "data": data,
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

    print("📌 EVENT:", json.dumps(payload, default=serialize))
    send_to_sink(payload)


def run():
    log_file, log_pos = load_offset(OFFSET_FILE)

    stream = BinLogStreamReader(
        connection_settings=MYSQL_CONFIG,
        server_id=SERVER_ID,
        blocking=True,
        resume_stream=True,
        log_file=log_file,
        log_pos=log_pos,
        only_schemas=ONLY_DATABASES,
        only_tables=ONLY_TABLES,
        only_events=[WriteRowsEvent, UpdateRowsEvent, DeleteRowsEvent],
        freeze_schema=False,
        slave_heartbeat=1
    )

    print("🚀 CDC Pipeline Started...")

    try:
        for event in stream:
            for row in event.rows:

                if isinstance(event, WriteRowsEvent):
                    process_event("INSERT", event.schema, event.table, row["values"])

                elif isinstance(event, UpdateRowsEvent):
                    process_event("UPDATE", event.schema, event.table, {
                        "before": row["before_values"],
                        "after": row["after_values"]
                    })

                elif isinstance(event, DeleteRowsEvent):
                    process_event("DELETE", event.schema, event.table, row["values"])

            # Save offset after each batch
            save_offset(OFFSET_FILE, stream.log_file, stream.log_pos)

    except KeyboardInterrupt:
        print("🛑 Stopped by user")

    finally:
        stream.close()
        sys.exit(0)
        stream.close()


if __name__ == "__main__":
    while True:
        try:
            run()
        except Exception as e:
            print("⚠️ Error:", e)
            print("🔁 Restarting in 5 seconds...")
            time.sleep(5)