from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QGroupBox
from tinysecurity.services.audit_service import AuditService

class AuditPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        box = QGroupBox("Nhật ký kiểm toán an ninh hệ thống (Audit Trail)")
        vbox = QVBoxLayout()

        self.txt_logs = QTextEdit()
        self.txt_logs.setReadOnly(True)
        btn_refresh = QPushButton("Làm mới nhật ký")
        btn_refresh.clicked.connect(self.refresh_logs)

        vbox.addWidget(self.txt_logs)
        vbox.addWidget(btn_refresh)
        box.setLayout(vbox)
        layout.addWidget(box)
        self.setLayout(layout)
        self.refresh_logs()

    def refresh_logs(self):
        self.txt_logs.setText(AuditService.read_logs())