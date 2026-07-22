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
ECG-Arrhythmia-Classification-Team-Project/
├── README.md
├── requirements.txt
├── .gitignore
├── .gitattributes
├── data/
│   ├── raw/                      # Unmodified PTB-XL source files (not committed — see .gitignore)
│   └── processed/                # Cleaned / resampled / feature-engineered data
├── 01_Data_Prep_EDA/              # Data cleaning + exploratory data analysis
├── 02_Model_Selection/            # Feature engineering, baseline model, advanced model
├── 03_Model_Analysis_Diagnostics/ # Intra- vs inter-patient diagnostics, ROC/AUC, confusion matrices
└── 04_Master_Pipeline/            # Final end-to-end notebook, technical paper, presentation
```

Each folder will hold its own notebook(s) and finished report files as the project moves forward.

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

## 📄 Reference Paper

Sadiq, M. T., et al. (2025). *Cardiac Arrhythmia Classification From Lead I ECG Recorded in a Free-Living Environment.* IEEE Journal of Biomedical and Health Informatics. https://ieeexplore.ieee.org/document/11259110

---

## Setup

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
