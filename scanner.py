"""Image-based scanning functions used by the command-line application."""

import os

import cv2

from config import DUPLICATE_COOLDOWN_SECONDS
from detector import detect_codes
from storage import save_scan, was_recently_scanned


def _store_detections(detections, source_name):
    saved = 0
    for detection in detections:
        if was_recently_scanned(detection.decoded_data, DUPLICATE_COOLDOWN_SECONDS):
            print(f"  SKIPPED duplicate: [{detection.code_type}] {detection.decoded_data}")
            continue
        save_scan(detection.decoded_data, detection.code_type)
        print(f"  SAVED: [{detection.code_type}] {detection.decoded_data}")
        saved += 1

    if not detections:
        print(f"  No QR code or barcode detected in {source_name}.")
    return saved


def scan_image(image_path):
    """Read one image, detect codes, validate results and store new scans."""
    if not os.path.isfile(image_path):
        print(f"ERROR: Image file not found: {image_path}")
        return False

    frame = cv2.imread(image_path)
    if frame is None:
        print(f"ERROR: Could not read image: {image_path}")
        return False

    print(f"\nScanning: {image_path}")
    detections = detect_codes(frame)
    _store_detections(detections, image_path)
    print(f"Detections found: {len(detections)}")
    return True


def scan_directory(directory_path):
    """Batch-scan common image files in a directory without opening a GUI."""
    if not os.path.isdir(directory_path):
        print(f"ERROR: Directory not found: {directory_path}")
        return False

    extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}
    files = sorted(
        os.path.join(directory_path, name)
        for name in os.listdir(directory_path)
        if os.path.splitext(name)[1].lower() in extensions
    )

    if not files:
        print("ERROR: No supported image files found in the directory.")
        return False

    print(f"\nBatch scanning {len(files)} image(s)...")
    for path in files:
        scan_image(path)
    print("Batch scan completed.")
    return True
