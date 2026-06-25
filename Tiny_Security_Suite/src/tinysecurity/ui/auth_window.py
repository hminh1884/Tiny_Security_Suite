from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QStackedWidget
from PySide6.QtCore import Qt
from tinysecurity.services.auth_service import AuthService
from tinysecurity.ui.main_window import MainWindow

class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Xác thực hệ thống - Tiny Security Suite")
        self.resize(400, 350)
        
        self.stacked_layout = QStackedWidget()
        self.main_window_instance = None
        
        self.temp_reg_email = ""
        self.temp_reg_pwd = ""
        self.expected_email_otp = ""

        self.stacked_layout.addWidget(self.create_login_panel())
        self.stacked_layout.addWidget(self.create_register_panel())
        self.stacked_layout.addWidget(self.create_forgot_panel())
        self.stacked_layout.addWidget(self.create_reset_panel())
        self.stacked_layout.addWidget(self.create_email_verify_panel())
        
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_layout)
        self.setLayout(layout)
        
        self.check_auto_login()

    def check_auto_login(self):
        saved_user = AuthService.get_local_session()
        if saved_user:
            if AuthService.check_session_timeout(saved_user):
                AuthService.clear_local_session()
                QMessageBox.warning(self, "Phiên hết hạn", "Tài khoản của bạn đã không hoạt động quá 1 tháng.\nVui lòng đăng nhập lại!")
            else:
                AuthService.update_activity(saved_user)
                self.enter_main_app(saved_user)

    def create_login_panel(self) -> QWidget:
        widget = QWidget()
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("<b>ĐĂNG NHẬP HỆ THỐNG</b>"), alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.login_email = QLineEdit()
        self.login_email.setPlaceholderText("Nhập Email")
        self.login_pass = QLineEdit()
        self.login_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_pass.setPlaceholderText("Nhập Mật khẩu")
        
        btn_login = QPushButton("Đăng nhập & Ghi nhớ phiên")
        btn_login.clicked.connect(self.handle_login)
        btn_to_reg = QPushButton("Chưa có tài khoản? Đăng ký")
        btn_to_reg.clicked.connect(lambda: self.stacked_layout.setCurrentIndex(1))
        
        vbox.addWidget(self.login_email)
        vbox.addWidget(self.login_pass)
        vbox.addWidget(btn_login)
        vbox.addWidget(btn_to_reg)
        widget.setLayout(vbox)
        return widget

    def handle_login(self):
        email = self.login_email.text().strip()
        pwd = self.login_pass.text()
        if AuthService.login(email, pwd):
            AuthService.save_local_session(email)
            self.enter_main_app(email)
        else:
            QMessageBox.critical(self, "Thất bại", "Sai Email hoặc Mật khẩu đăng nhập!")

    def enter_main_app(self, email: str):
        self.close()
        self.main_window_instance = MainWindow(email)
        self.main_window_instance.show()

    def create_register_panel(self) -> QWidget:
        widget = QWidget()
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("<b>ĐĂNG KÝ TÀI KHOẢN MỚI</b>"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.reg_email = QLineEdit()
        self.reg_pass = QLineEdit()
        self.reg_pass.setEchoMode(QLineEdit.EchoMode.Password)
        btn_reg = QPushButton("Gửi mã xác thực về Email")
        btn_reg.clicked.connect(self.handle_pre_register)
        btn_back = QPushButton("Quay lại")
        btn_back.clicked.connect(lambda: self.stacked_layout.setCurrentIndex(0))
        vbox.addWidget(QLabel("Email:"))
        vbox.addWidget(self.reg_email)
        vbox.addWidget(QLabel("Mật khẩu:"))
        vbox.addWidget(self.reg_pass)
        vbox.addWidget(btn_reg)
        vbox.addWidget(btn_back)
        widget.setLayout(vbox)
        return widget

    def handle_pre_register(self):
        email = self.reg_email.text().strip()
        pwd = self.reg_pass.text()
        if not email or not pwd: return
        if AuthService.is_temp_mail(email):
            QMessageBox.critical(self, "Bị chặn", "Không dùng Temp Mail!")
            return
        try:
            self.temp_reg_email = email
            self.temp_reg_pwd = pwd
            self.expected_email_otp = AuthService.generate_email_otp()
            print(f"--- [DEBUG OTP EMAIL]: {self.expected_email_otp} ---") 
            QMessageBox.information(self, "Thành công", "Đã cấp mã kích hoạt (Hãy check mail hoặc Console VS Code)!")
            self.stacked_layout.setCurrentIndex(4)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", str(e))

    def create_email_verify_panel(self) -> QWidget:
        widget = QWidget()
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("<b>XÁC THỰC KÍCH HOẠT EMAIL</b>"), alignment=Qt.AlignmentFlag.AlignCenter)
        self.txt_otp = QLineEdit()
        self.txt_otp.setPlaceholderText("Nhập mã OTP 6 số")
        btn_confirm = QPushButton("Kích hoạt ngay")
        btn_confirm.clicked.connect(self.handle_final_register)
        vbox.addWidget(self.txt_otp)
        vbox.addWidget(btn_confirm)
        widget.setLayout(vbox)
        return widget

    def handle_final_register(self):
        if self.txt_otp.text().strip() == self.expected_email_otp:
            if AuthService.register(self.temp_reg_email, self.temp_reg_pwd):
                QMessageBox.information(self, "Thành công", "Đăng ký thành công! Mời bạn đăng nhập.")
                self.stacked_layout.setCurrentIndex(0)
        else:
            QMessageBox.critical(self, "Sai mã", "Mã kích hoạt không đúng!")

    def create_forgot_panel(self) -> QWidget: return QWidget()
    def create_reset_panel(self) -> QWidget: return QWidget()