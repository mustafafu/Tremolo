# Tremolo
Tremolo Effect on Synthetic Piano
# Introduction
Tremolo effect is used in different kinds of music ranging from surf to punk. It achieves a trembling effect on the played notes. It mimics the playing of fast repeated notes generally used in violin, guitar, rolls on a percussion instrument or in our case on a piano sound.The tremolo effect simulates this repeated notes playing style by periodically modulating the amplitude of an input signal. Long sustained notes come out as short rapid repetitive notes. The tremolo was built into some guitar amplifiers as early as 1940s [1].

# Details
There are 3 different type of variations in tremolo effect. One can vary the low frequency of the effect i.e in a range from 1-5Hz which represents 1-5 beats per second. Similarly one can vary the amplitude of the modulating signal which in result will give a deeper or smoother sounding output signal. Moreover, one can choose a different wave type such as triangle, square or a sinusoidal wave. Which makes the modulation waveform sharper or softer. Sine waves are rounded wave-forms that provide a lush, strong tremolo, while a triangle wave, with its straight, linear rise and fall, creates peaks and valleys that can command attention and cut through a mix [2].

# Proposed Program
We will build a program with a GUI to control the options given in section \ref{sec:Details}. A user can turn on and off the effect. Moreover with sliders user can adjust the modulation rate and the amplitude of the modulating signal. Moreover user can select what type of waveform to use. Input will be piano notes generated by the press of a key. The piano implementation will follow demo 18 which can implement one octave of notes and can also play more than one note simultaneously. In order to show the effect better the length of the generated notes will be around 4-5 seconds.

# Conclusion
The tremolo effect, one of the most popular effects in music industry, can be applied real time as well as in post processing of the audio.With the help of GUI a user can try and experience different variations of the tremolo effect.


# Reference
[1]  J. D. Reiss and A. McPherson,Audio Effects:  Theory, Implementation andApplication.  CRC Press, 2014.

[2]  K. Pearsall, “Effects guide:  Get to know tremolo.”https://www.fender.com/articles/tech-talk/pedal-board-primer-get-to-know-tremolo.
