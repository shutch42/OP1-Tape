from threading import Event, Thread
from sound import Sound

class Track:
	def __init__(self):
		self.audio = Sound("audio/side_b.wav")
		self.state = Event()
		self.thread = Thread(target = self.audio.play, args = [self.state])
		self.thread.start()

	def play(self):
		self.state.set()
	
	def pause(self):
		self.state.clear()
