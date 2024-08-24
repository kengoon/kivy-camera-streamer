import contextlib

import flask
import socket

app = flask.Flask(import_name="Streamer")
browser_opened = False
HEADER_LENGTH = 64

frame = None


def gen_frames():
    global frame
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 7000))
    server.listen()
    client_socket, _ = server.accept()
    print("hello")
    while True:
        with contextlib.suppress(ValueError):
            header = int(client_socket.recv(HEADER_LENGTH))
            frame = client_socket.recv(header)
        yield (
                b'--frame\r\n'
                b'Content-Type: image/png\r\n\r\n'
                + frame + b'\r\n'
        )


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route('/video_feed')
def video_feed():
    return flask.Response(
        gen_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


app.run(host="0.0.0.0", port=8080, debug=True)
# for i in gen_frames():
#     print("ya")
