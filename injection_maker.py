import numpy as np
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
#freq = 30

#spectrogram_size = (150,100) #freqs, length
#injection = np.zeros(spectrogram_size)
#injection[freq] = 1.
#np.savetxt("injections/test.txt",injection)

def make_igr(invert = False):
	spectrogram_size = (150,150) 
	logo = Image.open("IGR_logo.jpg").resize((spectrogram_size[0],spectrogram_size[1])).transpose(Image.FLIP_TOP_BOTTOM)
	grey_logo = ImageOps.grayscale(logo)
	logo_arr = np.array(grey_logo)/255
	if invert:
		logo_arr = 1-logo_arr
		savename = "injections/igr_invert.txt"
	else:
		savename = "injections/igr.txt"
	np.savetxt(savename,logo_arr)
	
make_igr()
make_igr(True)
