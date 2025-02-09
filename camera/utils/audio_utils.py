import sounddevice as sd
import numpy as np
from queue import Queue

class AudioCapturer:
    def __init__(self, samplerate=44100, blocksize=1024):
        self.samplerate = samplerate
        self.blocksize = blocksize
        self.audio_queue = Queue()
        
    def callback(self, indata, frames, time, status):
        self.audio_queue.put(indata.copy())

    def start(self):
        self.stream = sd.InputStream(
            samplerate=self.samplerate,
            blocksize=self.blocksize,
            callback=self.callback
        )
        self.stream.start()

    def read(self):
        if self.audio_queue.empty():
            return None
        return self.audio_queue.get()

    def stop(self):
        self.stream.stop()
        self.stream.close()