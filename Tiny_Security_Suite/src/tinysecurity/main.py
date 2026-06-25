import sys
from PySide6.QtWidgets import QApplication
from tinysecurity.ui.auth_window import AuthWindow

def main():
    app = QApplication(sys.argv)
    
    auth = AuthWindow()
    auth.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()