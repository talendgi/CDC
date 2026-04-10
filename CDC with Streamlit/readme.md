# 🚀 Production-Grade MySQL CDC Pipeline

A high-performance, resilient Change Data Capture (CDC) pipeline built with Python. This system mimics a MySQL replica to stream database changes in real-time into a JSON Lines (JSONL) format, visualized by a professional dark-mode dashboard.

---
## to capture the evetns and store in json

    python cdc_pipeline\main.py

## To open the dashboard

    streamlit run cdc_pipeline\dashboard.py

```text
cdc_pipeline/
├── data/                  # Stores the JSONL stream and offsets
├── src/
│   ├── adapters/          # External interfaces (MySQL Reader, File Sink)
│   ├── core/              # Business logic & Domain models (Event schemas)
│   ├── interfaces/        # Abstract base classes (Enforcing contracts)
│   └── main.py            # Application entry point & Dependency Injection
├── dashboard.py           # Streamlit-based dashboard Monitor
├── config.py              # Environment-based configuration
└── offset_manager.py      # Persistence logic for Binlog positions