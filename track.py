from re import I
from threading import Event, Thread
import pyaudio
import wave

class Track:
	CHUNK_SIZE = 1024
	AUDIO_RATE = 44100

	def __init__(self):
		self.wf = wave.open("audio/side_b.wav")
		p = pyaudio.PyAudio()

		self.stream = p.open(format = p.get_format_from_width(self.wf.getsampwidth()), channels=self.wf.getnchannels(), rate=self.wf.getframerate(), output=True)
		self.data = self.wf.readframes(self.CHUNK_SIZE)
		self.curr_time = 0

		self.play_state = Event()
		self.record_state = Event()
		self.thread = Thread(target = self.handle_tape, args = [self.play_state, self.record_state])
		self.thread.start()

	def handle_tape(self, play_state, record_state):
		while True:
			if play_state.is_set():
				self.play_chunk()

	def play_chunk(self):
		self.stream.write(self.data)
		self.data = self.wf.readframes(self.CHUNK_SIZE)

	def play(self):
		self.play_state.set()
	
	def pause(self):
		self.play_state.clear()
