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
This should run relatively simply as `python run_spectrogram.py`. To input injections you simply type the name of the injection file
(without .txt or injection/) and it will find the file in the directory and input it into the live feed.


## How to close
Like all the best programs this isn't easy to close. Basically just hit Ctrl + C in the terminal window and that will close the stream and window

## Common Issues
If you are seeing a totally black (or white) output there's a chance you aren't using the correct device index. 
By running `pyaudio_device_list.py` you should get a list of devices for troubleshooting.



# injection_maker.py
This turns standard png/jpg/jpeg images into txt arrays that can be injected into the spectrogram.

to run in the command line you can try:

```
python injection_maker.py <file_name>.png/.jpg/.jpeg 
```

There are various options but the main one is the flag `-i` which will invert the grayscale image. At the moment
we can only do .png, .jpg, and .jpeg but this is mostly just laziness on my end.

# pyaudio_device_list.py
Lists devices found by pyaudio. Useful for discovering new things. The main information tends to be at the bottom, work
to be done on tidying the output of this but for now it is serviceable.

Can be run with `python pyaudio_device_list.py` then choose the relevant device index and input it in `run_spectrogram.py`
's audio.open as the `input_device_index`:

```python
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=<HERE>)
```

# TODO
[x] Finish README.md
[x] Tidy injection_maker.py
[x] Make injection_maker.py run in command line
[ ] Injection Sound File maker
[ ] Figure out why there's strange low frequency artifacts
[ ] Calculate FFT frequencies to display
[ ] log colormap
[ ] Tidy the device output of `pyaudio_device_list.py`
[ ] Simplify window closing
[ ] Spectrogram Reset command 

