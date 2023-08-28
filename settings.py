import os

SERVER_HOST = os.getenv('SERVER_HOST', 'localhost')
SERVER_PORT = os.getenv('SERVER_PORT', 8000)

SERVER_ADDR = (SERVER_HOST, SERVER_PORT)
METRIC_SERVER = ('localhost', 3000)