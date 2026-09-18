# VITYARTHI-PROJECT-Smart-QR-System
# Smart QR & Barcode Detection and Result Management System

This is a Python command-line project that I made for detecting and reading QR codes and barcodes from image files.

The basic idea is simple: give the program an image, let it find and decode the QR code or barcode, and then save the result so it can be checked later. The project uses OpenCV for reading images, pyzbar for decoding, and SQLite for storing the scan results.


## Overview

```text
Image file(s)
     |
     v
 scanner.py
     |
     v
 detector.py  ---> QR / Barcode decoding
     |
     v
 duplicate + validation check
     |
     v
 storage.py ---> SQLite database
     |
     +----> history
     +----> analytics.py
     +----> CSV export
```

## Major Functional Modules

1. **Detection & Decoding** - reads an image and identifies QR codes/barcodes using `pyzbar`.
2. **Scan Storage & History** - validates results, prevents repeated scans within the cooldown period, and stores records in SQLite.
3. **Analytics & Reporting** - displays QR/barcode statistics and exports scan history to CSV.
4. **Batch Processing** - scans all supported images in a directory from the terminal.

## Non-Functional Requirements

- **Performance:** process each supplied image once without maintaining a continuous GUI loop.
- **Reliability:** invalid paths, unreadable images, empty detections, and invalid decoded bytes are handled without terminating unexpectedly.
- **Usability:** commands and an interactive terminal menu provide clear prompts and status messages.
- **Maintainability:** detection, scanning, storage, analytics, configuration, and tests are separated into modules.
- **Resource efficiency:** image files are processed independently and duplicate records are suppressed using a configurable cooldown.

## Technologies Used

- Python 3
- OpenCV (`opencv-python`) - image loading
- `pyzbar` - QR/barcode decoding
- SQLite - persistent storage through Python's built-in `sqlite3`
- `unittest` - automated testing

## Project Structure

```text
Smart-QR-Barcode-System/
├── app.py                 # CLI entry point and command dispatcher
├── scanner.py             # Single-image and batch scanning
├── detector.py            # QR/barcode detection and decoding
├── storage.py             # SQLite database and CSV export
├── analytics.py           # Scan statistics and reporting
├── config.py              # Central configuration
├── utils.py               # Shared helper functions
├── tests/
│   ├── test_storage.py
│   └── test_analytics.py
├── data/                  # Created automatically at runtime
├── README.md
├── statement.md
├── requirements.txt
└── .gitignore
```

## Installation

```bash
git clone <your-repo-url>
cd Smart-QR-Barcode-System
python -m venv venv
```

Activate the environment:

**Windows**
```bash
venv\Scripts\activate
```

**Linux/macOS**
```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

> `pyzbar` requires the ZBar library on some operating systems. On Debian/Ubuntu, install it with `sudo apt-get install libzbar0`. Follow the ZBar package instructions appropriate to your operating system if required.

## Command-Line Usage

### 1. Show help

```bash
python app.py --help
```

### 2. Scan one image

```bash
python app.py scan --image samples/qr_code.png
```

Example output:

```text
Scanning: samples/qr_code.png
  SAVED: [QRCODE] https://example.com
Detections found: 1
```

### 3. Batch-scan a directory

```bash
python app.py scan --directory samples
```

Supported formats: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tif`, `.tiff`, `.webp`.

### 4. View scan history

```bash
python app.py history
```

### 5. View analytics

```bash
python app.py analytics
```

### 6. Export CSV

```bash
python app.py export --output data/results.csv
```

### 7. Interactive CLI menu

Run without a subcommand:

```bash
python app.py
```

The terminal menu provides scanning, history, analytics, export, clearing records, and exit options.

## Testing

Run all tests from the project root:

```bash
python -m unittest discover tests -v
```

The tests use temporary databases and do not modify the normal project database.

## Input / Output

**Input:** local image files containing QR codes or barcodes.

**Processing:** decode -> validate -> duplicate check -> store.

**Outputs:** terminal results, SQLite scan history, analytics summary, and CSV export.

## Screenshots / Demonstration
![Successful QR code scan](<Screenshot 2026-09-18 115736.png>)
![Help command](<Screenshot 2026-09-18 134017.png>)
![Scan history](<Screenshot 2026-09-18 134341.png>)
![Unit test results](<Screenshot 2026-09-18 134301.png>)
![CSV export](<Screenshot 2026-09-18 120153.png>)


## Future Enhancements

- Support additional barcode formats and decoding libraries.
- Add configurable duplicate cooldown from the CLI.
- Add structured JSON export.
- Add optional webcam support as a separate non-default feature without making the core application GUI-dependent.
