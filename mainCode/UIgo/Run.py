from PyQt5.QtWidgets import QApplication
from mainCode.UIgo.loginClass import login
import sys


def run():
    app = QApplication(sys.argv)
    login_window = login()
    login_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()
