import audioop
import copy
import wave
from pathlib import Path

audio_dir = Path("audio")


class Track:
    # FIXME: Change to mono track when implemented in tape
    CHUNK_SIZE = 512
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

        curr_block = self.blocks[self.position]
        self.position += 1

        return curr_block

    def read_block_reverse(self):
        if self.position <= 0:
            return b""

        curr_block = self.blocks[self.position]
        self.position -= 1

        reverse_bytes = b""
        data_point_len = self.NUM_CHANNELS*self.SAMPLE_WIDTH

        for i in range(self.CHUNK_SIZE + 1):
            data_point = curr_block[-data_point_len:]
            curr_block = curr_block[:-data_point_len]
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

    def record_block_reverse(self, block):
        if self.position <= 0:
            return b""

        recorded_block = copy.deepcopy(block)

        # Get currently stored block
        curr_block_saved = self.blocks[self.position]

        # Reverse the block that has been recorded
        reverse_bytes_recorded = b""
        data_point_len = self.NUM_CHANNELS * self.SAMPLE_WIDTH

        for i in range(self.CHUNK_SIZE):
            data_point = block[-data_point_len:]
            block = block[:-data_point_len]
            reverse_bytes_recorded += data_point

        # Add the reversed recorded block to the saved block, and save it to the track
        self.blocks[self.position] = audioop.add(reverse_bytes_recorded, curr_block_saved, self.SAMPLE_WIDTH)

        # Reverse the block that was saved before it was overwritten
        reverse_bytes_saved = b""

        for i in range(self.CHUNK_SIZE):
            data_point = curr_block_saved[-data_point_len:]
            curr_block_saved = curr_block_saved[:-data_point_len]
            reverse_bytes_saved += data_point

        self.position -= 1

        return audioop.add(reverse_bytes_saved, recorded_block, self.SAMPLE_WIDTH)
