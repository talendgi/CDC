MYSQL_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "passwd": "Andorokta!321"
}

SERVER_ID = 100  


ONLY_DATABASES = ["e_commerce"]
ONLY_TABLES = ["customers"]

OFFSET_FILE = "offsets.json"

# Sink config
SINK_TYPE = "file"   

API_URL = "http://localhost:8000/events"