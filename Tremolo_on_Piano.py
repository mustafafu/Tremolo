# DSP Lab - Project
# Tremolo Effect on Synthetic Piano
# Hashem Khalifeh & Mustafa F. Ozkoc

import pyaudio, struct
import numpy as np
from scipy import signal
from math import sin, cos, pi
import tkinter as Tk

BLOCKLEN   = 64        # Number of frames per block
WIDTH       = 2         # Bytes per sample
CHANNELS    = 1         # Mono
RATE        = 8000      # Frames per second

MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)
output = [0] * BLOCKLEN
m = [0] * BLOCKLEN

# Parameters
Ta = 2      # Decay time (seconds)
f0 = 400    #first harmonic frequency (Hz)
f = 2**(np.arange(12)/12)*f0

# Pole radius and angle
r = 0.01**(1.0/(Ta*RATE))       # 0.01 for 1 percent amplitude
om = 2.0 * pi * f/RATE

# Filter coefficients (second-order IIR)
a = np.array([np.ones(om.shape), -2*r*np.cos(om), r**2 * np.ones(om.shape)])
b = np.array([r*np.sin(om)])
ORDER = 2   # filter order
states = np.zeros([ORDER,om.shape[0]])
x = np.zeros([BLOCKLEN,om.shape[0]])
y = np.zeros([BLOCKLEN,om.shape[0]])
z = np.zeros([BLOCKLEN, om.shape[0]])

# Open the audio output stream
p = pyaudio.PyAudio()
PA_FORMAT = pyaudio.paInt16
stream = p.open(
    format      = PA_FORMAT,
    channels    = CHANNELS,
    rate        = RATE,
    input       = False,
    output      = True,
    frames_per_buffer = 128)
# specify low frames_per_buffer to reduce latency

CONTINUE = True
KEYPRESS = False
WHICHNOTE = 0

# note mapping dictionary
my_dict = {'z': 0, 's': 1, 'x': 2, 'd': 3, 'c': 4, 'v': 5, 'g': 6, 'b': 7, 'h': 8, 'n': 9, 'j': 10, 'm': 11,'q': 9999}

def my_function(event):
    global CONTINUE
    global WHICHNOTE
    print('You pressed ' + event.char)
    if event.char == 'q':
        print('Good bye')
        CONTINUE = False
        root.destroy()
        root.quit()
    WHICHNOTE = my_dict[event.char]
    global x
    if WHICHNOTE < 12:
        x[0,WHICHNOTE] = 10000

root = Tk.Tk()

# Define Tk variables
f1 = Tk.DoubleVar()
gain = Tk.DoubleVar()
waveform = Tk.StringVar()

# Initialize Tk variable
f1.set(5)
gain.set(0)

# Define Widgets
S1 = Tk.Scale(root, label = 'Frequency', variable = f1, from_ = 5, to = 20, tickinterval = 1)
S2 = Tk.Scale(root, label= 'Gain', variable = gain, from_ = 0, to = 1, digits = 2, resolution = 0.1)

# Place widgets
S1.pack()
S2.pack()

root.bind("<Key>", my_function)

print('Press keys for sound.')
print('Press "q" to quit')

theta = 0

while CONTINUE:
    root.update()

    for jj in np.arange(om.shape[0]):
        [y[:,jj], states[:,jj]] = signal.lfilter(b[:,jj], a[:,jj], x[:,jj], zi = states[:,jj])
        z

    x[0,:] = 0.0
    z = y.sum(1)
    om1 = 2.0 * pi * f1.get() / RATE
    for i in range(0, BLOCKLEN):
      m[i] = 1 + gain.get()*sin(theta)
      output[i] = int(z[i] * m[i])
      theta = theta + om1
    while theta > pi:
      theta = theta - 2.0 * pi
    output = np.clip(output, -MAXVALUE, MAXVALUE)     # Clipping
    binary_data = struct.pack('h' * BLOCKLEN, *output);    # Convert to binary binary data
    stream.write(binary_data, BLOCKLEN)               # Write binary binary data to audio output

print('* Done.')

# Close audio stream
stream.stop_stream()
stream.close()
p.terminate()