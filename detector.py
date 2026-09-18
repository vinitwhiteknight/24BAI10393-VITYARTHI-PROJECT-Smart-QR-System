"""QR/barcode detection and decoding logic."""

from pyzbar.pyzbar import decode as pyzbar_decode


class DetectionResult:
    """Container for one validated decoded QR/barcode result."""

    def __init__(self, decoded_data, code_type):
        self.decoded_data = decoded_data
        self.code_type = code_type


def detect_codes(image):
    """Return validated QR/barcode results found in an image."""
    results = []
    for symbol in pyzbar_decode(image):
        try:
            decoded_text = symbol.data.decode("utf-8").strip()
        except UnicodeDecodeError:
            continue

        if not decoded_text:
            continue

        results.append(DetectionResult(decoded_text, symbol.type))
    return results
