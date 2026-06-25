from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QGroupBox
import os
from tinysecurity.services.crypto_service import CryptoService
from tinysecurity.services.audit_service import AuditService

class CryptoPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        box = QGroupBox("Mã hóa / Giải mã File dữ liệu (Tự định vị nơi lưu)")
        grid = QVBoxLayout()

        self.txt_file = QLineEdit()
        btn_browse = QPushButton("Duyệt...")
        btn_browse.clicked.connect(self.browse_file)
        
        self.txt_pass = QLineEdit()
        self.txt_pass.setEchoMode(QLineEdit.EchoMode.Password)
        
        btn_enc = QPushButton("Mã hóa & Định vị nơi lưu...")
        btn_dec = QPushButton("Giải mã & Định vị nơi lưu...")
        btn_enc.clicked.connect(lambda: self.process_crypto(is_encrypt=True))
        btn_dec.clicked.connect(lambda: self.process_crypto(is_encrypt=False))

        h1 = QHBoxLayout()
        h1.addWidget(QLabel("Chọn File nguồn:"))
        h1.addWidget(self.txt_file)
        h1.addWidget(btn_browse)
        
        h2 = QHBoxLayout()
        h2.addWidget(QLabel("Nhập Mật khẩu:"))
        h2.addWidget(self.txt_pass)

        h3 = QHBoxLayout()
        h3.addWidget(btn_enc)
        h3.addWidget(btn_dec)

        grid.addLayout(h1)
        grid.addLayout(h2)
        grid.addLayout(h3)
        box.setLayout(grid)
        layout.addWidget(box)
        self.setLayout(layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file nguồn cần xử lý")
        if file_path:
            self.txt_file.setText(file_path)

    def process_crypto(self, is_encrypt):
        src = self.txt_file.text()
        pwd = self.txt_pass.text()
        if not src or not pwd:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn file nguồn và nhập mật khẩu!")
            return
            
        if is_encrypt:
            dest, _ = QFileDialog.getSaveFileName(self, "Chọn nơi lưu file sau khi mã hóa", src + ".tinyEnc")
        else:
            suggested = src.replace(".tinyEnc", "") if src.endswith(".tinyEnc") else src + ".decrypted"
            dest, _ = QFileDialog.getSaveFileName(self, "Chọn nơi lưu file sạch sau giải mã", suggested)
            
        if dest: 
            try:
                if is_encrypt:
                    CryptoService.encrypt_file(src, dest, pwd)
                    AuditService.log_event("Mật mã", f"Mã hóa file lưu tại {dest}", "Thành công")
                else:
                    CryptoService.decrypt_file(src, dest, pwd)
                    AuditService.log_event("Mật mã", f"Giải mã file lưu tại {dest}", "Thành công")
                QMessageBox.information(self, "Thành công", f"Thao tác hoàn tất!\nFile lưu tại: {dest}")
            except Exception as e:
                AuditService.log_event("Mật mã", "Lỗi xử lý file nhị phân", "Thất bại")
                QMessageBox.critical(self, "Lỗi mã hóa/giải mã", f"Chi tiết: {str(e)}")