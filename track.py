import wave
from pathlib import Path

audio_dir = Path("audio")


class Track:
    # FIXME: Change to mono track when implemented in tape
    CHUNK_SIZE = 1024
    NUM_CHANNELS = 2
    SAMPLE_WIDTH = 2
    AUDIO_RATE = 44100

    def __init__(self, filename):
        self.filename = filename
        self.blocks = []
        self.position = 0

        wr = wave.open(str(audio_dir / self.filename), "rb")

        data = wr.readframes(self.CHUNK_SIZE)
        while len(data) > 0:
            self.blocks.append(data)
            data = wr.readframes(self.CHUNK_SIZE)

        wr.close()

    def save(self):
        # ww = wave.open(audio_dir / self.filename, "wb")
        ww = wave.open(str(audio_dir / "tmp.wav"), "wb")
        ww.setnchannels(self.NUM_CHANNELS)
        ww.setsampwidth(self.SAMPLE_WIDTH)
        ww.setframerate(self.AUDIO_RATE)
        for block in self.blocks:
            ww.writeframes(block)
        ww.close()

    def read_block(self):
        block = self.blocks[self.position]
        self.position += 1
        return block

    def read_block_reverse(self):
        block = self.blocks[self.position]
        self.position -= 1

        reverse_bytes = b""
        data_point_len = self.NUM_CHANNELS*self.SAMPLE_WIDTH

        for i in range(self.CHUNK_SIZE + 1):
            data_point = block[-data_point_len:]
            block = block[:-data_point_len]
            reverse_bytes += data_point

        return reverse_bytes
