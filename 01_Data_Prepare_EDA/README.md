# Part 1: Data Preparation & EDA

**Course:** AAI-501 - Introduction to AI and Machine Learning  
**Project:** ECG Arrhythmia Classification Using Machine Learning  
**Responsible:** Ashok Bhairwal

## Overview

This directory contains all work related to Part 1 of the project: Data Preparation and Exploratory Data Analysis of the PTB-XL ECG Database.

## Contents

### Scripts and Notebooks

1. **[00_download_dataset.py](00_download_dataset.py)**
   - Downloads PTB-XL dataset from PhysioNet
   - Extracts and verifies dataset integrity
   - ~1.7 GB download, ~3.0 GB extracted
   - Run: `python 00_download_dataset.py`

2. **[01_data_exploration.ipynb](01_data_exploration.ipynb)**
   - Initial dataset exploration
   - Patient demographics analysis
   - Diagnostic label distribution
   - Signal quality assessment
   - Sample ECG visualization
   - **Output:** `data/preprocessed/metadata_with_labels.csv`

3. **[02_data_preprocessing.ipynb](02_data_preprocessing.ipynb)**
   - ECG signal preprocessing pipeline
   - Baseline wander removal (high-pass filter 0.5 Hz)
   - Bandpass filtering (0.5-40 Hz)
   - Z-score normalization
   - Quality control
   - **Outputs:**
     - `data/preprocessed/X_preprocessed.npy` (preprocessed signals)
     - `data/preprocessed/y_labels.npy` (labels)
     - `data/preprocessed/ecg_ids.npy` (identifiers)
     - `data/preprocessed/metadata_processed.csv`

4. **[03_time_series_decomposition.ipynb](03_time_series_decomposition.ipynb)**
   - Classical time series decomposition (Trend + Seasonal + Residual)
   - Wavelet decomposition (Daubechies db4, 5 levels)
   - Frequency domain analysis (FFT, Power Spectral Density)
   - Feature extraction:
     - Time-domain features (statistics, energy, zero crossings)
     - Frequency-domain features (spectral centroid, entropy, power bands)
     - Wavelet features (energy at each decomposition level)
     - Morphological features (heart rate, R-R intervals, HRV)
   - **Output:** `data/features/extracted_features_lead2.csv`

5. **[04_exploratory_data_analysis.ipynb](04_exploratory_data_analysis.ipynb)**
   - Feature distribution analysis
   - Statistical tests (ANOVA) for discriminative features
   - Correlation analysis
   - Dimensionality reduction (PCA, t-SNE)
   - Class separability visualization
   - Insights and recommendations for modeling

## Data Flow

```
PhysioNet
    ↓
[00_download_dataset.py]
    ↓
data/raw/ptb-xl/
    ↓
[01_data_exploration.ipynb]
    ↓
data/preprocessed/metadata_with_labels.csv
    ↓
[02_data_preprocessing.ipynb]
    ↓
data/preprocessed/X_preprocessed.npy
data/preprocessed/y_labels.npy
    ↓
[03_time_series_decomposition.ipynb]
    ↓
data/features/extracted_features_lead2.csv
    ↓
[04_exploratory_data_analysis.ipynb]
    ↓
Insights for Part 2 (Model Building)
```

## Key Findings

### Dataset Characteristics
- **21,799 ECG records** from 18,869 patients
- **12-lead ECGs**, 10-second duration, 100/500 Hz sampling rates
- **5 diagnostic superclasses:** NORM, MI, STTC, CD, HYP
- **Class imbalance:** NORM (~9,500) > HYP (~2,600)

### Signal Quality
- Some records have quality issues (noise, baseline drift, electrode problems)
- Preprocessing pipeline successfully handles most quality issues
- Preprocessed signals: mean ≈ 0, std ≈ 1 (normalized)

### Feature Extraction
- Extracted **40+ features** per ECG lead
- Categories: time-domain, frequency-domain, wavelet, morphological
- Top discriminative features: heart rate, morphological, frequency features

### Dimensionality Reduction
- **95% variance** captured by ~20-30 PCA components (from 40+ features)
- PCA shows partial class separation
- t-SNE reveals clustering patterns

### Recommendations for Modeling
1. Address class imbalance (SMOTE, class weights)
2. Use ensemble methods (Random Forest, XGBoost)
3. Implement stratified cross-validation
4. Consider multi-label classification approach
5. Feature selection to reduce dimensionality

## Requirements

```bash
pip install -r ../requirements.txt
```

Key packages:
- `numpy`, `pandas` - Data manipulation
- `matplotlib`, `seaborn`, `plotly` - Visualization
- `wfdb` - ECG data reading
- `scipy`, `statsmodels` - Signal processing, statistics
- `scikit-learn` - ML preprocessing, PCA, scaling
- `pywt` - Wavelet decomposition

## How to Run

### Step 1: Download Dataset
```bash
cd 01_Data_Prepare_EDA
python 00_download_dataset.py
```

### Step 2: Run Notebooks in Order
1. Open Jupyter: `jupyter notebook`
2. Execute notebooks sequentially:
   - `01_data_exploration.ipynb`
   - `02_data_preprocessing.ipynb`
   - `03_time_series_decomposition.ipynb`
   - `04_exploratory_data_analysis.ipynb`

### Notes:
- Processing all 21,799 records takes time (set `PROCESS_ALL = True` in notebooks)
- For quick testing, notebooks default to 1,000 samples
- Preprocessed data is saved incrementally

## Output Summary

| File | Location | Size | Description |
|------|----------|------|-------------|
| Raw dataset | `data/raw/ptb-xl/` | ~3.0 GB | Original PTB-XL data |
| Preprocessed signals | `data/preprocessed/X_preprocessed.npy` | Variable | Filtered & normalized ECG signals |
| Labels | `data/preprocessed/y_labels.npy` | Small | Multi-label targets |
| Extracted features | `data/features/extracted_features_lead2.csv` | ~MB | Time/freq/wavelet/morphological features |

## Next Steps

**Part 2: Model Selection & Building** (Diaesh Antony)
- Implement baseline models (Logistic Regression, Random Forest, Decision Tree)
- Develop advanced models (XGBoost)
- Hyperparameter tuning
- Model training and validation

## References

1. **PTB-XL Dataset:**  
   Wagner et al. (2020). PTB-XL, a large publicly available electrocardiography dataset.  
   *Scientific Data*, 7(1), 1-15. https://doi.org/10.1038/s41597-020-0495-6

2. **PhysioNet:**  
   https://physionet.org/content/ptb-xl/1.0.3/

---

*Part 1 completed by Ashok Bhairwal - Last updated: 2026-07-21*
