from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit, QMessageBox, QGroupBox
from tinysecurity.services.firewall_service import FirewallService
from tinysecurity.services.audit_service import AuditService

class FirewallPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        box_status = QGroupBox("Giám sát Windows Tường lửa")
        v1 = QVBoxLayout()
        self.txt_log = QTextEdit()
        self.txt_log.setReadOnly(True)
        btn_status = QPushButton("Kiểm tra trạng thái cấu hình hệ thống")
        btn_status.clicked.connect(self.view_status)
        v1.addWidget(self.txt_log)
        v1.addWidget(btn_status)
        box_status.setLayout(v1)

        box_rule = QGroupBox("Quản lý Luật Chặn Cổng (Yêu cầu quyền Admin)")
        h1 = QHBoxLayout()
        self.txt_rule_name = QLineEdit()
        self.txt_rule_name.setPlaceholderText("Tên luật")
        self.txt_port = QLineEdit()
        self.txt_port.setPlaceholderText("Số cổng chặn TCP (VD: 445)")
        btn_add = QPushButton("Áp dụng Luật Chặn")
        btn_add.clicked.connect(self.add_rule)
        h1.addWidget(self.txt_rule_name)
        h1.addWidget(self.txt_port)
        h1.addWidget(btn_add)
        box_rule.setLayout(h1)

        layout.addWidget(box_status)
        layout.addWidget(box_rule)
        self.setLayout(layout)

    def view_status(self):
        self.txt_log.setText(FirewallService.get_status())
        AuditService.log_event("Tường lửa", "Truy vấn cấu hình", "Thành công")

    def add_rule(self):
        name = self.txt_rule_name.text()
        port = self.txt_port.text()
        if not name or not port: return
        try:
            FirewallService.add_block_rule(name, port)
            AuditService.log_event("Tường lửa", f"Thêm rule chặn cổng {port}", "Thành công")
            QMessageBox.information(self, "Thành công", f"Đã thực thi luật chặn cổng {port} xuống hệ thống Windows!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", "Thất bại. Hãy chạy VS Code dưới quyền Administrator!")