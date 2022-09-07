import audioop
import wave
from pathlib import Path

audio_dir = Path("audio")


class Track:
    # FIXME: Change to mono track when implemented in tape
    CHUNK_SIZE = 256
    NUM_CHANNELS = 1
    SAMPLE_WIDTH = 2
    AUDIO_RATE = 44100

    def __init__(self, filename):
        self.filename = filename
        self.blocks = []
        self.position = 0

        try:
            wr = wave.open(str(audio_dir / self.filename), "rb")
            data = wr.readframes(self.CHUNK_SIZE)
            while len(data) > 0:
                self.blocks.append(data)
                data = wr.readframes(self.CHUNK_SIZE)

            wr.close()
        except FileNotFoundError:
            # Create 6 minute empty tape
            chunk = b"\x00" * self.CHUNK_SIZE * self.SAMPLE_WIDTH
            num_chunks = 6 * 60 * self.AUDIO_RATE // self.CHUNK_SIZE
            self.blocks = [chunk]*num_chunks

    def save(self):
        ww = wave.open(str(audio_dir / self.filename), "w")
        ww.setnchannels(self.NUM_CHANNELS)
        ww.setsampwidth(self.SAMPLE_WIDTH)
        ww.setframerate(self.AUDIO_RATE)
        for block in self.blocks:
            ww.writeframes(block)
        ww.close()

    def stop(self):
        self.position = 0

    def read_block(self):
        if self.position >= len(self.blocks) - 1:
            return b""

        block = self.blocks[self.position]
        self.position += 1

        return block

    def read_block_reverse(self):
        if self.position <= 0:
            return b""

        block = self.blocks[self.position]
        self.position -= 1

        reverse_bytes = b""
        data_point_len = self.NUM_CHANNELS*self.SAMPLE_WIDTH

        for i in range(self.CHUNK_SIZE + 1):
            data_point = block[-data_point_len:]
            block = block[:-data_point_len]
            reverse_bytes += data_point

        return reverse_bytes

    def record_block(self, block):
        if self.position >= len(self.blocks) - 1:
            return b""

        curr_block = self.blocks[self.position]
        combined_block = audioop.add(curr_block, block, self.SAMPLE_WIDTH)
        self.blocks[self.position] = combined_block
        self.position += 1

        return combined_block
