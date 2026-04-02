from flask import request, Response
import os

def stream_video(path):
    file_size = os.path.getsize(path)
    range_header = request.headers.get('Range', None)

    if not range_header:
        return Response(open(path, 'rb'), mimetype='video/mp4')

    byte1, byte2 = 0, None
    range_header = range_header.replace("bytes=", "")
    parts = range_header.split("-")

    byte1 = int(parts[0])
    if parts[1]:
        byte2 = int(parts[1])

    length = file_size - byte1
    if byte2:
        length = byte2 - byte1 + 1

    with open(path, 'rb') as f:
        f.seek(byte1)
        data = f.read(length)

    response = Response(data, 206, mimetype='video/mp4')
    response.headers.add('Content-Range', f'bytes {byte1}-{byte1 + length - 1}/{file_size}')
    response.headers.add('Accept-Ranges', 'bytes')

    return response