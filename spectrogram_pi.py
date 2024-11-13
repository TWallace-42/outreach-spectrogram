import soundcard as sc
import numpy as np
import scipy.signal as scipySignal
import matplotlib.pyplot as plt
import warnings
import time
import cv2
import threading

#warnings.simplefilter(category=sc.SoundcardRuntimeWarning,action = "ignore")
RATE = 16000#48000

CHUNK = 1024#2048
BUFFER = 4096

channel = 0 
mics = sc.all_microphones(include_loopback=True)
print("-----------------Detected Mics-------------")
print(mics)
print("------------------------------------------")
max_fft = 0.15
max_f = 300
max_v = 0.25 #maximum pixel value
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

audioIn = mics[0]
run = True
f= 3

#get audio as a function so we can thread it
def get_audio(mic,data):
        data[0] = mic.record(numframes=CHUNK)

def get_fft(data,fft):
        signal = np.sum(data, axis=1).real

        signal = scipySignal.detrend(signal)

        fft_ = np.abs(np.fft.fft(signal)) * 2 / (CHUNK // 2)
        fft_ = fft_[:int(len(fft_) / 2)]
        fft[0]=fft_
        #return(fft)
data_output = [None]
fft_output = [None]
with audioIn.recorder(samplerate=RATE) as mic:
    data_output = [None]

    audio_thread = threading.Thread(target = get_audio,args = (mic,data_output))
    audio_thread.start()
    while run == True:
        #get latest data
        audio_thread.join()
        #create fft thread
        fft_output = [None]
        fft_thread = threading.Thread(target = get_fft,args = (data_output[0],fft_output))
        fft_thread.start()
        #create new audio thread (while fft runs?)
        data_output = [None]
        audio_thread = threading.Thread(target = get_audio,args = (mic,data_output))
        
        #get new fft data
        fft_thread.join()

        fft_output = fft_output[0]
        spec_array = np.concatenate([spec_array,fft_output[:spectrogram_size[0],None]],axis = 1)
        spec_array = spec_array[:,1:]
        spec_array[np.where(spec_array>max_v)] = max_v
        audio_thread.start()
        spec_show = spec_array/np.max(spec_array)

        spec_show = cv2.resize(spec_show,None,fx = f,fy = f)[::-1,:]

        spec_show = cv2.applyColorMap((255*spec_show).astype(np.uint8),cv2.COLORMAP_VIRIDIS)

        cv2.imshow("spectrogram",spec_show)
        
        #if the graph is stop-start then increase this
        cv2.waitKey(60)
        
