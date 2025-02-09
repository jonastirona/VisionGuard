import asyncio
import json
import base64
from channels.generic.websocket import AsyncWebsocketConsumer
from .utils.camera_utils import VideoProcessor
from .utils.audio_utils import AudioCapturer

class StreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.video = VideoProcessor()
        self.audio = AudioCapturer()
        self.audio.start()
        await self.accept()

    async def disconnect(self, close_code):
        self.video.release()
        self.audio.stop()
        
    async def receive(self, text_data):
        # Send combined stream at 30 FPS
        while True:
            video_frame = self.video.get_processed_frame()
            audio_data = self.audio.read()
            
            if video_frame and audio_data is not None:
                await self.send(json.dumps({
                    'video': base64.b64encode(video_frame).decode('utf-8'),
                    'audio': base64.b64encode(audio_data.tobytes()).decode('utf-8')
                }))
            elif video_frame:
                await self.send(json.dumps({
                    'video': base64.b64encode(video_frame).decode('utf-8')
                }))
            else:
                break
            await asyncio.sleep(1/30)