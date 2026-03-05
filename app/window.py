from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QTabWidget
)
from PyQt6.QtCore import Qt

from app.styles import STYLE_SHEET
from app.tab_print import PrintTab
from app.tab_pdf import PdfTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Numéroteur")
        self.setMinimumSize(700, 650)
        self.resize(780, 720)
        self.setStyleSheet(STYLE_SHEET)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(24, 18, 24, 18)
        main_layout.setSpacing(12)

        # Header
        title = QLabel("PDF Numéroteur")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        subtitle = QLabel("Numérotez, imprimez et numérisez vos pages facilement")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle)

        # Tabs
        tabs = QTabWidget()
        tabs.addTab(PrintTab(), "Impression")
        tabs.addTab(PdfTab(), "PDF Existant")
        main_layout.addWidget(tabs)
