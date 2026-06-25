from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QGroupBox
from tinysecurity.services.folder_service import FolderService
from tinysecurity.services.audit_service import AuditService

class FolderPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        box = QGroupBox("Thư mục bảo mật (Secure Folder)")
        vbox = QVBoxLayout()

        self.txt_folder = QLineEdit()
        btn_browse = QPushButton("Chọn Thư Mục...")
        btn_browse.clicked.connect(self.browse_folder)

        btn_hide = QPushButton("Ẩn Thư Mục")
        btn_unhide = QPushButton("Hiện Thư Mục")
        btn_hide.clicked.connect(lambda: self.toggle_folder(True))
        btn_unhide.clicked.connect(lambda: self.toggle_folder(False))

        h1 = QHBoxLayout()
        h1.addWidget(QLabel("Đường dẫn:"))
        h1.addWidget(self.txt_folder)
        h1.addWidget(btn_browse)

        h2 = QHBoxLayout()
        h2.addWidget(btn_hide)
        h2.addWidget(btn_unhide)

        vbox.addLayout(h1)
        vbox.addLayout(h2)
        box.setLayout(vbox)
        layout.addWidget(box)
        self.setLayout(layout)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Chọn thư mục")
        if folder:
            self.txt_folder.setText(folder)

    def toggle_folder(self, should_hide):
        path = self.txt_folder.text()
        if not path: return
        try:
            if should_hide:
                FolderService.hide_folder(path)
                AuditService.log_event("Folder", f"Ẩn {path}", "Thành công")
            else:
                FolderService.unhide_folder(path)
                AuditService.log_event("Folder", f"Hiện {path}", "Thành công")
            QMessageBox.information(self, "Thông báo", "Thao tác trên hệ thống hoàn tất!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))