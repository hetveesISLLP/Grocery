# from channels.layers import get_channel_layer
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer



class ChatConsumer(WebsocketConsumer):

    # client to server
    def connect(self):
        print("Websocket connected.")
        self.accept()

    def disconnect(self, close_code):
        print("Websocket disconnected")

    def receive(self, text_data=None, bytes_data=None):
        print("Received")