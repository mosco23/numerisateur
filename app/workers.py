import os

from PyQt6.QtCore import QThread, pyqtSignal

from reportlab.pdfgen import canvas

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
