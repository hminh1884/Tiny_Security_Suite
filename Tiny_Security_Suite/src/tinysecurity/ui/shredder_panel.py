from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QSpinBox, QGroupBox
from tinysecurity.services.shredder_service import ShredderService
from tinysecurity.services.audit_service import AuditService

class ShredderPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        box = QGroupBox("Hủy dữ liệu an toàn (Shredder)")
        vbox = QVBoxLayout()

        self.txt_file = QLineEdit()
        btn_browse = QPushButton("Duyệt...")
        btn_browse.clicked.connect(self.browse_file)

        self.spin_passes = QSpinBox()
        self.spin_passes.setRange(1, 7)
        self.spin_passes.setValue(2)

        btn_shred = QPushButton("XÓA TẬN GỐC (SHRED)")
        btn_shred.setStyleSheet("background-color: red; color: white; font-weight: bold;")
        btn_shred.clicked.connect(self.run_shred)

        h1 = QHBoxLayout()
        h1.addWidget(QLabel("Chọn File:"))
        h1.addWidget(self.txt_file)
        h1.addWidget(btn_browse)

        h2 = QHBoxLayout()
        h2.addWidget(QLabel("Số vòng lặp ghi đè:"))
        h2.addWidget(self.spin_passes)

        vbox.addLayout(h1)
        vbox.addLayout(h2)
        vbox.addWidget(btn_shred)
        box.setLayout(vbox)
        layout.addWidget(box)
        self.setLayout(layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file cần hủy")
        if file_path:
            self.txt_file.setText(file_path)

    def run_shred(self):
        path = self.txt_file.text()
        if not path:
            return
        ans = QMessageBox.question(
            self, 
            "Xác nhận nguy hiểm", 
            "Dữ liệu sẽ bị phá hủy hoàn toàn. Bạn chắc chắn?", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if ans == QMessageBox.StandardButton.Yes:
            try:
                ShredderService.shred_file(path, self.spin_passes.value())
                AuditService.log_event("Shredder", f"Hủy file {path}", "Thành công")
                QMessageBox.information(self, "Thành công", "Đã hủy file vĩnh viễn!")
                self.txt_file.clear()
            except Exception as e:
                AuditService.log_event("Shredder", f"Hủy file {path}", "Thất bại")
                QMessageBox.critical(self, "Lỗi", str(e))