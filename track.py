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
                                               channels=self.wf.getnchannels(), rate=self.wf.getframerate()*5, output=True, frames_per_buffer=self.CHUNK_SIZE)

        self.slow_stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                                       channels=self.wf.getnchannels(), rate=int(self.AUDIO_RATE/2), output=True, frames_per_buffer=self.CHUNK_SIZE)

        self.normal_stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                                         channels=self.wf.getnchannels(), rate=self.wf.getframerate(), output=True, frames_per_buffer=self.CHUNK_SIZE)

        self.stream = self.normal_stream

        self.data = None

        self.open_state = Event()
        self.open_state.set()

        self.signals = {"play": Event(),
                        "reverse": Event(),
                        "fast forward": Event(),
                        "rewind": Event(),
                        "record": Event(),
                        "stop": Event()}

        self.thread = Thread(target=self.handle_tape,
                             args=[self.open_state, self.signals])
        self.thread.start()

    def handle_tape(self, open_state, signals):
        while open_state.is_set():
            if signals["stop"].is_set():
                self.stop()
            if signals["play"].is_set():
                self.play_chunk()
            if signals["reverse"].is_set():
                self.reverse_chunk()
            if signals["fast forward"].is_set():
                self.fast_forward_chunk()
            if signals["rewind"].is_set():
                self.rewind_chunk()
        return

    def play_chunk(self):
        self.stream = self.normal_stream
        self.data = self.wf.readframes(self.CHUNK_SIZE)
        self.stream.write(self.data, self.CHUNK_SIZE)

    def fast_forward_chunk(self):
        self.stream = self.fast_stream
        self.data = self.wf.readframes(self.CHUNK_SIZE)
        self.stream.write(self.data, self.CHUNK_SIZE)

    def reverse_chunk(self):
        self.stream = self.normal_stream
        # Get current position
        position = self.wf.tell()

        # Move file position back two chunks
        self.wf.setpos(position - self.CHUNK_SIZE * 2)

        # Read chunk from new file position
        self.data = self.wf.readframes(self.CHUNK_SIZE)

        # Reverse chunk data:
        # Since wave byte strings are stored as (frequency, position) per channel at each point in time,
        # the number of bytes stored at each time point is dependent on the number of channels.
        # An easy way to calculate the number of bytes at each point is to divide the byte string length by chunk size.
        # After we have this number, we can each time point that is stored in the data string

        bytes_per_unit_time = int(len(self.data) / self.CHUNK_SIZE)

        reverse_bytes = b""
        for i in range(self.CHUNK_SIZE + 1):
            data_point = self.data[-bytes_per_unit_time:]
            self.data = self.data[:-bytes_per_unit_time]
            reverse_bytes += data_point

        if reverse_bytes == '':
            reverse_bytes = chr(0) * bytes_per_unit_time

        # Write reversed chunk to stream
        self.stream.write(reverse_bytes, self.CHUNK_SIZE)

    def rewind_chunk(self):
        self.stream = self.fast_stream
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
        for i in range(self.CHUNK_SIZE+1):
            data_point = self.data[-bytes_per_unit_time:]
            self.data = self.data[:-bytes_per_unit_time]
            reverse_bytes += data_point

        if reverse_bytes == '':
            reverse_bytes = chr(0)*bytes_per_unit_time

        # Write reversed chunk to stream
        self.stream.write(reverse_bytes, self.CHUNK_SIZE)

    def play(self):
        self.signals["play"].set()
        self.signals["reverse"].clear()
        self.signals["fast forward"].clear()
        self.signals["rewind"].clear()

    def pause(self):
        self.signals["play"].clear()
        self.signals["reverse"].clear()
        self.signals["fast forward"].clear()
        self.signals["rewind"].clear()

    def stop(self):
        self.wf.rewind()
        self.pause()

    def reverse(self):
        self.signals["reverse"].set()
        self.signals["play"].clear()
        self.signals["fast forward"].clear()
        self.signals["rewind"].clear()

    def fast_forward(self):
        self.signals["fast forward"].set()
        self.signals["play"].clear()
        self.signals["reverse"].clear()
        self.signals["rewind"].clear()

    def rewind(self):
        self.signals["rewind"].set()
        self.signals["play"].clear()
        self.signals["reverse"].clear()
        self.signals["fast forward"].clear()

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
