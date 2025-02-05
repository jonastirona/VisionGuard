import pyaudio

class AudioStream:
    def __init__(self, rate=44100, channels=2, frames_per_buffer=1024, input_device_index=0): # 0 for default audio input device, >0 for external audio input devices
        self.rate = rate
        self.channels = channels
        self.frames_per_buffer = frames_per_buffer
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      input_device_index=input_device_index,
                                      frames_per_buffer=self.frames_per_buffer)

    def get_frame(self):
        return self.stream.read(self.frames_per_buffer)

    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()