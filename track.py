from threading import Event, Thread
import pyaudio
import wave
import math

class Track:
    CHUNK_SIZE = 1024
    AUDIO_RATE = 44100

    def __init__(self):
        self.wf = wave.open("audio/side_b.wav")

        self.p = pyaudio.PyAudio()

        self.fast_stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                                       channels=self.wf.getnchannels(), rate=self.wf.getframerate()*5, output=True)

        self.normal_stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                                         channels=self.wf.getnchannels(), rate=self.wf.getframerate(), output=True)

        self.stream = self.normal_stream

        self.data = None

        self.open_state = Event()
        self.open_state.set()

        self.play_state = Event()
        self.record_state = Event()
        self.stop_state = Event()
        self.thread = Thread(target=self.handle_tape,
                             args=[self.open_state, self.play_state, self.stop_state, self.record_state])
        self.thread.start()

    def handle_tape(self, open_state, play_state, stop_state, record_state):
        while open_state.is_set():
            if stop_state.is_set():
                self.stop()
            if play_state.is_set():
                self.play_chunk()
        return

    def play_chunk(self):
        self.data = self.wf.readframes(self.CHUNK_SIZE)
        self.stream.write(self.data)

    def play(self):
        self.play_state.set()

    def pause(self):
        self.play_state.clear()

    def stop(self):
        self.wf.rewind()
        self.data = self.wf.readframes(self.CHUNK_SIZE)

    def fast_forward(self):
        # Unfortunately speed adjustments to the track require some weird file manipulation
        self.stream = self.fast_stream

    def reset_speed(self):
        self.stream = self.normal_stream
    def get_time(self):
        return self.wf.tell() / self.AUDIO_RATE

    def get_time_string(self):
        time = self.get_time()
        minutes = str(math.floor(time / 60)).zfill(2)
        seconds = str(math.floor(time % 60)).zfill(2)
        hundredth_seconds = str(math.floor(time*100 % 100)).zfill(2)
        return minutes + ":" + seconds + ":" + hundredth_seconds

    def close(self):
        self.open_state.clear()
        self.thread.join()
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
