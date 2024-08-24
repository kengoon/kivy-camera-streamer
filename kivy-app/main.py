from kivy.app import App
from kivy.lang import Builder
import requests
from kivy_gradient import save_as_png
from threading import Thread
from kivy.clock import Clock
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 7000))
HEADER_LENGTH = 64


class CameraLiveStreamApp(App):
    image_list = []

    def build(self):
        return Builder.load_file("stream.kv")

    def stream_live_camera(self):
        Clock.schedule_interval(self.take_picture, 1/5)

    def take_picture(self, _):
        texture = self.root.ids.camera.texture
        width, height = texture.size

        # Get the pixels from the texture (this returns a bytes object)
        pixel_data = texture.pixels

        # Create a PNG file from the pixel data
        img = save_as_png(width, height, pixel_data)
        Thread(target=self.send_image_request, args=(img,)).start()

    @staticmethod
    def send_image_request(img):
        client.sendall(f"{len(img):<{HEADER_LENGTH}}".encode("utf-8"))
        byt = client.sendall(img)
        print(byt)
        print(len(img))


if __name__ == "__main__":
    CameraLiveStreamApp().run()
