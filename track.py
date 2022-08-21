from re import I
from threading import Event, Thread
import pyaudio
import wave

class Track:
	CHUNK_SIZE = 1024
	AUDIO_RATE = 44100

	def __init__(self):
		self.wf = wave.open("audio/side_b.wav")
		self.p = pyaudio.PyAudio()

		self.stream = self.p.open(format = self.p.get_format_from_width(self.wf.getsampwidth()), channels=self.wf.getnchannels(), rate=self.wf.getframerate(), output=True)
		self.data = self.wf.readframes(self.CHUNK_SIZE)
		self.curr_time = 0

		self.open = Event()
		self.open.set()
		self.play_state = Event()
		self.record_state = Event()
		self.thread = Thread(target = self.handle_tape, args = [self.open, self.play_state, self.record_state])
		self.thread.start()

	def handle_tape(self, open, play_state, record_state):
		while open.is_set():
			if play_state.is_set():
				self.play_chunk()
		return

	def play_chunk(self):
		self.stream.write(self.data)
		self.data = self.wf.readframes(self.CHUNK_SIZE)

	def play(self):
		self.play_state.set()
	
	def pause(self):
		self.play_state.clear()

	def close(self):
		self.open.clear()
		self.thread.join()
		self.stream.stop_stream()
		self.stream.close()
		self.p.terminate()
	