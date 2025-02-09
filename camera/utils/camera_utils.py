# Python
STREAM_SERVER_HOST = 'localhost'
STREAM_SERVER_PORT = 8000

def get_stream_url():
    protocol = 'wss' if settings.SECURE_SSL_REDIRECT else 'ws'
    return f"{protocol}://{STREAM_SERVER_HOST}:{STREAM_SERVER_PORT}"