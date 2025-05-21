
from gwpy.timeseries import TimeSeries
import numpy as np
import matplotlib.pyplot as plt
from gwosc.datasets import event_gps

gps = event_gps("GW150914")
print(gps)
start = int(gps) - 90
end = int(gps) + 90
gwdata = TimeSeries.fetch_open_data(
    "L1",
	start,
	end,
    verbose = True,
    sample_rate = 16384,
)

gwdata.plot()
plt.show()
specgram = gwdata.spectrogram(2, fftlength=1, overlap=0.5) ** (1/2.)
spec_array = np.array(specgram)
fmin = specgram.y0
fmax = specgram.y0 + spec_array.shape[1]*specgram.dy

# 0-8kHz is the spectrogram programme
# 300 frequency bins
# 75 for 2000Hz
# assume fmin = 0 always
spec_height = 300
spec_fmin = 8000
new_time = None
if new_time is None:
	new_time = spec_array.shape[0]
n_bins_covered = float(fmax.value)/(spec_fmin/spec_height) #max spec Hz/spectrogram height

spec_small = np.resize(spec_array,(int(np.ceil(n_bins_covered)),new_time))
print(np.min(spec_small),np.max(spec_small))
spec_small = np.log10(spec_small)
spec_small -= np.min(spec_small)
spec_small /= np.max(spec_small)
empty_diff = np.zeros((spec_height - spec_small.shape[1],new_time))
print(spec_small.shape,empty_diff.shape)
spec_full = np.concatenate([spec_small[:,:],empty_diff],axis = 0)

#spec_full = np.log10(spec_full)


plt.imshow(spec_full)
plt.gca().invert_yaxis()
plt.show()
file_name = "150914.txt"
savename = f"injections/{file_name.replace('.jpeg','.txt').replace('.png','.txt')}"
np.savetxt(savename,spec_full)
