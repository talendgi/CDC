from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import WriteRowsEvent, UpdateRowsEvent, DeleteRowsEvent

class MySQLBinlogReader:
    def __init__(self, mysql_settings, server_id, offset):
        self.stream = BinLogStreamReader(
            connection_settings=mysql_settings,
            server_id=server_id,
            blocking=False,
            resume_stream=True,
            log_file=offset.get('file'),
            log_pos=offset.get('pos'),
            only_events=[WriteRowsEvent, UpdateRowsEvent, DeleteRowsEvent],
            slave_heartbeat=1   # Forces the stream to wake up every 1s
        )

    def fetch_events(self,app_state):
        for binlogevent in self.stream:
            
            if not app_state.running:
                break
            for row in binlogevent.rows:
                event_type = self._get_event_type(binlogevent)
                data = self._format_data(event_type, row)
                
                yield {
                    "type": event_type,
                    "schema": binlogevent.schema,
                    "table": binlogevent.table,
                    "data": data,
                    "log_file": self.stream.log_file,
                    "log_pos": self.stream.log_pos
                }

    def _get_event_type(self, event):
        if isinstance(event, WriteRowsEvent): return "INSERT"
        if isinstance(event, UpdateRowsEvent): return "UPDATE"
        if isinstance(event, DeleteRowsEvent): return "DELETE"
        return "UNKNOWN"

    def _format_data(self, event_type, row):
        if event_type == "UPDATE":
            return {"before": row["before_values"], "after": row["after_values"]}
        return row["values"]
    
    def close(self):
        self.stream.close()