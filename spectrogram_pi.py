
import soundcard as sc
import numpy as np
import scipy.signal as scipySignal
import matplotlib.pyplot as plt
import warnings
import time
import cv2
#warnings.simplefilter(category=sc.SoundcardRuntimeWarning,action = "ignore")
RATE = 16000#48000

CHUNK = 1024#2048
BUFFER = 20000

channel = 0 
mics = sc.all_microphones(include_loopback=True)
print("-----------------Detected Mics-------------")
print(mics)
print("------------------------------------------")
max_fft = 0.15
max_f = 300
cmap = plt.get_cmap('viridis')
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
#im = plt.imshow(spec_array,vmin = 0,vmax = max_fft,cmap = 'viridis')
#plt.gca().invert_yaxis()

audioIn = mics[2]
run = True
f= 3
with audioIn.recorder(samplerate=RATE) as mic:
    while run == True:

        data = mic.record(numframes=CHUNK)

        signal = np.sum(data, axis=1).real

        signal = scipySignal.detrend(signal)

        fft = np.abs(np.fft.fft(signal)) * 2 / (CHUNK // 2)
        fft = fft[:int(len(fft) / 2)]

        start = time.time()
        #im.set_clim(0,np.max(spec_array))
        spec_array = np.concatenate([spec_array,fft[:spectrogram_size[0],None]],axis = 1)
        spec_array = spec_array[:,1:]

        #spec_array[np.where(spec_array >= 0.001)] = np.log(spec_array[np.where(spec_array >= 0.001)])
        
        spec_show = spec_array/np.max(spec_array)
        spec_show = cmap(spec_show)
        
        spec_show = cv2.resize(spec_show,None,fx = f,fy = f)[::-1,:]
        spec_show[:,:,0],spec_show[:,:,2] = spec_show[:,:,2],spec_show[:,:,0]
        #print(spec_show.shape)
        cv2.imshow("spectrogram",spec_show)
        cv2.waitKey(1)
        #if not plt.fignum_exists(1):
        #    run = False
        
