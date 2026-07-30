"""
PTB-XL Dataset Downloader

This script downloads the PTB-XL ECG dataset from PhysioNet.
It downloads files selectively and shows progress.

Usage:
    python download_ptbxl.py --all              # Download everything
    python download_ptbxl.py --metadata         # Download only metadata files
    python download_ptbxl.py --records100       # Download 100Hz records only
    python download_ptbxl.py --records500       # Download 500Hz records only
    python download_ptbxl.py --sample 100       # Download first 100 patients
"""

import os
import sys
import argparse
import requests
from pathlib import Path
from urllib.parse import urljoin
import time

class PTBXLDownloader:
    """Download PTB-XL dataset from PhysioNet"""

    # FIX: the old base_url pointed at physionet.org/content/..., which is
    # PhysioNet's human-facing project webpage. Requesting a "file" there
    # (e.g. ptbxl_database.csv or a .hea file) returns Content-Type: text/html
    # -- a rendered preview page, NOT the actual file bytes -- unless a
    # '?download' query string is appended. physionet.org/files/... is the
    # real static file server and returns true raw content (verified
    # directly: text/plain, exact byte-for-byte file contents) for every
    # file in this dataset.
    def __init__(self, base_url="https://physionet.org/files/ptb-xl/1.0.3/",
                 output_dir="data/raw/physionet.org/files/ptb-xl/1.0.3"):
        self.base_url = base_url
        self.output_dir = Path(output_dir)
        self.session = requests.Session()
        self.downloaded_count = 0
        self.total_size = 0

    def download_file(self, url, local_path, show_progress=True):
        """Download a single file with progress indication"""
        try:
            # Create directory if needed
            local_path.parent.mkdir(parents=True, exist_ok=True)

            # Skip if file already exists
            if local_path.exists():
                print(f"[SKIP] {local_path.name} (already exists)")
                return True

            # Download with streaming
            response = self.session.get(url, stream=True)
            response.raise_for_status()

            # FIX: guard against silently saving an HTML error/preview page
            # as if it were the real data file (exactly what happened with
            # the old /content/ base_url). Any non-.html target file should
            # never come back as text/html.
            content_type = response.headers.get('content-type', '')
            if 'text/html' in content_type.lower() and local_path.suffix.lower() != '.html':
                print(f"\n[ERROR] {url} returned HTML (Content-Type: {content_type}) "
                      f"instead of the expected file -- not saving. This usually means "
                      f"the URL is wrong (e.g. pointing at a webpage instead of the raw file).")
                return False

            total_size = int(response.headers.get('content-length', 0))

            with open(local_path, 'wb') as f:
                if show_progress and total_size > 0:
                    downloaded = 0
                    chunk_size = 8192

                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            percent = (downloaded / total_size) * 100

                            # Show progress bar
                            bar_length = 40
                            filled = int(bar_length * downloaded / total_size)
                            bar = '=' * filled + '-' * (bar_length - filled)

                            print(f"\r[{bar}] {percent:.1f}% {local_path.name}", end='')

                    print()  # New line after progress
                else:
                    f.write(response.content)
                    print(f"[OK] {local_path.name}")

            self.downloaded_count += 1
            self.total_size += total_size
            return True

        except Exception as e:
            print(f"\n[ERROR] Failed to download {url}: {e}")
            if local_path.exists():
                local_path.unlink()  # Remove partial file
            return False

    def download_metadata_files(self):
        """Download metadata CSV files"""
        print("\n" + "="*70)
        print("DOWNLOADING METADATA FILES")
        print("="*70)

        # FIX: 'sha256sums.txt' 404'd -- the real file on PhysioNet is
        # uppercase 'SHA256SUMS.txt'. 'RECORDS-WFDB' doesn't exist on
        # PhysioNet for this dataset at all (only 'RECORDS') -- removed.
        # Neither of these affects the notebook (only ptbxl_database.csv and
        # scp_statements.csv are actually read by it), but fixing them avoids
        # confusing false [ERROR] lines during download.
        metadata_files = [
            'ptbxl_database.csv',
            'scp_statements.csv',
            'SHA256SUMS.txt',
            'LICENSE.txt',
            'RECORDS',
        ]

        for filename in metadata_files:
            url = urljoin(self.base_url, filename)
            local_path = self.output_dir / filename
            print(f"\nDownloading: {filename}")
            self.download_file(url, local_path)

    def download_records(self, sampling_rate=100, max_patients=None):
        """Download ECG records at specified sampling rate

        Args:
            sampling_rate: 100 or 500 Hz
            max_patients: Maximum number of patients to download (None = all)
        """
        folder = f"records{sampling_rate}"
        print("\n" + "="*70)
        print(f"DOWNLOADING ECG RECORDS ({sampling_rate} Hz)")
        if max_patients:
            print(f"Limit: First {max_patients} patients")
        print("="*70)

        # FIX: PhysioNet's file server does not serve a browsable directory
        # listing for records100/records500/ (fetching that URL returns an
        # empty page, or -- when pointed at the /content/ project page --
        # returns the human-facing webpage instead, which includes a
        # "share via email" mailto: link. The old code scraped that page with
        # BeautifulSoup looking for subfolder links, picked up the mailto:
        # link as if it were a directory, and crashed trying to GET it
        # ("No connection adapters were found for 'mailto:...'").
        #
        # The reliable, PhysioNet-recommended way to enumerate every record
        # is to use the file paths already listed in ptbxl_database.csv's
        # filename_lr / filename_hr columns (downloaded in
        # download_metadata_files() just before this runs), rather than
        # trying to scrape a directory index that doesn't exist.
        import pandas as pd

        db_path = self.output_dir / 'ptbxl_database.csv'
        if not db_path.exists():
            print(f"[ERROR] {db_path} not found -- run with --metadata first "
                  f"(or --records100/--records500/--all, which download it automatically).")
            return

        db = pd.read_csv(db_path)
        filename_col = 'filename_lr' if sampling_rate == 100 else 'filename_hr'
        if filename_col not in db.columns:
            print(f"[ERROR] Column '{filename_col}' not found in {db_path}")
            return

        record_paths = db[filename_col].dropna().unique().tolist()
        if max_patients:
            record_paths = record_paths[:max_patients]

        print(f"\nFound {len(record_paths):,} records to download "
              f"({'all' if not max_patients else f'limited to first {max_patients}'})")

        patient_count = 0

        for record_path in record_paths:
            # record_path looks like 'records100/00000/00001_lr'
            for ext in ('.dat', '.hea'):
                file_url = urljoin(self.base_url, record_path + ext)
                local_path = self.output_dir / (record_path + ext)
                self.download_file(file_url, local_path, show_progress=False)

            patient_count += 1
            if patient_count % 100 == 0:
                print(f"\n[Progress] Downloaded {patient_count:,} / {len(record_paths):,} patients...")

        print(f"\n[OK] Finished downloading {patient_count:,} patient record(s).")

    def download_all(self, max_patients=None):
        """Download complete dataset"""
        print("\n" + "="*70)
        print("PTB-XL DATASET DOWNLOADER")
        print("="*70)
        print(f"Output directory: {self.output_dir}")
        print(f"Base URL: {self.base_url}")

        start_time = time.time()

        # Download metadata
        self.download_metadata_files()

        # Download 100 Hz records
        self.download_records(sampling_rate=100, max_patients=max_patients)

        # Summary
        elapsed = time.time() - start_time
        print("\n" + "="*70)
        print("DOWNLOAD SUMMARY")
        print("="*70)
        print(f"Files downloaded: {self.downloaded_count}")
        print(f"Total size: {self.total_size / (1024*1024):.2f} MB")
        print(f"Time elapsed: {elapsed/60:.1f} minutes")
        print(f"Output location: {self.output_dir}")
        print("="*70)


def main():
    parser = argparse.ArgumentParser(description='Download PTB-XL dataset from PhysioNet')
    parser.add_argument('--all', action='store_true', help='Download complete dataset')
    parser.add_argument('--metadata', action='store_true', help='Download only metadata files')
    parser.add_argument('--records100', action='store_true', help='Download 100Hz records')
    parser.add_argument('--records500', action='store_true', help='Download 500Hz records')
    parser.add_argument('--sample', type=int, help='Download first N patients only')
    parser.add_argument('--output', type=str, default='data/raw/physionet.org/files/ptb-xl/1.0.3',
                       help='Output directory (default: data/raw/physionet.org/files/ptb-xl/1.0.3)')

    args = parser.parse_args()

    # Create downloader
    downloader = PTBXLDownloader(output_dir=args.output)

    # Execute based on arguments
    if args.metadata:
        downloader.download_metadata_files()
    elif args.records100:
        downloader.download_metadata_files()
        downloader.download_records(sampling_rate=100, max_patients=args.sample)
    elif args.records500:
        downloader.download_metadata_files()
        downloader.download_records(sampling_rate=500, max_patients=args.sample)
    elif args.all or args.sample:
        downloader.download_all(max_patients=args.sample)
    else:
        print("Please specify what to download:")
        print("  --all              Download complete dataset")
        print("  --metadata         Download only metadata files")
        print("  --records100       Download 100Hz records")
        print("  --records500       Download 500Hz records")
        print("  --sample N         Download first N patients")
        print("\nExample:")
        print("  python download_ptbxl.py --sample 100")
        print("  python download_ptbxl.py --metadata")
        print("  python download_ptbxl.py --all")


if __name__ == "__main__":
    main()
