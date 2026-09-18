"""Analytics functions for saved scan records."""

from storage import get_all_scans

QR_TYPE_NAME = "QRCODE"


def compute_statistics():
    scans = get_all_scans()
    total_scans = len(scans)
    qr_count = sum(1 for scan in scans if scan["code_type"] == QR_TYPE_NAME)
    barcode_count = total_scans - qr_count
    return {
        "total_scans": total_scans,
        "qr_count": qr_count,
        "barcode_count": barcode_count,
    }


def format_statistics(stats):
    return (
        "ANALYTICS\n"
        "========="
        f"\nTotal scans : {stats['total_scans']}"
        f"\nQR codes    : {stats['qr_count']}"
        f"\nBarcodes    : {stats['barcode_count']}"
    )
