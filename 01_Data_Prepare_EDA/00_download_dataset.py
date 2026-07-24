"""
PTB-XL ECG Database Download Script
Dataset: https://physionet.org/content/ptb-xl/1.0.3/
Size: ~1.7 GB (compressed), ~3.0 GB (uncompressed)
"""

import os
import urllib.request
import zipfile
from pathlib import Path
from tqdm import tqdm

# Configuration
DATASET_URL = "https://physionet.org/static/published-projects/ptb-xl/ptb-xl-a-large-publicly-available-electrocardiography-dataset-1.0.3.zip"
DATA_DIR = Path("../data/raw")
EXTRACT_DIR = DATA_DIR / "ptb-xl"

class DownloadProgressBar(tqdm):
    """Progress bar for download"""
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def download_dataset():
    """Download PTB-XL dataset from PhysioNet"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)

    zip_path = DATA_DIR / "ptb-xl.zip"

    if zip_path.exists():
        print(f"Dataset already downloaded at {zip_path}")
        response = input("Re-download? (y/n): ")
        if response.lower() != 'y':
            print("Skipping download...")
            return zip_path

    print(f"Downloading PTB-XL dataset...")
    print(f"Size: ~1.7 GB - This may take several minutes...")

    try:
        with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc="Downloading") as t:
            urllib.request.urlretrieve(DATASET_URL, zip_path, reporthook=t.update_to)
        print(f"\nDownload complete! Saved to {zip_path}")
        return zip_path
    except Exception as e:
        print(f"Error: {e}")
        print("\nAlternative methods:")
        print("1. Manual: https://physionet.org/content/ptb-xl/1.0.3/")
        print("2. wget: wget -r -N -c -np https://physionet.org/files/ptb-xl/1.0.3/")
        return None

def extract_dataset(zip_path):
    """Extract downloaded dataset"""
    if not zip_path or not zip_path.exists():
        print("No zip file to extract")
        return False

    if (EXTRACT_DIR / "ptbxl_database.csv").exists():
        print(f"Dataset already extracted at {EXTRACT_DIR}")
        response = input("Re-extract? (y/n): ")
        if response.lower() != 'y':
            return True

    print(f"\nExtracting to {EXTRACT_DIR}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file in tqdm(zip_ref.namelist(), desc="Extracting"):
                zip_ref.extract(file, EXTRACT_DIR)

        # Move nested files up
        nested = EXTRACT_DIR / "ptb-xl-a-large-publicly-available-electrocardiography-dataset-1.0.3"
        if nested.exists():
            import shutil
            for item in nested.iterdir():
                shutil.move(str(item), str(EXTRACT_DIR / item.name))
            nested.rmdir()

        print("Extraction complete!")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def verify_dataset():
    """Verify dataset integrity"""
    print("\nVerifying dataset...")
    required = ["ptbxl_database.csv", "scp_statements.csv", "records100", "records500"]

    all_ok = True
    for item in required:
        path = EXTRACT_DIR / item
        if path.exists():
            print(f"✓ {item}")
        else:
            print(f"✗ {item} (missing)")
            all_ok = False

    if all_ok:
        print("\n✓ Dataset ready!")
        print(f"Location: {EXTRACT_DIR.absolute()}")
    return all_ok

if __name__ == "__main__":
    print("=" * 60)
    print("PTB-XL ECG Database Download")
    print("=" * 60)

    zip_path = download_dataset()
    if zip_path and extract_dataset(zip_path):
        verify_dataset()

    print("\n" + "=" * 60)
