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
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

class PTBXLDownloader:
    """Download PTB-XL dataset from PhysioNet"""

    def __init__(self, base_url="https://physionet.org/content/ptb-xl/1.0.3/",
                 output_dir="data/raw/physionet.org/files/ptb-xl/1.0.3"):
        self.base_url = base_url
        self.output_dir = Path(output_dir)
        self.session = requests.Session()
        self.downloaded_count = 0
        self.total_size = 0

    def get_directory_listing(self, url):
        """Get list of files from a PhysioNet directory"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            files = []
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and not href.startswith(('?', '#', 'http')):
                    files.append(href)

            return files
        except Exception as e:
            print(f"Error getting directory listing from {url}: {e}")
            return []

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

        metadata_files = [
            'ptbxl_database.csv',
            'scp_statements.csv',
            'sha256sums.txt',
            'LICENSE.txt',
            'RECORDS',
            'RECORDS-WFDB'
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

        # Get list of patient directories
        records_url = urljoin(self.base_url, folder + '/')
        subdirs = self.get_directory_listing(records_url)

        # Filter out non-directory items
        subdirs = [d for d in subdirs if not d.endswith('.html') and d.endswith('/')]

        print(f"\nFound {len(subdirs)} patient groups")

        patient_count = 0

        for subdir in subdirs:
            subdir_url = urljoin(records_url, subdir)
            files = self.get_directory_listing(subdir_url)

            # Get patient files (.dat and .hea)
            patient_files = [f for f in files if f.endswith(('.dat', '.hea'))]

            for patient_file in patient_files:
                if max_patients and patient_count >= max_patients:
                    print(f"\n[OK] Reached limit of {max_patients} patients")
                    return

                file_url = urljoin(subdir_url, patient_file)
                local_path = self.output_dir / folder / subdir.rstrip('/') / patient_file

                self.download_file(file_url, local_path, show_progress=False)

                # Count unique patients (based on .dat files)
                if patient_file.endswith('.dat'):
                    patient_count += 1
                    if patient_count % 100 == 0:
                        print(f"\n[Progress] Downloaded {patient_count} patients...")

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
