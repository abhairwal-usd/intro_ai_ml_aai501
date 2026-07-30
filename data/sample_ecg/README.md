# Bundled ECG Sample (100 patients)

This folder contains 100 real PTB-XL ECG recordings (`records100_sample/000/`, ecg_id 00001–00100,
100Hz, `.dat`/`.hea` WFDB format) checked into the repo so you can smoke-test the notebooks and scripts
without waiting for the full ~21,799-record download.

**This is not the dataset the notebooks read from.** `01_Data_Prepare_EDA/01_data_exploration.ipynb` and
every other notebook read from `data/raw/physionet.org/files/ptb-xl/1.0.3/`, which you get by running
`scripts/download_ptbxl.py` (see the main README's "Downloading the Dataset" section) -- not from this folder.

Use this sample only for quick, local checks, e.g. confirming `wfdb.rdsamp()` can read a record, or testing
a snippet of cleanup logic against real signals before running it against the full dataset.

Note: one record in this sample (ecg_id 00046) is missing its `.dat` file on purpose -- useful for testing
missing-file handling, since PhysioNet's real dataset occasionally has this too.
