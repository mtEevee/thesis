import mne
import pandas as pd
import pathlib

data_path = 'E:\Wavelet_analysis\Analyzer_export'
raw_fname = data_path + '\Learning_S6_d5_M_Mult_wMarkers.dat'
vhdr_fname = data_path + '\Learning_S6_d5_M_Mult_wMarkers.vhdr'

#read all vhdr wMarkers
#for vhdrFiles in pathlib.Path(data_path).glob('*wMarkers.vhdr'):
    #raw = mne.io.read_raw_brainvision(vhdrFiles, montage=None, misc = ['FCC4h'])
    #events = mne.read_events(vhdrFiles)

raw = mne.io.read_raw_brainvision(vhdr_fname, montage=None, eog=['VEOG'], misc=['FCC4h'])
raw.set_eeg_reference()
#data, times = raw[:]
channels = pd.DataFrame(raw.info['ch_names'])
events = mne.find_events(raw, stim_channel='STI 014')
#print(raw)
print(raw.info)
#print(channels)
#print('STI 014')


