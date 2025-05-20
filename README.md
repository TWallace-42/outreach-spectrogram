# Outreach Spectrogram
A very basic spectrogram that, in theory, has room to grow and improve.
In fact, it has a very large amount of room. Any questions or issues please
email Thomas Wallace at t.wallace.1@research.gla.ac.uk.

This README will be a very basic guide into the usage and todo list of the repo
as well as some basic troubleshooting.

The main goal of this project is to have a real time spectrogram that we can 
have output standard audio inputs to a raspberry-pi3. Additionally it would
be nice if we could show injections.

Below I will detail each individual file, how it's run, and then at the bottom a large TODO list

# run_spectrogram.py

# injection_maker.py
This turns standard png/jpg/jpeg images into txt arrays that can be injected into the spectrogram.

to run in the command line you can try:

```
python injection_maker.py <file_name>.png/.jpg/.jpeg 
```

There are various options but the main one is the flag `-i` which will invert the grayscale image.

# pyaudio_device_list.py


# TODO
[ ] Finish README.md
[x] Tidy injection_maker.py
[x] Make injection_maker.py run in command line
[ ] Injection Sound File maker
[ ] Figure out why there's strange low frequency artifacts
[ ] Calculate FFT frequencies to display
[ ] log colormap


