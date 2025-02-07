import os
from dotenv import load_dotenv
import asyncio
import cv2
import pyaudio
import websockets
import struct
import sys
import threading
import ssl
import pathlib
from typing import Optional

# Load environment variables
load_dotenv()

HOST = ''
PORT = int(os.getenv('WEBSOCKET_PORT', '8000'))
HEADER_FORMAT = "!cI"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

SSL_CERT_PATH = os.getenv('SSL_CERT_PATH')
SSL_KEY_PATH = os.getenv('SSL_KEY_PATH')

def get_ssl_context() -> Optional[ssl.SSLContext]:
    """Create SSL context for production use"""
    if SSL_CERT_PATH and SSL_KEY_PATH:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(SSL_CERT_PATH, SSL_KEY_PATH)
        return context
    return None

def video_stream(websocket, loop):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to open video capture")
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        ret, encoded = cv2.imencode('.jpg', frame)
        if ret:
            data = encoded.tobytes()
            header = struct.pack(HEADER_FORMAT, b'V', len(data))
            message = header + data
            asyncio.run_coroutine_threadsafe(websocket.send(message), loop)
        cv2.waitKey(30)

def audio_stream(websocket, loop):
    pa = pyaudio.PyAudio()
    try:
        stream = pa.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            input=True,
            frames_per_buffer=1024
        )
    except Exception as e:
        print("Error opening audio stream:", e)
        return
    while True:
        try:
            frames = stream.read(1024, exception_on_overflow=False)
        except Exception as e:
            print("Error reading audio stream:", e)
            continue
        header = struct.pack(HEADER_FORMAT, b'A', len(frames))
        message = header + frames
        asyncio.run_coroutine_threadsafe(websocket.send(message), loop)

async def handler(websocket, path):
    # Verify Cloudflare headers if needed
    headers = websocket.request_headers
    cf_connecting_ip = headers.get('CF-Connecting-IP')
    cf_visitor = headers.get('CF-Visitor')

    if not cf_connecting_ip:
        print("Warning: Connection not from Cloudflare")

    loop = asyncio.get_event_loop()
    video_thread = threading.Thread(target=video_stream, args=(websocket, loop), daemon=True)
    audio_thread = threading.Thread(target=audio_stream, args=(websocket, loop), daemon=True)
    video_thread.start()
    audio_thread.start()
    await asyncio.Future()  # run forever

def main():
    ssl_context = get_ssl_context()
    
    # WebSocket server with or without SSL based on context
    start_server = websockets.serve(
        handler,
        HOST,
        PORT,
        ssl=ssl_context,
        # Required for Cloudflare
        ping_interval=20,
        ping_timeout=20,
        close_timeout=10
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    print(f"WebSocket streaming server listening on port {PORT} {'with SSL' if ssl_context else 'without SSL'}")
    loop.run_forever()

if __name__ == '__main__':
    main()