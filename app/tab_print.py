import os
import tempfile

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QSpinBox, QComboBox, QGroupBox, QProgressBar, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

from app.utils import add_shadow, make_field_label
from app.workers import ScanWorker
from app.platform_utils import print_pdf


class PrintTab(QWidget):
    """Onglet : Imprimer les numéros puis numériser les feuilles."""

    def __init__(self):
        super().__init__()
        self.scan_folder = None
        self.scan_worker = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # Info
        info = QLabel(
            "Les feuilles sont dans l'imprimante.\n"
            "Les numéros seront imprimés en haut de chaque feuille, puis les feuilles seront numérisées."
        )
        info.setStyleSheet(
            "color: #6c63ff; font-size: 14px; padding: 16px; "
            "background-color: #f0eeff; border-radius: 10px; border: 1px solid #d8d5ff;"
        )
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setWordWrap(True)
        layout.addWidget(info)

        # Plage
        range_group = QGroupBox("Plage de numérotation")
        range_layout = QHBoxLayout(range_group)
        range_layout.setSpacing(24)

        col1 = QVBoxLayout()
        col1.addWidget(make_field_label("Numéro début"))
        self.start_spin = QSpinBox()
        self.start_spin.setMinimum(1)
        self.start_spin.setMaximum(9999)
        self.start_spin.setValue(1)
        col1.addWidget(self.start_spin)
        range_layout.addLayout(col1)

        col2 = QVBoxLayout()
        col2.addWidget(make_field_label("Numéro fin"))
        self.end_spin = QSpinBox()
        self.end_spin.setMinimum(1)
        self.end_spin.setMaximum(9999)
        self.end_spin.setValue(10)
        col2.addWidget(self.end_spin)
        range_layout.addLayout(col2)

        add_shadow(range_group)
        layout.addWidget(range_group)

        # Options d'impression
        options_group = QGroupBox("Options d'impression")
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

        # Options de numérisation
        scan_group = QGroupBox("Numérisation après impression")
        scan_layout = QHBoxLayout(scan_group)
        scan_layout.setSpacing(24)

        col_folder = QVBoxLayout()
        col_folder.addWidget(make_field_label("Dossier de destination"))
        folder_row = QHBoxLayout()
        self.folder_btn = QPushButton("Choisir...")
        self.folder_btn.setObjectName("selectFolderBtn")
        self.folder_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.folder_btn.clicked.connect(self.select_folder)
        self.folder_btn.setStyleSheet(
            "background-color: #e8e6ff; color: #6c63ff; border: 1px solid #6c63ff; "
            "padding: 8px 16px; font-size: 13px; border-radius: 6px; font-weight: bold;"
        )
        folder_row.addWidget(self.folder_btn)
        self.folder_label = QLabel("Aucun dossier")
        self.folder_label.setStyleSheet("color: #888; font-size: 12px; font-weight: normal;")
        folder_row.addWidget(self.folder_label, 1)
        col_folder.addLayout(folder_row)
        scan_layout.addLayout(col_folder)

        col_fmt = QVBoxLayout()
        col_fmt.addWidget(make_field_label("Format"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["PDF", "PNG", "JPEG"])
        col_fmt.addWidget(self.format_combo)
        scan_layout.addLayout(col_fmt)

        col_res = QVBoxLayout()
        col_res.addWidget(make_field_label("Résolution (DPI)"))
        self.res_combo = QComboBox()
        self.res_combo.addItems(["150", "200", "300", "600"])
        self.res_combo.setCurrentIndex(2)
        col_res.addWidget(self.res_combo)
        scan_layout.addLayout(col_res)

        add_shadow(scan_group)
        layout.addWidget(scan_group)

        # Progress
        self.progress_label = QLabel("")
        self.progress_label.setStyleSheet("color: #6c63ff; font-size: 13px; font-weight: bold;")
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_label.setVisible(False)
        layout.addWidget(self.progress_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Boutons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)

        self.print_btn = QPushButton("Imprimer et numériser")
        self.print_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.print_btn.setMinimumHeight(50)
        self.print_btn.clicked.connect(self.do_print_and_scan)
        btn_row.addWidget(self.print_btn)

        self.stop_btn = QPushButton("Arrêter")
        self.stop_btn.setObjectName("stopBtn")
        self.stop_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.stop_btn.setMinimumHeight(50)
        self.stop_btn.setVisible(False)
        self.stop_btn.clicked.connect(self.stop_scan)
        btn_row.addWidget(self.stop_btn)

        layout.addLayout(btn_row)
        layout.addStretch()

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Choisir le dossier de destination")
        if folder:
            self.scan_folder = folder
            display = folder if len(folder) <= 40 else "..." + folder[-37:]
            self.folder_label.setText(display)

    def do_print_and_scan(self):
        start = self.start_spin.value()
        end = self.end_spin.value()
        if start > end:
            QMessageBox.warning(self, "Plage invalide",
                                "Le numéro de début doit être inférieur ou égal au numéro de fin.")
            return

        if not self.scan_folder:
            QMessageBox.warning(self, "Dossier manquant",
                                "Veuillez choisir un dossier de destination pour la numérisation.")
            return

        position = self.position_combo.currentText().lower()
        font_size = self.font_spin.value()
        margin_top = self.margin_spin.value()

        # Générer le PDF de numérotation
        tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        tmp_path = tmp.name
        tmp.close()

        try:
            page_width, page_height = A4
            c_pdf = canvas.Canvas(tmp_path, pagesize=A4)
            for num in range(start, end + 1):
                c_pdf.setFont("Helvetica", font_size)
                text = str(num)
                tw = c_pdf.stringWidth(text, "Helvetica", font_size)
                y = page_height - margin_top * mm
                if position == "gauche":
                    x = 30 * mm
                elif position == "droite":
                    x = page_width - 30 * mm - tw
                else:
                    x = (page_width - tw) / 2
                c_pdf.drawString(x, y, text)
                c_pdf.showPage()
            c_pdf.save()

            # Dialogue d'impression natif (cross-platform)
            printer = QPrinter(QPrinter.Mode.HighResolution)
            dialog = QPrintDialog(printer, self)
            dialog.setWindowTitle("Imprimer la numérotation")
            if dialog.exec() != QPrintDialog.DialogCode.Accepted:
                return

            printer_name = printer.printerName()
            success, err = print_pdf(tmp_path, printer_name)
            if not success:
                QMessageBox.critical(self, "Erreur",
                    f"Erreur lors de l'impression :\n{err}")
                return
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

        # Lancer la numérisation
        QMessageBox.information(self, "Impression envoyée",
            f"Numérotation de {start} à {end} envoyée à l'imprimante.\n\n"
            "Récupérez les feuilles imprimées et placez-les dans le scanner.\n"
            "La numérisation va commencer.")

        self.start_scanning(start, end)

    def start_scanning(self, start, end):
        self.print_btn.setEnabled(False)
        self.stop_btn.setVisible(True)
        self.progress_bar.setVisible(True)
        self.progress_label.setVisible(True)
        self.progress_bar.setValue(0)

        self.scan_worker = ScanWorker(
            self.scan_folder, start, end,
            self.format_combo.currentText(),
            int(self.res_combo.currentText())
        )
        self.scan_worker.progress.connect(self.on_scan_progress)
        self.scan_worker.page_scanned.connect(self.on_page_scanned)
        self.scan_worker.finished.connect(self.on_scan_finished)
        self.scan_worker.error.connect(self.on_scan_error)
        self.scan_worker.start()

    def stop_scan(self):
        if self.scan_worker:
            self.scan_worker.stop()

    def on_scan_progress(self, current, total):
        self.progress_bar.setValue(int((current / total) * 100))
        self.progress_label.setText(
            f"Numérisation page {current} / {total} — Placez la feuille et attendez...")

    def on_page_scanned(self, filepath):
        self.progress_label.setText(f"Page scannée : {os.path.basename(filepath)}")

    def on_scan_finished(self, total):
        self.print_btn.setEnabled(True)
        self.stop_btn.setVisible(False)
        self.progress_bar.setValue(100)
        self.progress_label.setText(f"Numérisation terminée : {total} pages")
        QMessageBox.information(self, "Numérisation terminée",
            f"{total} page(s) numérisée(s) avec succès !\n\n"
            f"Fichiers enregistrés dans :\n{self.scan_folder}")

    def on_scan_error(self, message):
        self.print_btn.setEnabled(True)
        self.stop_btn.setVisible(False)
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)
        QMessageBox.critical(self, "Erreur de numérisation", message)
