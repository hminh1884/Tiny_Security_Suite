from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QGroupBox
from tinysecurity.services.network_service import NetworkService
from tinysecurity.services.audit_service import AuditService

class NetworkPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        vpn_box = QGroupBox("Kết nối mạng riêng ảo (OpenVPN)")
        v1 = QVBoxLayout()
        self.txt_ovpn = QLineEdit()
        btn_browse_vpn = QPushButton("Chọn file .ovpn...")
        btn_browse_vpn.clicked.connect(self.browse_ovpn)
        btn_start_vpn = QPushButton("Khởi động VPN Tunnel")
        btn_start_vpn.clicked.connect(self.start_vpn)
        
        h1 = QHBoxLayout()
        h1.addWidget(self.txt_ovpn)
        h1.addWidget(btn_browse_vpn)
        v1.addLayout(h1)
        v1.addWidget(btn_start_vpn)
        vpn_box.setLayout(v1)

        tor_box = QGroupBox("Duyệt web ẩn danh (Tor Browser)")
        v2 = QVBoxLayout()
        self.txt_tor = QLineEdit("C:\\Users\\Public\\Desktop\\Tor Browser\\Browser\\firefox.exe") # Đường dẫn mặc định
        btn_launch_tor = QPushButton("Khởi chạy Tor Browser")
        btn_launch_tor.clicked.connect(self.launch_tor)
        
        v2.addWidget(QLabel("Đường dẫn thực thi Tor:"))
        v2.addWidget(self.txt_tor)
        v2.addWidget(btn_launch_tor)
        tor_box.setLayout(v2)

        layout.addWidget(vpn_box)
        layout.addWidget(tor_box)
        self.setLayout(layout)

    def browse_ovpn(self):
        file, _ = QFileDialog.getOpenFileName(self, "Chọn cấu hình OpenVPN", "", "VPN Files (*.ovpn)")
        if file: self.txt_ovpn.setText(file)

    def start_vpn(self):
        try:
            NetworkService.start_openvpn(self.txt_ovpn.text())
            AuditService.log_event("Mạng", "Kích hoạt OpenVPN", "Thành công")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

    def launch_tor(self):
        try:
            NetworkService.launch_tor(self.txt_tor.text())
            AuditService.log_event("Mạng", "Mở trình duyệt Tor", "Thành công")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))