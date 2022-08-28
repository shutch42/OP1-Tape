from track import Track
from threading import Event, Thread
import math
import pyaudio


class Tape:
    def __init__(self):
        self.track1 = Track("side_b.wav")
        self.p = pyaudio.PyAudio()

        self.normal_stream = self.p.open(format=self.p.get_format_from_width(self.track1.SAMPLE_WIDTH),
                                         channels=self.track1.NUM_CHANNELS, rate=self.track1.AUDIO_RATE, input=True,
                                         output=True, frames_per_buffer=self.track1.CHUNK_SIZE)
        self.fast_stream = self.p.open(format=self.p.get_format_from_width(self.track1.SAMPLE_WIDTH),
                                       channels=self.track1.NUM_CHANNELS, rate=self.track1.AUDIO_RATE*5, output=True,
                                       frames_per_buffer=self.track1.SAMPLE_WIDTH)

        self.stream = self.normal_stream

        self.signals = {"open_state": Event(),
                        "play": Event(),
                        "forward": Event(),
                        "fast": Event(),
                        "record": Event()}

        self.signals["open_state"].set()

        self.thread = Thread(target=self.handle_tape, args=[self.signals])
        self.thread.start()

    def handle_tape(self, signals):
        while signals["open_state"].is_set():
            if signals["fast"].is_set():
                self.stream = self.fast_stream
            else:
                self.stream = self.normal_stream

            if signals["play"].is_set():
                if signals["forward"].is_set():
                    self.play_chunk()
                else:
                    self.play_chunk_reverse()

    def play_chunk(self):
        data = self.track1.read_block()
        self.stream.write(data)

    def play_chunk_reverse(self):
        data = self.track1.read_block_reverse()
        self.stream.write(data)

    def play(self):
        self.signals["play"].set()
        self.signals["forward"].set()
        self.signals["fast"].clear()
        self.signals["record"].clear()

    def pause(self):
        self.signals["play"].clear()
        self.signals["record"].clear()

    def stop(self):
        self.track1.stop()
        self.signals["play"].clear()
        self.signals["forward"].set()
        self.signals["fast"].clear()
        self.signals["record"].clear()

    def reverse(self):
        self.signals["forward"].clear()
        self.signals["play"].set()
        self.signals["fast"].clear()

    def fast_forward(self):
        self.signals["fast"].set()
        self.signals["forward"].set()
        self.signals["play"].set()
        self.signals["record"].clear()

    def rewind(self):
        self.signals["fast"].set()
        self.signals["forward"].clear()
        self.signals["play"].set()
        self.signals["record"].clear()

    def get_time(self):
        return self.track1.position * self.track1.CHUNK_SIZE / self.track1.AUDIO_RATE

    def get_time_string(self):
        time = self.get_time()
        minutes = str(math.floor(time / 60)).zfill(2)
        seconds = str(math.floor(time % 60)).zfill(2)
        hundredth_seconds = str(math.floor(time*100 % 100)).zfill(2)
        return minutes + ":" + seconds + ":" + hundredth_seconds

    def close(self):
        self.signals["open_state"].clear()
        self.thread.join()
        self.normal_stream.stop_stream()
        self.fast_stream.stop_stream()
        self.normal_stream.close()
        self.fast_stream.close()
        self.track1.save()
        self.p.terminate()
