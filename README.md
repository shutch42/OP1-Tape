# OP1-Tape

This project was meant to be a clone of the OP-1 Tape feature, specifically for running on the raspberry pi. The code I have in this repo works on some systems, but it is limited by hardware. In particular, the combination of pygame and pyaudio is just too much for the raspberry pi 4 to handle. It can't process the audio quickly enough, and this results in skipping and distorted sounds. Because of this, I have decided to redo the project using a different stack. Going forward, I plan to program the same application in C with a more minimal GUI to improve sound processing on the pi 4. In the meantime, here's what I have working from this repository.
- Single track audio playback
- Simultaneous playback and recording (overdubbing)
- Sound manipulation such as fast-forward, rewind, and reverse audio effects
- Basic GUI with animated reel-to-reel tape (OP1-style)
- Key inputs/combinations for play, pause, stop, fast-forward, rewind, reverse, and record
