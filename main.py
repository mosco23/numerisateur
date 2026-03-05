import os
import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont, QIcon

from app.window import MainWindow

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    icon_path = os.path.join(BASE_DIR, "assets", "logo.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    font = QFont("Segoe UI", 10)
    font.setStyleHint(QFont.StyleHint.SansSerif)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
