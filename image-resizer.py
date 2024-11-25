from flask import Flask, send_from_directory, send_file, make_response
from PIL import Image
import pillow_avif
from io import BytesIO
import time
import os

app = Flask(__name__, static_folder='static')

@app.route('/<path:path>', methods=['GET', 'POST'])

#   格式参考B站，示例：
#   http://127.0.0.1:10000/example.jpg@1920w_1080h.webp
#   http://127.0.0.1:10000/example.png@800w_800h.avif
#   http://127.0.0.1:10000/example.webp@512h.jpg
#   http://127.0.0.1:10000/example.avif@256w.png
#   http://127.0.0.1:10000/example.ico@.gif
#   http://127.0.0.1:10000/example.gif@64w_64h.ico
#   宽或高超出原图时，仅转换格式，不改变图片尺寸
#   宽和高都指定时，依旧保持原比例，以在原宽或原高中占比更大的那一边为标准进行缩小

def resizer(path):

    out_path = path.replace('/', '_')
    image = f'./img/{path.split('@')[0]}'
    cache = f'./static/{out_path}'

    fileEx = path.split('@')[1].split('.')[1]
    if fileEx.lower() == 'webp':
        io_type = 'WebP'
        io_mimetype = 'image/webp'
    elif fileEx.lower() == 'avif':
        io_type = 'AVIF'
        io_mimetype = 'image/avif'
    elif fileEx.lower() == 'jpg' or fileEx.lower() == 'jpeg':
        io_type = 'JPEG'
        io_mimetype = 'image/jpeg'
    elif fileEx.lower() == 'png':
        io_type = 'PNG'
        io_mimetype = 'image/png'
    elif fileEx.lower() == 'gif':
        io_type = 'GIF'
        io_mimetype = 'image/gif'
    elif fileEx.lower() == 'ico':
        io_type = 'ICO'
        io_mimetype = 'image/x-icon'

    if os.path.isfile(cache) and os.path.getmtime(cache) == os.path.getmtime(image):
        os.utime(cache,(time.time(), os.path.getmtime(cache)))
        return send_from_directory(app.static_folder, out_path, mimetype=io_mimetype)

    else:
        if os.path.isfile(image):
            img = Image.open(image)

            parameter = path.split('@')[1].split('.')[0]
            if 'w' in parameter and 'h' in parameter:
                out_w = int(parameter.split('_')[0].replace('w', ''))
                out_h = int(parameter.split('_')[1].replace('h', ''))
                if out_w/img.width < 1 and out_h/img.height < 1:
                    if out_w/img.width >= out_h/img.height:
                        out_h = round(out_w*img.height/img.width)
                        img = img.resize((out_w, out_h), Image.BILINEAR)
                        img.save(cache)
                    else:
                        out_w = round(out_h*img.width/img.height)
                        img = img.resize((out_w, out_h), Image.BILINEAR)
                        img.save(cache)
            elif 'w' in parameter:
                out_w = int(parameter.replace('w', ''))
                if out_w < img.width:
                    out_h = round(out_w*img.height/img.width)
                    img = img.resize((out_w, out_h), Image.BILINEAR)
                    img.save(cache)
            elif 'h' in parameter:
                out_h = int(parameter.replace('h', ''))
                if out_h < img.height:
                    out_w = round(out_h*img.width/img.height)
                    img = img.resize((out_w, out_h), Image.BILINEAR)
                    img.save(cache)

            img.save(cache)
            os.utime(cache,(time.time(), os.path.getmtime(image)))
            image_io = BytesIO()
            img.save(image_io, io_type)
            image_io.seek(0)
            return send_file(image_io, mimetype=io_mimetype)

        else:
            return make_response('', 404)

if __name__ == '__main__':
    app.run(port=10000)
