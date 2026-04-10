import os
from dotenv import load_dotenv

load_dotenv(override=True)
# MySQL Source Configuration
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "user": os.getenv("MYSQL_USER", "cdc_user"),
    "passwd": os.getenv("MYSQL_PASS", "password"),
    "read_timeout": 5
}

SERVER_ID = int(os.getenv("SERVER_ID", 100))

# Sink Configuration
SINK_TYPE = os.getenv("SINK_TYPE", "api") # 'api', 'kafka', or 'file'
API_URL = os.getenv("API_URL", "http://localhost:8080/webhook")

# File Paths
OFFSET_FILE = os.getenv("OFFSET_FILE", "binlog_offset.json")
