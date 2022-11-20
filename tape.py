from track import Track
from threading import Event, Thread
import math
import pyaudio
import audioop


class Tape:
    def __init__(self):
        self.track1 = Track("track_1.wav")
        self.p = pyaudio.PyAudio()

        # Change input_device_index to work with different inputs
        # Currently it's set to my audio interface
        self.normal_stream = self.p.open(format=self.p.get_format_from_width(self.track1.SAMPLE_WIDTH),
                                         channels=self.track1.NUM_CHANNELS, rate=self.track1.AUDIO_RATE, input=True,
                                         output=True, frames_per_buffer=self.track1.CHUNK_SIZE, input_device_index=0)
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
                    if signals["record"].is_set():
                        self.record_chunk()
                    else:
                        self.play_chunk()
                else:
                    if signals["record"].is_set():
                        self.record_chunk_reverse()
                    else:
                        self.play_chunk_reverse()
            else:
                if signals["record"].is_set():
                    self.monitor_input_trigger()

    def play_chunk(self):
        data = self.track1.read_block()
        self.stream.write(data)

    def play_chunk_reverse(self):
        data = self.track1.read_block_reverse()
        self.stream.write(data)

    def record_chunk(self):
        recorded_chunk = self.stream.read(self.track1.CHUNK_SIZE, exception_on_overflow=False)
        data = self.track1.record_block(recorded_chunk)
        self.stream.write(data)

    def record_chunk_reverse(self):
        recorded_chunk = self.stream.read(self.track1.CHUNK_SIZE, exception_on_overflow=False)
        data = self.track1.record_block_reverse(recorded_chunk)
        self.stream.write(data)

    def monitor_input_trigger(self):
        recorded_chunk = self.stream.read(self.track1.CHUNK_SIZE, exception_on_overflow=False)
        level = audioop.rms(recorded_chunk, self.track1.SAMPLE_WIDTH)
        if level > 10:
            data = self.track1.record_block(recorded_chunk)
            self.stream.write(data)
            self.record()

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

    def record(self):
        self.signals["play"].set()
        self.signals["forward"].set()
        self.signals["fast"].clear()
        self.signals["record"].set()

    def record_reverse(self):
        self.signals["play"].set()
        self.signals["forward"].clear()
        self.signals["fast"].clear()
        self.signals["record"].set()

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

    def arm_record(self):
        self.signals["fast"].clear()
        self.signals["forward"].set()
        self.signals["play"].clear()
        self.signals["record"].set()

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
