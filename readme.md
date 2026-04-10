
```text
config.py        → configuration (DB, filters, sink)
offset_manager   → remembers last processed position
cdc_pipeline.py  → main engine (reads + processes events)
```

---

# 📦 1. `config.py` — Central Configuration

```python
MYSQL_CONFIG = {...}
SERVER_ID = 100
ONLY_DATABASES = ["test_db"]
ONLY_TABLES = ["customers"]
OFFSET_FILE = "offsets.json"
SINK_TYPE = "file"
API_URL = "http://localhost:8000/events"
```

---

```python
{
  "host": "localhost",
  "port": 3306,
  "user": "cdc_user",
  "passwd": "cdc_pass"
}
```

👉 Used to **connect to MySQL binlog**

---

### ✅ `SERVER_ID`

👉 Unique ID for this CDC client

* MySQL treats your script like a **replication slave**
* Must be unique (or connection fails)

---

### ✅ Filters

```python
ONLY_DATABASES = ["test_db"]
ONLY_TABLES = ["customers"]
```

👉 Limits CDC to:

* specific database
* specific tables

💡 Without this → you get ALL DB changes

---

### ✅ `OFFSET_FILE`

```python
offsets.json
```

👉 Stores:

```json
{
  "log_file": "mysql-bin.000001",
  "log_pos": 12345
}
```

👉 Used for:

```text
Resume from last processed event
```

---

### ✅ Sink Config

```python
SINK_TYPE = "file"  # or "api"
```

👉 Defines **where events go**

---

# 💾 2. `offset_manager.py` — State Management

---

## 🔹 `load_offset()`

```python
def load_offset(file_path):
```

👉 Reads last processed position

---

### If file exists:

```python
return log_file, log_pos
```

### If not:

```python
return None, None
```

👉 Meaning:

```text
Start from latest binlog
```

---

## 🔹 `save_offset()`

```python
def save_offset(file_path, log_file, log_pos):
```

👉 Saves position after processing events

---

### Why this is CRITICAL

Without this:

❌ Restart → duplicate data
❌ Crash → data inconsistency

With this:

✅ Exactly-once-ish behavior
✅ Safe recovery

---

# 🚀 3. `cdc_pipeline.py` — Main Engine

This is the **heart of your system**

---

## 🔹 Imports

```python
from pymysqlreplication import BinLogStreamReader
```

👉 Core component:

```text
Reads MySQL binlog in real-time
```

---

## 🔹 Event Types

```python
WriteRowsEvent   → INSERT
UpdateRowsEvent  → UPDATE
DeleteRowsEvent  → DELETE
```

---

## 🔹 `serialize()`

```python
def serialize(obj):
```

👉 Converts:

* datetime → string

💡 Needed because:

```text
JSON cannot serialize datetime by default
```

---

## 🔹 `send_to_sink()`

```python
def send_to_sink(payload):
```

👉 Sends data to destination

---

### Option 1: File

```python
with open("cdc_output.json", "a") as f:
```

👉 Appends events line-by-line

---

### Option 2: API

```python
requests.post(API_URL, json=payload)
```

👉 Sends events to external service

---

## 🔹 `process_event()`

```python
def process_event(event_type, schema, table, data):
```

👉 Standardizes all events into one format

---

### Output structure:

```json
{
  "event_type": "INSERT",
  "schema": "test_db",
  "table": "customers",
  "data": {...},
  "ts": "timestamp"
}
```

---

### Why this is important

👉 Makes downstream processing easy:

* ML
* APIs
* dashboards
* RAG

---

## 🔹 `run()` — Core Streaming Logic

---

### Step 1: Load Offset

```python
log_file, log_pos = load_offset(OFFSET_FILE)
```

👉 Resume from last position

---

### Step 2: Create Stream

```python
stream = BinLogStreamReader(...)
```

---

### Key parameters:

#### ✅ `blocking=True`

```text
Wait for new events (real-time)
```

---

#### ✅ `resume_stream=True`

```text
Continue from last position
```

---

#### ✅ `only_schemas / only_tables`

```text
Filter data
```

---

#### ✅ `only_events`

```text
Only INSERT, UPDATE, DELETE
```

---

## 🔁 Step 3: Infinite Loop

```python
for event in stream:
```

👉 This is:

```text
Continuous streaming loop
```

---

## 🔄 Step 4: Process Each Event

---

### INSERT

```python
row["values"]
```

---

### UPDATE

```python
{
  "before": row["before_values"],
  "after": row["after_values"]
}
```

---

### DELETE

```python
row["values"]
```

---

## 💾 Step 5: Save Offset

```python
save_offset(OFFSET_FILE, stream.log_file, stream.log_pos)
```

👉 Happens after each batch

---

## 🛑 Error Handling

```python
except KeyboardInterrupt:
```

👉 Graceful shutdown

---

## 🔁 Auto Restart

```python
while True:
    try:
        run()
```

👉 If crash:

```text
Wait 5 sec → restart
```

---

# 🔥 End-to-End Flow

---

## 🧪 Example

### You run:

```bash
python cdc_pipeline.py
```

---

### Then MySQL:

```sql
INSERT INTO customers VALUES (1, 'John');
```

---

## Internally:

1. MySQL writes to binlog
2. `BinLogStreamReader` reads it
3. Event detected → `WriteRowsEvent`
4. `process_event()` formats it
5. `send_to_sink()` outputs it
6. Offset saved

---

# ⚡ Key Concepts You Just Implemented

---

## 🧠 1. CDC (Change Data Capture)

Capture DB changes in real time

---

## 🧠 2. Streaming

```text
Continuous data flow (not batch)
```

---

## 🧠 3. Offset Management

```text
Checkpoint system for recovery
```

---

## 🧠 4. Event-Driven Architecture

```text
Everything reacts to events
```

---

# 🎯 Why This Is Powerful

You just built:

```text
A mini Kafka-like CDC system — in pure Python
```

---

# 🚀 What You Can Add Next

If you want to go advanced:

* Kafka integration (later)
* FastAPI ingestion
* Redis queue
* Delta Lake
* Vector DB (RAG auto update)

---

# 👉 If You Want Next

Say:

👉 **“add fastapi consumer + dashboard”**

and I’ll turn this into a full real-time system 🔥
