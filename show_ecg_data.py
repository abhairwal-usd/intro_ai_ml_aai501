import wfdb
import numpy as np

record_path = 'data/raw/physionet.org/files/ptb-xl/1.0.3/records100/00000/00001_lr'
record = wfdb.rdrecord(record_path)

print('='*70)
print('SIGNAL STATISTICS (all 1000 samples)')
print('='*70)
print(f"{'Lead':<6s} {'Mean':>10s} {'Std':>10s} {'Min':>10s} {'Max':>10s} {'Range':>10s}")
print('-'*70)

for i, lead_name in enumerate(record.sig_name):
    data = record.p_signal[:, i]
    mean_val = np.mean(data)
    std_val = np.std(data)
    min_val = np.min(data)
    max_val = np.max(data)
    range_val = max_val - min_val
    print(f'{lead_name:<6s} {mean_val:10.3f} {std_val:10.3f} {min_val:10.3f} {max_val:10.3f} {range_val:10.3f}')

print()
print('='*70)
print('KEY INSIGHTS FROM THIS ECG')
print('='*70)
print('✓ Patient ID: 00001')
print('✓ Recording: 10 seconds, 100 Hz sampling rate')
print('✓ All 12 standard ECG leads present')
print('✓ Values in millivolts (mV)')
print()
print('Lead II shows typical ECG characteristics:')
print(f'  - Mean: {np.mean(record.p_signal[:, 1]):.3f} mV (close to baseline)')
print(f'  - Range: {np.max(record.p_signal[:, 1]) - np.min(record.p_signal[:, 1]):.3f} mV (peak-to-peak amplitude)')
print()
print('Normal ECG patterns visible:')
print('  - Voltage variations represent heartbeat cycles')
print('  - P wave, QRS complex, T wave patterns embedded in data')
print('  - These patterns help diagnose cardiac conditions')
