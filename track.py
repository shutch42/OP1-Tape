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
        self.reverse_state = Event()
        self.record_state = Event()
        self.stop_state = Event()
        self.thread = Thread(target=self.handle_tape,
                             args=[self.open_state, self.play_state, self.reverse_state,
                                   self.stop_state, self.record_state])
        self.thread.start()

    def handle_tape(self, open_state, play_state, reverse_state, stop_state, record_state):
        while open_state.is_set():
            if stop_state.is_set():
                self.stop()
            if play_state.is_set():
                self.play_chunk()
            if reverse_state.is_set():
                self.play_chunk_reverse()
        return

    def play_chunk(self):
        self.data = self.wf.readframes(self.CHUNK_SIZE)
        self.stream.write(self.data)

    def play_chunk_reverse(self):
        # Get current position
        position = self.wf.tell()

        # Move file position back two chunks
        self.wf.setpos(position - self.CHUNK_SIZE*2)

        # Read chunk from new file position
        self.data = self.wf.readframes(self.CHUNK_SIZE)

        # Reverse chunk data:
        # Since wave byte strings are stored as (frequency, position) per channel at each point in time,
        # the number of bytes stored at each time point is dependent on the number of channels.
        # An easy way to calculate the number of bytes at each point is to divide the byte string length by chunk size.
        # After we have this number, we can each time point that is stored in the data string

        bytes_per_unit_time = int(len(self.data)/self.CHUNK_SIZE)

        reverse_bytes = b""
        for i in range(self.CHUNK_SIZE):
            data_point = self.data[-bytes_per_unit_time:]
            self.data = self.data[:-bytes_per_unit_time]
            reverse_bytes += data_point

        # Write reversed chunk to stream
        self.stream.write(reverse_bytes)

    def play(self):
        self.play_state.set()
        self.reverse_state.clear()

    def pause(self):
        self.play_state.clear()
        self.reverse_state.clear()

    def reverse(self):
        self.reverse_state.set()
        self.play_state.clear()

    def stop(self):
        self.wf.rewind()
        self.data = self.wf.readframes(self.CHUNK_SIZE)

    def fast_forward(self):
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
