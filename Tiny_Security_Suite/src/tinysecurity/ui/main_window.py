from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QListWidget, QStackedWidget
from tinysecurity.ui.crypto_panel import CryptoPanel
from tinysecurity.ui.shredder_panel import ShredderPanel
from tinysecurity.ui.folder_panel import FolderPanel
from tinysecurity.ui.network_panel import NetworkPanel
from tinysecurity.ui.firewall_panel import FirewallPanel
from tinysecurity.ui.audit_panel import AuditPanel

class MainWindow(QMainWindow):
    def __init__(self, logged_in_email: str = "admin@tinysecurity.local"):
        super().__init__()
        self.logged_in_email = logged_in_email
        self.setWindowTitle("Tiny Security Suite - Học viện Kỹ thuật Mật mã [2026]")
        self.resize(800, 500)

        main_widget = QWidget()
        layout = QHBoxLayout()

        self.menu_list = QListWidget()
        self.menu_list.setFixedWidth(180)
        self.menu_list.addItems([
            "Mã hóa File (AES)", 
            "Hủy dữ liệu (Shredder)", 
            "Thư mục bảo mật", 
            "Mạng (VPN/Tor)", 
            "Tường lửa (Firewall)",
            "Nhật ký hệ thống"
        ])

        self.stacked_pages = QStackedWidget()
        self.stacked_pages.addWidget(CryptoPanel())
        self.stacked_pages.addWidget(ShredderPanel())
        self.stacked_pages.addWidget(FolderPanel())
        self.stacked_pages.addWidget(NetworkPanel())
        self.stacked_pages.addWidget(FirewallPanel())
        self.stacked_pages.addWidget(AuditPanel())

        self.menu_list.currentRowChanged.connect(self.stacked_pages.setCurrentIndex)

        layout.addWidget(self.menu_list)
        layout.addWidget(self.stacked_pages)
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)        
        self.show()