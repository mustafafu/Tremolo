""" DSP Lab Project - Tremolo Effect on Synthetic Piano
Hashem Khalifeh & Mustafa F. Ozkoc """


import pyaudio, struct
import numpy as np
from scipy import signal
from math import sin, cos, pi
from tkinter import *


BLOCKLEN   = 64        # Number of frames per block
WIDTH       = 2         # Bytes per sample
CHANNELS    = 1         # Mono
RATE        = 8000      # Frames per second
MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)

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
output = [0] * BLOCKLEN
m = [0] * BLOCKLEN


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

# Key note generating function
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


# Function to create On/Off toggle button
status = 0
def toggle(tog=[0]):
    tog[0] = not tog[0]
    global status
    if tog[0]:
        t_btn.config(text='ON', font = 'Times 10 bold', foreground = 'green', relief = 'raised')
        status = 1
    else:
        t_btn.config(text='OFF', font = 'Times 10 bold', foreground = 'red', relief = 'sunken')
        status = 0


root = Tk()

# Define Tkinter variables
f1 = DoubleVar()
gain = DoubleVar()
waveform = StringVar()

# Initialize Tk Variables
f1.set(5)
gain.set(0)

root.configure(background = 'gray90')

# Define Widgets
Label(root, text='Tremolo Effect on Synthetic Piano', font = 'Times 16 bold', background = 'gray90').grid(row=0, column=2)

# Frequency Scale
Scale(root, label = 'Frequency', variable = f1, from_ = 5, to = 10, resolution = 1, font = 'fixedsys 10',
      background = 'gray90', foreground = 'black').grid(row=1, column=0)

# Gain Scale
Scale(root, label= 'Gain', variable = gain, from_ = 0, to = 1, digits = 2, resolution = 0.1, font = 'fixedsys 10',
      background = 'gray90', foreground = 'black').grid(row=1, column=4)

# On/Off Button
t_btn = Button(text="OFF", font = 'Times 10 bold', foreground = 'red', width=6, command=toggle, relief = 'sunken')
t_btn.grid(row=1, column=2)

# Wave Type
sinimage = PhotoImage(file = 'DSPProject/sine.png')
Radiobutton(root, value=1, image = sinimage, background = 'gray90').grid(row=3, column=1)
triimage = PhotoImage(file = 'DSPProject/triangle.png')
Radiobutton(root, value=2, image = triimage, background = 'gray90').grid(row=3, column=2)
squareimage = PhotoImage(file = 'DSPProject/square.png')
Radiobutton(root, value=3, image = squareimage, background = 'gray90').grid(row=3, column=3)


root.bind("<Key>", my_function)

print('Press keys for sound.')
print('Press "q" to quit')

theta = 0
om1 = 2.0 * pi * f1.get() / RATE

while CONTINUE:
    root.update()

    for jj in np.arange(om.shape[0]):
        [y[:,jj], states[:,jj]] = signal.lfilter(b[:,jj], a[:,jj], x[:,jj], zi = states[:,jj])

    x[0,:] = 0.0
    z = y.sum(1)
    for i in range(0, BLOCKLEN):
      m[i] = 1 + status*gain.get()*sin(theta)
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





