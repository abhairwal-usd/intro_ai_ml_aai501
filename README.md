# Cardiac Arrhythmia Classification

This repository is the team's workspace for our AAI-501 project. We use the **PTB-XL ECG dataset** to train a model to detect abnormal heart rhythms (arrhythmias) from a single-lead ECG signal, following the same testing approach used in the paper referenced below.

---

## 📝 Introduction: Project Context & Goals

### Project Context

Doctors can spot heart problems by looking at a patient's ECG (electrocardiogram) signal. Wearable devices like smartwatches can now record a simple, single-lead version of this signal (called Lead-I), which makes it possible to catch arrhythmias outside a hospital. This project builds a machine learning model that reads a Lead-I ECG signal and predicts whether it shows a normal heartbeat or an arrhythmia.

There's a catch that makes this a real problem worth solving. If you train and test a model on ECGs from the same group of people, it can score very high — often 90%+ — because it partly "memorizes" quirks of those specific patients. But when that same model is tested on ECGs from patients it has never seen, or on noisier recordings (like the ones you'd actually get from a wearable in daily life), accuracy can drop a lot. Our anchor paper measured exactly this drop.

- **Anchor paper:** Sadiq et al. (2025), *"Cardiac Arrhythmia Classification From Lead I ECG Recorded in a Free-Living Environment,"* IEEE Journal of Biomedical and Health Informatics. ([IEEE Xplore](https://ieeexplore.ieee.org/document/11259110))
- **Dataset:** [PTB-XL v1.0.3](https://physionet.org/content/ptb-xl/1.0.3/) — 21,799 ECG recordings from 18,869 patients (PhysioNet).
- **Main question we're answering:** How much worse does the model get when we test it on new patients instead of ones it already saw, and when we add noise to the signal?

### What the Model Predicts

Given one 10-second Lead-I ECG recording, the model predicts which cardiac rhythm(s) are present. This is a **multi-label classification** problem (a recording can show more than one condition at once), and the anchor paper focuses on seven arrhythmia labels that show up consistently across datasets, including PTB-XL:

| Label | Condition |
| ----- | --------- |
| **NSR** | Normal Sinus Rhythm (no arrhythmia) |
| **AFb / AFl** | Atrial Fibrillation / Atrial Flutter |
| **1AV** | First-Degree AV Block |
| **PAC** | Premature Atrial Contraction |
| **PVC** | Premature Ventricular Contraction |
| **BRADY** | Bradycardia (abnormally slow heart rate) |
| **TACHY** | Tachycardia (abnormally fast heart rate) |

We'll start with this same seven-label set on PTB-XL so our results are directly comparable to the paper's, and can expand to PTB-XL's full label set if time allows.

### Project Goals

1. **Clean the data**: Prepare the PTB-XL Lead-I signals — handle missing or broken records, resample the signals, remove noise, and cut out individual heartbeats.
2. **Explore the data**: Look at how many examples we have of each arrhythmia type, check heartbeat-timing and shape features, and run basic statistical tests.
3. **Build models**: Start with a simpler model (Random Forest / SVM using heartbeat-timing and shape features), then try a stronger one (XGBoost or a 1D CNN).
4. **Test how well it really works**: Compare results when testing on already-seen patients vs. brand-new patients, and check performance under noise. This comparison is the most important part of the project.

---

## 📁 Repository Directory Structure

```
intro_ai_ml_aai501/
├── README.md
├── requirements.txt
├── .gitignore
├── .gitattributes
├── scripts/                       # Standalone utility scripts
│   ├── download_ptbxl.py          #   Downloads the raw PTB-XL dataset from PhysioNet (see below)
│   └── show_ecg_data.py           #   Quick viewer/sanity-check for a downloaded ECG record
├── data/
│   ├── raw/                       # Raw PTB-XL source files -- NOT committed, download-only (see .gitignore)
│   │   └── physionet.org/files/ptb-xl/1.0.3/   # <- scripts/download_ptbxl.py writes here; the notebooks read from here
│   ├── preprocessed/              # Cleaning/EDA outputs from 01_Data_Prepare_EDA + model_features.csv from 02_Model_Selection (committed via Git LFS)
│   └── sample_ecg/                # 100 real ECGs bundled for smoke-testing only -- see data/sample_ecg/README.md
├── 01_Data_Prepare_EDA/           # Data cleaning + exploratory data analysis
├── 02_Model_Selection/            # Feature engineering, baseline model, advanced model
│   ├── 01_feature_engineering.ipynb   # Lead I signal features + metadata encoding -> data/preprocessed/model_features.csv
│   └── 02_model_training.ipynb        # Baseline (Random Forest) vs advanced (XGBoost) model comparison
├── 03_Model_Diagnostics/          # Intra- vs inter-patient diagnostics, ROC/AUC, confusion matrices
└── 04_Master_Pipeline/            # Final end-to-end notebook, technical paper, presentation
```

Each folder holds its own notebook(s) and finished report files as the project moves forward.

**Important:** the *only* raw-data path the notebooks read from is `data/raw/physionet.org/files/ptb-xl/1.0.3/` (created automatically by `scripts/download_ptbxl.py`, see below). If you see any other `data/raw/...` folder in your checkout, it's stale and not used by any notebook -- delete it rather than trying to point anything at it.

---

## 👥 Team Roles & Responsibilities

| Folder Subsystem                     | Owner(s)                                                  | Milestone                                  | Target Date |
| ------------------------------------- | ----------------------------------------------------------- | ------------------------------------------- | ----------- |
| **`01_Data_Prep_EDA/`**               | Ashok Bhairwal                                              | Data Cleaning & EDA                         | Jul 26      |
| **`02_Model_Selection/`**             | Diaesh Antony                                                | Baseline Model + Advanced Model / Tuning    | Aug 01      |
| **`03_Model_Analysis_Diagnostics/`**  | N L N Sai Krishna Akula                                      | Model Diagnostics & Comparative Analysis    | Aug 05      |
| **`04_Master_Pipeline/`**             | Joint (Ashok Bhairwal, N L N Sai Krishna Akula, Diaesh Antony) | Technical Paper, Final Notebook, Video      | Aug 08–10   |

---

## 📦 Dataset

- **Name:** PTB-XL, a large, free, public collection of ECG recordings
- **Source:** [PhysioNet — PTB-XL v1.0.3](https://physionet.org/content/ptb-xl/1.0.3/)
- **Size:** 21,799 ECG recordings (10 seconds each) from 18,869 patients
- **Access:** Free and open — no application needed, just download it from PhysioNet
- **Note:** The raw files are large, so we don't upload them to this repo (see `.gitignore`). Download them yourself and put them in `data/raw/`.

### Downloading the Dataset

We provide a Python script to download the PTB-XL dataset from PhysioNet: `scripts/download_ptbxl.py`.

> **Note:** an earlier version of this script had two bugs that either crashed mid-download or silently
> saved corrupted (HTML) files instead of real data. Both are fixed as of this revision. If you downloaded
> data with an older copy of this script, delete `data/raw/` entirely and re-download following the steps
> below -- do not trust files downloaded before this fix without re-verifying them (step 4).

**1. Install required packages** (already covered by `requirements.txt`, `beautifulsoup4` is no longer needed):
```bash
pip install -r requirements.txt
```

**2. Download options:**

```bash
# Download first 100 patients (for quick testing)
python scripts/download_ptbxl.py --sample 100

# Download only metadata files (CSV files, no ECG data)
python scripts/download_ptbxl.py --metadata

# Download 100Hz records only, ALL 21,799 patients (recommended for this project)
python scripts/download_ptbxl.py --records100

# Download complete dataset (100Hz + 500Hz, all 21,799 patients, ~3 GB uncompressed)
python scripts/download_ptbxl.py --all
```

This can take a while (`--records100` downloads ~43,000 individual files). For a much faster bulk
download, especially if you only need `--records100`, use one of these instead and skip the script
entirely:

```bash
# Option A: AWS S3 sync (parallel, no AWS account needed, only pulls what you need)
pip install awscli
aws s3 sync --no-sign-request s3://physionet-open/ptb-xl/1.0.3/records100/ \
  data/raw/physionet.org/files/ptb-xl/1.0.3/records100/
aws s3 sync --no-sign-request s3://physionet-open/ptb-xl/1.0.3/ \
  data/raw/physionet.org/files/ptb-xl/1.0.3/ --exclude "*" \
  --include "ptbxl_database.csv" --include "scp_statements.csv"

# Option B: official single ZIP file (1.7 GB, includes both 100Hz and 500Hz)
curl -L -o ptbxl.zip https://physionet.org/content/ptb-xl/get-zip/1.0.3/
unzip ptbxl.zip -d data/raw/physionet.org/files/ptb-xl/1.0.3/
```

**3. What gets downloaded:**
- **Metadata files:** `ptbxl_database.csv` (~6.3 MB), `scp_statements.csv` (~9.7 KB)
- **ECG records:** `.dat` and `.hea` files
  - `_lr.dat` - Low Resolution (100 Hz) - recommended, smaller files
  - `_hr.dat` - High Resolution (500 Hz) - optional, 5x larger
- **Output location:** `data/raw/physionet.org/files/ptb-xl/1.0.3/` -- this is the *only* path any notebook reads from.

**4. Verify the download is real** (takes a few seconds, always do this before running any notebook):
```bash
ls -la data/raw/physionet.org/files/ptb-xl/1.0.3/ptbxl_database.csv   # should be ~6.3 MB, not a few hundred bytes
wc -l  data/raw/physionet.org/files/ptb-xl/1.0.3/ptbxl_database.csv   # should be ~21,800 lines
head -c 100 data/raw/physionet.org/files/ptb-xl/1.0.3/ptbxl_database.csv  # should look like real CSV, not "<html" or "version https://git-lfs..."
find data/raw/physionet.org/files/ptb-xl/1.0.3/records100 -name "*.dat" | wc -l  # should be 21,799 once fully downloaded
```
If any of those look wrong (tiny file size, HTML content, or a `git-lfs.github.com` pointer file instead
of real data), the download did not complete correctly -- delete `data/raw/` and re-download.

**5. Understanding the files:**
- **_lr.dat** (Low Resolution): 100 Hz sampling rate, ~10-12 KB per patient
- **_hr.dat** (High Resolution): 500 Hz sampling rate, ~50-60 KB per patient
- **.hea** (Header): Metadata for each .dat file

**Recommendation:** Use 100 Hz data (_lr.dat) for faster processing and sufficient accuracy for ML classification.

### Dataset Structure & Metadata

#### File Relationship:
```
ptbxl_database.csv (21,799 rows)
        ↓
    filename_lr column → "records100/00000/00001_lr"
        ↓
    Actual Files:
        ├─ 00001_lr.dat (Binary ECG signals: 12 leads × 1000 samples)
        └─ 00001_lr.hea (Text header: sampling rate, lead names, units)
```

#### ptbxl_database.csv - Complete Metadata (27 columns):

**Columns that link to files:**
- `filename_lr` - Path to 100 Hz .dat/.hea files (recommended)
- `filename_hr` - Path to 500 Hz .dat/.hea files (optional)

**Patient demographics:**
- `patient_id` - Patient identifier (multiple ECGs per patient possible)
- `age` - Patient age in years
- `sex` - 0=Female, 1=Male
- `height` - Patient height in cm
- `weight` - Patient weight in kg

**Recording context:**
- `ecg_id` - Unique ECG recording ID (CSV index)
- `recording_date` - Date and time of recording
- `nurse` - Nurse who performed recording
- `site` - Recording site/hospital
- `device` - ECG recording device

**Diagnostic information:**
- `scp_codes` - Diagnostic codes (SCP-ECG standard) - **used as labels for ML**
- `report` - Medical report text (German)
- `heart_axis` - Electrical heart axis
- `infarction_stadium1/2` - Infarction stages (if applicable)

**Signal quality indicators:**
- `baseline_drift` - Baseline wander present
- `static_noise` - Static noise present
- `burst_noise` - Burst noise present
- `electrodes_problems` - Electrode placement issues
- `extra_beats` - Extra heartbeats detected
- `pacemaker` - Pacemaker present

**Validation info:**
- `validated_by` - Cardiologist who validated
- `second_opinion` - Whether second opinion obtained
- `validated_by_human` - Human validation flag
- `initial_autogenerated_report` - Auto-generated report

**ML utilities:**
- `strat_fold` - Stratification fold (1-10) for cross-validation

**Key Point:** You need BOTH the CSV (for metadata & labels) AND the .dat/.hea files (for signals) for complete analysis.


## 📄 Reference Paper

Sadiq, M. T., et al. (2025). *Cardiac Arrhythmia Classification From Lead I ECG Recorded in a Free-Living Environment.* IEEE Journal of Biomedical and Health Informatics. https://ieeexplore.ieee.org/document/11259110

