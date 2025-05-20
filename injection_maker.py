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
	logo = Image.open("IGRlogo_black.png").resize((int(spectrogram_size[0]),int(spectrogram_size[1]))).transpose(Image.FLIP_TOP_BOTTOM)

	grey_logo = ImageOps.grayscale(logo)
	logo_arr = np.array(logo)/255 #use grey_logo if not transparency issues
	if len(logo_arr.shape) > 2:
		logo_arr = logo_arr[:,:,3]
	
	if invert:
		logo_arr = 1-logo_arr
		savename = "injections/igr_invert2.txt"
	else:
		savename = "injections/igr2.txt"
	np.savetxt(savename,logo_arr)
	
make_igr()
make_igr(True)
