
import soundcard as sc
import numpy as np
import scipy.signal as scipySignal
import matplotlib.pyplot as plt
import warnings

warnings.simplefilter(category=sc.SoundcardRuntimeWarning,action = "ignore")
RATE = 48000

CHUNK = 2048
BUFFER = 20000

channel = 0 
mics = sc.all_microphones(include_loopback=True)
max_fft = 0.15
max_f = 300
# x = np.arange(1024)
# y = np.zeros(1024)
# li = plt.plot(x,y)[0]
# plt.ion()
# plt.ylim(0,max_fft)
# plt.xlim(0,max_f)
# plt.show()

# audioIn=mics[int(input("Choose input device: "))]
spectrogram_size = (150,300) #f_steps, time steps
spec_array = np.zeros(spectrogram_size)
im = plt.imshow(spec_array,vmin = 0,vmax = max_fft,cmap = 'viridis')
plt.gca().invert_yaxis()

audioIn = mics[1]
run = True
with audioIn.recorder(samplerate=RATE) as mic:
    while run == True:
        # start = time.time()
        data = mic.record(numframes=CHUNK)

        signal = np.sum(data, axis=1).real

        signal = scipySignal.detrend(signal)
        fft = np.abs(np.fft.fft(signal)) * 2 / (CHUNK // 2)
        fft = fft[:int(len(fft) / 2)]
        im.set_clim(0,np.max(spec_array))
        spec_array = np.concatenate([spec_array,fft[:spectrogram_size[0],None]],axis = 1)
        spec_array = spec_array[:,1:]
        im.set_data(spec_array)
        plt.pause(0.001)
        if not plt.fignum_exists(1):
            run = False
        