import os
import io

from PyQt6.QtCore import QThread, pyqtSignal

from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

from app.platform_utils import scan_page


class ScanWorker(QThread):
    progress = pyqtSignal(int, int)
    page_scanned = pyqtSignal(str)
    finished = pyqtSignal(int)
    error = pyqtSignal(str)

    def __init__(self, output_dir, start_num, end_num, fmt, resolution):
        super().__init__()
        self.output_dir = output_dir
        self.start_num = start_num
        self.end_num = end_num
        self.fmt = fmt
        self.resolution = resolution
        self._stop_requested = False

    def stop(self):
        self._stop_requested = True

    def run(self):
        total = self.end_num - self.start_num + 1
        scanned = 0

        for num in range(self.start_num, self.end_num + 1):
            if self._stop_requested:
                break

            self.progress.emit(num - self.start_num + 1, total)

            ext = "pdf" if self.fmt == "PDF" else self.fmt.lower()
            filename = f"page_{num:04d}.{ext}"
            filepath = os.path.join(self.output_dir, filename)

            # Scan vers PNG temporaire si format PDF, sinon directement
            if self.fmt == "PDF":
                tmp_img = os.path.join(self.output_dir, f"_tmp_scan_{num}.png")
                success, err = scan_page(tmp_img, "PNG", self.resolution)
            else:
                success, err = scan_page(filepath, self.fmt, self.resolution)

            if not success:
                self.error.emit(
                    f"Erreur lors du scan de la page {num} :\n{err}\n\n"
                    "Vérifiez que votre scanner est connecté et allumé."
                )
                return

            # Convertir PNG → PDF si nécessaire
            if self.fmt == "PDF":
                try:
                    from reportlab.lib.utils import ImageReader
                    img = ImageReader(tmp_img)
                    img_w, img_h = img.getSize()
                    c_pdf = canvas.Canvas(filepath, pagesize=(img_w, img_h))
                    c_pdf.drawImage(tmp_img, 0, 0, img_w, img_h)
                    c_pdf.save()
                    os.unlink(tmp_img)
                except Exception as e:
                    self.error.emit(f"Erreur de conversion PDF à la page {num} :\n{e}")
                    return

            scanned += 1
            self.page_scanned.emit(filepath)

        self.finished.emit(scanned)


class NumberingWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, input_path, output_path, start_num, end_num, position, font_size, margin_top):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path
        self.start_num = start_num
        self.end_num = end_num
        self.position = position
        self.font_size = font_size
        self.margin_top = margin_top

    def run(self):
        try:
            reader = PdfReader(self.input_path)
            writer = PdfWriter()
            total_pages = len(reader.pages)

            if self.end_num > total_pages:
                self.error.emit(
                    f"Le document ne contient que {total_pages} pages. "
                    f"La plage demandée dépasse le nombre de pages."
                )
                return

            for i, page in enumerate(reader.pages):
                page_num = i + 1

                if self.start_num <= page_num <= self.end_num:
                    media_box = page.mediabox
                    page_width = float(media_box.width)
                    page_height = float(media_box.height)

                    packet = io.BytesIO()
                    c = canvas.Canvas(packet, pagesize=(page_width, page_height))
                    c.setFont("Helvetica", self.font_size)

                    number_text = str(page_num)
                    text_width = c.stringWidth(number_text, "Helvetica", self.font_size)

                    y_pos = page_height - self.margin_top * mm

                    if self.position == "gauche":
                        x_pos = 30 * mm
                    elif self.position == "droite":
                        x_pos = page_width - 30 * mm - text_width
                    else:
                        x_pos = (page_width - text_width) / 2

                    c.drawString(x_pos, y_pos, number_text)
                    c.save()
                    packet.seek(0)

                    overlay_reader = PdfReader(packet)
                    page.merge_page(overlay_reader.pages[0])

                writer.add_page(page)
                self.progress.emit(int(((i + 1) / total_pages) * 100))

            with open(self.output_path, "wb") as f:
                writer.write(f)

            self.finished.emit(self.output_path)

        except Exception as e:
            self.error.emit(str(e))
