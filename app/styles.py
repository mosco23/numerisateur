STYLE_SHEET = """
QMainWindow {
    background-color: #f0f2f5;
}

QTabWidget::pane {
    border: none;
    background-color: #f0f2f5;
}

QTabBar::tab {
    background-color: #e0e0e0;
    color: #555;
    border: none;
    padding: 14px 32px;
    font-size: 14px;
    font-weight: bold;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    margin-right: 4px;
    min-width: 140px;
}

QTabBar::tab:selected {
    background-color: white;
    color: #6c63ff;
}

QTabBar::tab:hover:!selected {
    background-color: #d0d0d0;
}

QGroupBox {
    background-color: white;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    margin-top: 10px;
    padding: 28px 16px 14px 16px;
    font-size: 14px;
    font-weight: bold;
    color: #1a1a2e;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 16px;
    top: 4px;
    padding: 0 6px;
    background-color: white;
    color: #6c63ff;
    font-size: 14px;
}

QPushButton {
    background-color: #6c63ff;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 28px;
    font-size: 14px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #5a52d5;
}

QPushButton:pressed {
    background-color: #4a43b5;
}

QPushButton:disabled {
    background-color: #b0b0b0;
}

QPushButton#selectFileBtn, QPushButton#selectFolderBtn {
    background-color: #e8e6ff;
    color: #6c63ff;
    border: 2px dashed #6c63ff;
    padding: 24px;
    font-size: 15px;
    border-radius: 12px;
}

QPushButton#selectFileBtn:hover, QPushButton#selectFolderBtn:hover {
    background-color: #d8d5ff;
}

QPushButton#scanBtn {
    background-color: #10b981;
    font-size: 15px;
}

QPushButton#scanBtn:hover {
    background-color: #059669;
}

QPushButton#scanBtn:disabled {
    background-color: #b0b0b0;
}

QPushButton#stopBtn {
    background-color: #ef4444;
}

QPushButton#stopBtn:hover {
    background-color: #dc2626;
}

QLabel#fileLabel, QLabel#folderLabel {
    color: #555;
    font-size: 13px;
    padding: 10px;
    background-color: #f8f8ff;
    border-radius: 6px;
    border: 1px solid #e0e0e0;
}

QLabel#titleLabel {
    color: #1a1a2e;
    font-size: 24px;
    font-weight: bold;
}

QLabel#subtitleLabel {
    color: #888;
    font-size: 13px;
}

QSpinBox {
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 15px;
    background-color: white;
    color: #1a1a2e;
    min-height: 20px;
}

QSpinBox:focus {
    border-color: #6c63ff;
}

QComboBox {
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 15px;
    background-color: white;
    color: #1a1a2e;
    min-height: 20px;
}

QComboBox:focus {
    border-color: #6c63ff;
}

QComboBox::drop-down {
    border: none;
    padding-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: white;
    color: #1a1a2e;
    selection-background-color: #6c63ff;
    selection-color: white;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    padding: 4px;
    font-size: 15px;
}

QComboBox QAbstractItemView::item {
    padding: 8px 14px;
    min-height: 32px;
}

QProgressBar {
    border: none;
    border-radius: 6px;
    background-color: #e8e6ff;
    text-align: center;
    font-size: 12px;
    font-weight: bold;
    color: #6c63ff;
    min-height: 14px;
    max-height: 14px;
}

QProgressBar::chunk {
    background-color: #6c63ff;
    border-radius: 6px;
}
"""

FIELD_LABEL_STYLE = "font-weight: bold; color: #444; font-size: 13px; padding-bottom: 2px;"
