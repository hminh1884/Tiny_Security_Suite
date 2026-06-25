import os
from datetime import datetime

class AuditService:
    LOG_FILE = "logs/security_audit.log"

    @staticmethod
    def log_event(module_name, action, status):
        if not os.path.exists("logs"):
            os.makedirs("logs")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{module_name}] {action} -> {status}\n"
        with open(AuditService.LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)

    @staticmethod
    def read_logs():
        if not os.path.exists(AuditService.LOG_FILE):
            return "Chưa có dữ liệu log an ninh."
        with open(AuditService.LOG_FILE, "r", encoding="utf-8") as f:
            return f.read()