import os

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QSpinBox, QComboBox, QGroupBox, QProgressBar, QMessageBox
)
from PyQt6.QtCore import Qt

from PyPDF2 import PdfReader

from app.utils import add_shadow, make_field_label
from app.workers import NumberingWorker


class PdfTab(QWidget):
    """Onglet : Numéroter un PDF existant."""

    def __init__(self):
        super().__init__()
        self.input_file = None
        self.worker = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(18)

        # Fichier
        file_group = QGroupBox("Fichier PDF source")
        file_layout = QVBoxLayout(file_group)
        file_layout.setSpacing(10)

        self.select_btn = QPushButton("Cliquez ici pour sélectionner un fichier PDF")
        self.select_btn.setObjectName("selectFileBtn")
        self.select_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.select_btn.clicked.connect(self.select_file)
        file_layout.addWidget(self.select_btn)

        self.file_label = QLabel("Aucun fichier sélectionné")
        self.file_label.setObjectName("fileLabel")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        file_layout.addWidget(self.file_label)

        add_shadow(file_group)
        layout.addWidget(file_group)

        # Plage
        range_group = QGroupBox("Plage de numérotation")
        range_layout = QHBoxLayout(range_group)
        range_layout.setSpacing(24)

        col1 = QVBoxLayout()
        col1.addWidget(make_field_label("Page début"))
        self.start_spin = QSpinBox()
        self.start_spin.setMinimum(1)
        self.start_spin.setMaximum(9999)
        self.start_spin.setValue(1)
        col1.addWidget(self.start_spin)
        range_layout.addLayout(col1)

        col2 = QVBoxLayout()
        col2.addWidget(make_field_label("Page fin"))
        self.end_spin = QSpinBox()
        self.end_spin.setMinimum(1)
        self.end_spin.setMaximum(9999)
        self.end_spin.setValue(1)
        col2.addWidget(self.end_spin)
        range_layout.addLayout(col2)

        add_shadow(range_group)
        layout.addWidget(range_group)

        # Options
        options_group = QGroupBox("Options")
        options_layout = QHBoxLayout(options_group)
        options_layout.setSpacing(24)

        col_pos = QVBoxLayout()
        col_pos.addWidget(make_field_label("Position du numéro"))
        self.position_combo = QComboBox()
        self.position_combo.addItems(["Gauche", "Centre", "Droite"])
        self.position_combo.setCurrentIndex(1)
        col_pos.addWidget(self.position_combo)
        options_layout.addLayout(col_pos)

        col_font = QVBoxLayout()
        col_font.addWidget(make_field_label("Taille police"))
        self.font_spin = QSpinBox()
        self.font_spin.setMinimum(6)
        self.font_spin.setMaximum(72)
        self.font_spin.setValue(12)
        col_font.addWidget(self.font_spin)
        options_layout.addLayout(col_font)

        col_margin = QVBoxLayout()
        col_margin.addWidget(make_field_label("Marge haut (mm)"))
        self.margin_spin = QSpinBox()
        self.margin_spin.setMinimum(5)
        self.margin_spin.setMaximum(100)
        self.margin_spin.setValue(15)
        col_margin.addWidget(self.margin_spin)
        options_layout.addLayout(col_margin)

        add_shadow(options_group)
        layout.addWidget(options_group)

        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Bouton
        self.apply_btn = QPushButton("Appliquer la numérotation")
        self.apply_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.apply_btn.setMinimumHeight(50)
        self.apply_btn.setEnabled(False)
        self.apply_btn.clicked.connect(self.apply_numbering)
        layout.addWidget(self.apply_btn)

        layout.addStretch()

    def select_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Sélectionner un fichier PDF", "", "Fichiers PDF (*.pdf)")
        if not path:
            return
        self.input_file = path
        try:
            reader = PdfReader(path)
            total = len(reader.pages)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de lire le fichier :\n{e}")
            return
        self.file_label.setText(f"{os.path.basename(path)}  ({total} pages)")
        self.start_spin.setMaximum(total)
        self.end_spin.setMaximum(total)
        self.end_spin.setValue(total)
        self.apply_btn.setEnabled(True)

    def apply_numbering(self):
        if not self.input_file:
            QMessageBox.warning(self, "Attention", "Veuillez d'abord sélectionner un fichier PDF.")
            return
        start = self.start_spin.value()
        end = self.end_spin.value()
        if start > end:
            QMessageBox.warning(self, "Plage invalide",
                                "La page de début doit être inférieure ou égale à la page de fin.")
            return

        output_path, _ = QFileDialog.getSaveFileName(
            self, "Enregistrer le PDF numéroté", "", "Fichiers PDF (*.pdf)")
        if not output_path:
            return
        if not output_path.lower().endswith(".pdf"):
            output_path += ".pdf"

        self.apply_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        self.worker = NumberingWorker(
            self.input_file, output_path, start, end,
            self.position_combo.currentText().lower(),
            self.font_spin.value(), self.margin_spin.value()
        )
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_finished(self, output_path):
        self.progress_bar.setValue(100)
        self.apply_btn.setEnabled(True)
        QMessageBox.information(self, "Succès",
            f"Le fichier a été numéroté avec succès !\n\nEnregistré sous :\n{output_path}")
        self.progress_bar.setVisible(False)

    def on_error(self, message):
        self.apply_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        QMessageBox.critical(self, "Erreur", f"Une erreur est survenue :\n{message}")
