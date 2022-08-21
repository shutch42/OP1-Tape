import pyaudio
from threading import Event
import wave

class Sound:
	CHUNK_SIZE = 256
	AUDIO_RATE = 44100

	def __init__(self, filename):
		self.wf = wave.open(filename, 'rb')
		self.p = pyaudio.PyAudio()

		self.stream = self.p.open(format = self.p.get_format_from_width(self.wf.getsampwidth()), channels=self.wf.getnchannels(), rate=self.wf.getframerate(), output=True)

		self.data = self.wf.readframes(self.CHUNK_SIZE)
	
	def play_chunk(self):
		self.stream.write(self.data)
		self.data = self.wf.readframes(self.CHUNK_SIZE)
	
	def play(self, state):
		while True:
			if state.is_set():
				self.play_chunk()

	def close(self):
		self.stream.close()
		self.p.terminate()
