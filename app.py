import argparse
import sys

from analytics import compute_statistics, format_statistics
from config import EXPORT_CSV_PATH
from scanner import scan_directory, scan_image
from storage import clear_all_scans, export_to_csv, get_all_scans, init_db


def build_parser():
    parser = argparse.ArgumentParser(
        prog="smart-qr",
        description="Command-line QR and barcode detection, storage and analytics system.",
    )
    sub = parser.add_subparsers(dest="command")

    scan = sub.add_parser("scan", help="Detect QR/barcodes from an image or directory.")
    source = scan.add_mutually_exclusive_group(required=True)
    source.add_argument("--image", help="Path to one image containing QR/barcodes.")
    source.add_argument("--directory", help="Directory of images to scan in batch.")

    sub.add_parser("history", help="Display saved scan history.")
    sub.add_parser("analytics", help="Display scan statistics.")

    export = sub.add_parser("export", help="Export scan history to CSV.")
    export.add_argument("--output", default=EXPORT_CSV_PATH, help="CSV output path.")

    sub.add_parser("clear", help="Delete all stored scan records after confirmation.")
    return parser


def print_history():
    scans = get_all_scans()
    if not scans:
        print("No scan records found.")
        return

    print("\nSCAN HISTORY")
    print("=" * 88)
    print(f"{'ID':<5} {'TYPE':<12} {'DATE':<12} {'TIME':<10} DATA")
    print("-" * 88)
    for scan in scans:
        data = scan["decoded_data"]
        if len(data) > 48:
            data = data[:45] + "..."
        print(f"{scan['scan_id']:<5} {scan['code_type']:<12} {scan['scan_date']:<12} {scan['scan_time']:<10} {data}")
    print("=" * 88)
    print(f"Total records: {len(scans)}")


def interactive_menu():
    while True:
        print("\n" + "=" * 44)
        print(" SMART QR & BARCODE SYSTEM")
        print("=" * 44)
        print("1. Scan an image")
        print("2. Scan a directory of images")
        print("3. View scan history")
        print("4. View analytics")
        print("5. Export history to CSV")
        print("6. Clear all records")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            path = input("Enter image path: ").strip()
            scan_image(path)
        elif choice == "2":
            path = input("Enter directory path: ").strip()
            scan_directory(path)
        elif choice == "3":
            print_history()
        elif choice == "4":
            print("\n" + format_statistics(compute_statistics()))
        elif choice == "5":
            path = input(f"Output CSV path [{EXPORT_CSV_PATH}]: ").strip() or EXPORT_CSV_PATH
            print(f"CSV exported to: {export_to_csv(path)}")
        elif choice == "6":
            confirm = input("Type YES to delete all scan records: ").strip()
            if confirm == "YES":
                clear_all_scans()
                print("All scan records deleted.")
            else:
                print("Operation cancelled.")
        elif choice == "7":
            print("Goodbye.")
            return 0
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


def main(argv=None):
    init_db()
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        return interactive_menu()
    if args.command == "scan":
        if args.image:
            return 0 if scan_image(args.image) else 1
        return 0 if scan_directory(args.directory) else 1
    if args.command == "history":
        print_history()
        return 0
    if args.command == "analytics":
        print(format_statistics(compute_statistics()))
        return 0
    if args.command == "export":
        print(f"CSV exported to: {export_to_csv(args.output)}")
        return 0
    if args.command == "clear":
        confirm = input("Type YES to delete all scan records: ").strip()
        if confirm == "YES":
            clear_all_scans()
            print("All scan records deleted.")
            return 0
        print("Operation cancelled.")
        return 1

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
