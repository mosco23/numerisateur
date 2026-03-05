import os
import sys
import subprocess


def is_windows():
    return sys.platform == "win32"


def print_pdf(pdf_path, printer_name):
    """Imprime un fichier PDF sur l'imprimante spécifiée."""
    if is_windows():
        import win32api
        import win32print
        win32api.ShellExecute(0, "print", pdf_path, f'/d:"{printer_name}"', ".", 0)
        return True, ""
    else:
        result = subprocess.run(
            ["lp", "-d", printer_name, pdf_path],
            capture_output=True, text=True
        )
        return result.returncode == 0, result.stderr


def scan_page(output_path, fmt, resolution):
    """Scanne une page et la sauvegarde. Retourne (success, error_message)."""
    if is_windows():
        return _scan_wia(output_path, fmt, resolution)
    else:
        return _scan_sane(output_path, fmt, resolution)


def _scan_sane(output_path, fmt, resolution):
    """Scan via SANE (Linux)."""
    scan_fmt = "png" if fmt == "PDF" else fmt.lower()
    cmd = [
        "scanimage",
        f"--format={scan_fmt}",
        f"--resolution={resolution}",
        f"--output-file={output_path}"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return False, result.stderr.strip()
    return True, ""


def _scan_wia(output_path, fmt, resolution):
    """Scan via WIA (Windows)."""
    try:
        import comtypes.client

        wia_device_type_scanner = 1
        wia_img_format_png = "{B96B3CAF-0728-11D3-9D7B-0000F81EF32E}"
        wia_img_format_jpeg = "{B96B3CAE-0728-11D3-9D7B-0000F81EF32E}"
        wia_img_format_bmp = "{B96B3CAB-0728-11D3-9D7B-0000F81EF32E}"

        wia_manager = comtypes.client.CreateObject("WIA.DeviceManager")
        devices = wia_manager.DeviceInfos

        scanner = None
        for i in range(1, devices.Count + 1):
            info = devices.Item(i)
            if info.Type == wia_device_type_scanner:
                scanner = info
                break

        if scanner is None:
            return False, "Aucun scanner détecté.\nVérifiez que votre scanner est connecté et allumé."

        device = scanner.Connect()
        item = device.Items.Item(1)

        # Configurer la résolution
        for prop in item.Properties:
            if prop.Name == "Horizontal Resolution":
                prop.Value = resolution
            elif prop.Name == "Vertical Resolution":
                prop.Value = resolution

        image = item.Transfer(wia_img_format_png)

        # Sauvegarder l'image temporaire
        tmp_path = output_path
        if fmt.upper() in ("PNG", "JPEG", "JPG"):
            tmp_path = output_path
        else:
            tmp_path = output_path + ".tmp.png"

        # Utiliser SaveFile via FileData
        vector = image.FileData
        binary_data = bytes(vector.BinaryData)
        with open(tmp_path, "wb") as f:
            f.write(binary_data)

        if fmt.upper() in ("JPEG", "JPG"):
            from PIL import Image
            img = Image.open(tmp_path)
            img.save(output_path, "JPEG")
            if tmp_path != output_path:
                os.unlink(tmp_path)

        return True, ""

    except ImportError:
        return False, (
            "Le module 'comtypes' est requis pour la numérisation sous Windows.\n"
            "Installez-le avec : pip install comtypes"
        )
    except Exception as e:
        return False, str(e)
