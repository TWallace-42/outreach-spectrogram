try:
	import pyaudio
	import numpy as np
	import matplotlib.pyplot as plt
	import matplotlib.patches as plc
	import cv2
	import threading
except Exception as e:
    print("Something didn't import")
    print(e)

p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

FORMAT = pyaudio.paInt16 # We use 16bit format per sample
CHANNELS = 1
RATE = 16000
CHUNK = 512 # 1024bytes of data red from a buffer
RECORD_SECONDS = 0.1
WAVE_OUTPUT_FILENAME = "file.wav"

print("------------DEVICES------------")
for i in range(p.get_device_count()):
    print(p.get_device_info_by_index(i))
print("---------------------------")
audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=2)
                    #input_device_index=1)
                    #frames_per_buffer=CHUNK)

global keep_going
keep_going = True
n_avg = 10
average_colors = np.zeros((n_avg,4))
spectrogram_size = (150,300) #f_steps, time steps
spec_array = np.zeros(spectrogram_size)
max_v = 0.25
f = 3
def plot_data(in_data,i,spec_array):
	# get and convert the data to float
	audio_data = np.fromstring(in_data, np.int16)

	# Fast Fourier Transform, 10*log10(abs) is to scale it to dB
	# and make sure it's not imaginary

	dfft = np.abs(np.fft.rfft(audio_data,n = spectrogram_size[0]*4))
	dfft = np.resize(dfft,(spectrogram_size[0],1))

	spec_array = np.concatenate([spec_array,dfft],axis = 1)
	spec_array = spec_array[:,1:]
	
	spec_show = spec_array/np.max(spec_array)
	spec_show -= np.min(spec_show)
	spec_show = cv2.resize(spec_show,None,fx = f,fy = f)[::-1,:]

	spec_show = cv2.applyColorMap((255*spec_show).astype(np.uint8),cv2.COLORMAP_VIRIDIS)

	cv2.imshow("spectrogram",spec_show)

	#if the graph is stop-start then increase this
	cv2.waitKey(1)
	#print(dfft.shape)
	if keep_going:
		return (True,spec_array)
	else:
		return (False,spec_array)

# Open the connection and start streaming the data
stream.start_stream()
print("\n+---------------------------------+")
print("| Press Ctrl+C to Break Recording |")
print("+---------------------------------+\n")
audio_data = [None]
dfft_data = [None]

def read_audio(input_stream):
	audio_data[0] = np.fromstring(input_stream, np.int16)

def get_dfft(audio_input):
	dfft_data[0] = np.log10(np.abs(np.fft.rfft(audio_input,n = spectrogram_size[0]*4)))
	dfft_data[0] = np.resize(dfft_data[0],(spectrogram_size[0],1))


def load_file():
	ui= input()
	if "," in ui:
		fname,strength = ui.split(",")
	else:
		fname = ui
		strength = 1.
	
	print(f"loading {fname}")
	user_input[0] = fname
	user_input_strength[0] = float(strength)
	print(user_input_strength)
inject_data = np.zeros((spectrogram_size[0],1))
print(inject_data.shape)

#cv2.namedWindow("spectrogram")
#cv2.createButton("Test",load_file,None,cv2.QT_PUSH_BUTTON,1)

# Loop so program doesn't end while the stream callback's
# itself for new data
audio_thread = threading.Thread(target = read_audio,args = (stream.read(CHUNK,exception_on_overflow=False),))
audio_thread.start()

user_input = [None]
user_input_strength = [1]
injection_strength = 1
user_thread = threading.Thread(target = load_file)
user_thread.start()
injection = False
while keep_going:
	try:
		audio_thread.join()

		dfft_data = [None]
		dfft_thread = threading.Thread(target = get_dfft,args = (audio_data[0],))
		dfft_thread.start()
		
		audio_data= [None]
		audio_thread = threading.Thread(target = read_audio,args = (stream.read(CHUNK,exception_on_overflow=False),))
		audio_thread.start()
		
		dfft_thread.join()
		spec_array = np.concatenate([spec_array,dfft_data[0]+
		injection_strength*np.max(dfft_data[0])*inject_data[:,0][:,None]],axis = 1)
		if injection and inject_data.shape[1]>=2:
			inject_data = inject_data[:,1:]
		elif injection:
			injection = False
			print("Injection finished")
			inject_data = np.zeros((spectrogram_size[0],1))
			injection_strength = 1
		
		spec_array = spec_array[:,1:]

		spec_show = spec_array/np.max(spec_array)
		spec_show -= np.min(spec_show)
		spec_show = cv2.resize(spec_show,None,fx = f,fy = f)[::-1,:]

		spec_show = cv2.applyColorMap((255*spec_show).astype(np.uint8),cv2.COLORMAP_VIRIDIS)

		cv2.imshow("spectrogram",spec_show)

		#if the graph is stop-start then increase this
		cv2.waitKey(5)
		if user_input[0] is not None:
			try:
				inject_data = np.loadtxt("injections/" + user_input[0] + ".txt")
				injection_strength = user_input_strength[0]
				injection = True
				print("Beginning Injection")
			except:
				print(f"No such file as {user_input[0]}")
			user_input = [None]
			user_input_strength = [1]
			user_thread.join()
			user_thread = threading.Thread(target = load_file)
			user_thread.start()
		
	except KeyboardInterrupt:
		keep_going=False
	except Exception as e:
		print(e)
		pass

# Close up shop (currently not used because KeyboardInterrupt
# is the only way to close)
stream.stop_stream()
stream.close()

audio.terminate()
