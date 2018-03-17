import mne
import pandas as pd

data_path = 'E:\Wavelet_analysis\Analyzer_export'
raw_fname = data_path + '\Learning_S6_d5_M_Mult_wMarkers.dat'
vhdr_fname = data_path + '\Learning_S6_d5_M_Mult_wMarkers.vhdr'
#montage_fname = 'D:\Lisa\THESIS\DLproject\\127-channels-Tomsk.txt'

raw = mne.io.read_raw_brainvision(vhdr_fname, montage=None, misc = ['FCC4h'])
#montage_data = read_montage(kind='easycap-M1', path = 'D:\Lisa\THESIS\DLproject')
print(raw)
print(raw.info)
channels = pd.DataFrame(raw.info['chs'])
print(channels)

#read_montage(kind='easycap-M1', path = 'D:\Lisa\THESIS\DLproject')
"""
print(raw.ch_names)

start, stop = raw.time_as_index([100, 115])  # 100 s to 115 s data segment
data, times = raw[:, start:stop]
print(data.shape)
print(times.shape)
data, times = raw[2:20:3, start:stop]  # access underlying data
raw.plot()
"""