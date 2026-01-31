import datetime

class LoggingService:
    def __init__(self, log_file="logs/mcp.log"):
        self.log_file = log_file

    def log(self, message: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")