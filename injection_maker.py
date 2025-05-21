import numpy as np
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import os
from argparse import ArgumentParser


def create_dir(*PATHS):
	for p in PATHS:
		components = p.split("/")
		for i,_ in enumerate(components):
			new_dir = "/".join(components[:i+1]) + "/"
			if not os.path.isdir(new_dir):
				os.makedirs(new_dir)
				print(f"Created: {new_dir}")

def make_injection(file_name,invert = False,spectrogram_size = (150,150)):
	#the size of image on the spectrogram,
	# if I remember correctly the size is set to the same as the spectrogram in 
	# run_spectrogram.py so that might need hardcoded
	create_dir("injections/")
	spectrogram_size = (150,150) 
	#load image
	logo = Image.open(file_name).resize((int(spectrogram_size[0]),int(spectrogram_size[1]))).transpose(Image.FLIP_TOP_BOTTOM)
	#greyscale
	grey_logo = ImageOps.grayscale(logo)
	
	logo_arr = np.array(logo)/255 
	#use grey_logo if not transparency issues
	if len(logo_arr.shape) > 2:
		
		logo_arr = logo_arr[:,:,0]
	
	if invert:
		logo_arr = 1-logo_arr
	savename = f"injections/{file_name.replace('.jpeg','.txt').replace('.png','.txt')}"
	#save
	np.savetxt(savename,logo_arr)
	print(f"injection saved in {savename}")
if __name__ == "__main__":
	parser = ArgumentParser(prog = "injection_maker.py",
			description = "Creates injection arrays for inputing to the spectrogram",
			epilog = "If there are any questions and comments please email t.wallace.1@research.gla.ac.uk")
	parser.add_argument("filename",help = "file to turn into an injection")
	parser.add_argument("-i","--invert",help = "Whether to invert the values of the array",
	action = "store_true")
	parser.add_argument("-s","--spec_size",
	help = "Size of spectrogram, by default will assume the injection should be square",
	type = int,default = 150)
	args = parser.parse_args()
	make_injection(file_name = args.filename,
				invert = args.invert,
				spectrogram_size = (args.spec_size,args.spec_size))
				
