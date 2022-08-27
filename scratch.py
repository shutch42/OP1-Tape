from track import Track
import pyaudio

track1 = Track("side_b.wav")

p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(2), channels=2, rate=44100, output=True, frames_per_buffer=1024)

data = track1.read_block()
for i in range(300):
    stream.write(data, 1024)
    data = track1.read_block()

data = track1.read_block_reverse()
for i in range(300):
    stream.write(data, 1024)
    data = track1.read_block_reverse()
