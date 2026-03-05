from PyQt6.QtWidgets import QLabel, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor

from app.styles import FIELD_LABEL_STYLE


def add_shadow(widget):
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(20)
    shadow.setXOffset(0)
    shadow.setYOffset(4)
    shadow.setColor(QColor(0, 0, 0, 30))
    widget.setGraphicsEffect(shadow)


def make_field_label(text):
    label = QLabel(text)
    label.setStyleSheet(FIELD_LABEL_STYLE)
    return label
