# ECG Arrhythmia Classification Using Machine Learning

## Project Description

This project focuses on developing and comparing multiple machine learning algorithms for automated ECG-based cardiac arrhythmia classification using the PTB-XL dataset. The project implements a comprehensive end-to-end machine learning pipeline including data preprocessing, exploratory analysis, baseline and advanced model development, hyperparameter optimization, and comparative evaluation using clinical performance metrics.

## Project Context and Goal

### Context

Electrocardiogram (ECG) analysis is crucial for diagnosing cardiac conditions, but manual interpretation is time-consuming and requires specialized expertise. Automated ECG classification using machine learning can assist clinicians in rapid and accurate diagnosis of cardiac arrhythmias and other heart conditions.

### Goal

The primary goal is to:
1. Develop and compare multiple ML/DL algorithms (Random Forest, XGBoost) for multi-class ECG classification
2. Implement comprehensive data preprocessing and feature engineering for 12-lead ECG signals
3. Perform time series analysis and signal decomposition
4. Optimize models through hyperparameter tuning and handle class imbalance
5. Evaluate models using clinical metrics (Sensitivity, Specificity, ROC-AUC, Precision-Recall)
6. Identify the best-performing approach for ECG arrhythmia classification

### Dataset

- **Name**: PTB-XL ECG Database (v1.0.3)
- **Source**: [PhysioNet](https://physionet.org/content/ptb-xl/1.0.3/)
- **Size**: 21,799 clinical 12-lead ECG records from 18,869 patients
- **Format**: WFDB format with 16-bit precision
- **Sampling Rates**: 500 Hz (high resolution) and 100 Hz (downsampled)
- **Patient Demographics**: Ages 0-95 years (median: 62), 52% male, 48% female
- **Annotations**: Up to 71 standardized diagnostic statements (SCP-ECG standard)
- **Pathologies**: Normal ECGs, myocardial infarction, ST/T changes, conduction disturbances, hypertrophy
- **License**: Creative Commons Attribution 4.0 International

**Research Paper**: [ECG Arrhythmia Classification](https://ieeexplore.ieee.org/document/11259110)

## Repository Structure

```
intro_ai_ml_aai501/
├── 01_Data_Prepare_EDA/            # PART 1: Data Preparation & EDA
├── 02_Model_Selection_n_Building/  # PART 2: Model Selection & Building
├── 03_Model_Diagnostics/           # PART 3: Model Diagnostics
├── 04_Final/                       # PART 4: Final Report & Delivery
├── data/                           # Dataset storage
└── README.md                       # This file
```

## Team Roles and Responsibilities

| Team Member | Primary Responsibilities | Project Parts |
|-------------|-------------------------|---------------|
| **Ashok Bhairwal** | • Data preprocessing and cleaning<br>• Exploratory data analysis (EDA)<br>• Time series decomposition<br>• Technical paper writing<br>• Repository management and documentation | PART 1, PART 4 |
| **Diaesh Antony** | • Baseline model implementation (Logistic Reg, RF, Decision Tree)<br>• Advanced model development (XGBoost)<br>• Hyperparameter tuning and optimization<br>• Model training and validation<br>• Peer evaluation coordination | PART 2, PART 4 |
| **N L N Sai Krishna Akula** | • Model performance evaluation and diagnostics<br>• ROC-AUC and Precision-Recall analysis<br>• Feature importance and interpretability (SHAP, Grad-CAM)<br>• Comparative model analysis<br>• Technical paper writing | PART 3, PART 4 |

### Collaborative Responsibilities (All Members)
- Literature review and proposal development (PART 1)
- Final presentation and video recording (PART 4)
- Peer evaluation and team coordination (PART 4)

---

*Course: AAI-501 - Introduction to AI and Machine Learning*  
*Program: MS in Applied Artificial Intelligence, University of San Diego*  
*Last Updated: 2026-07-20*
