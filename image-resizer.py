from flask import Flask, send_from_directory, send_file
from PIL import Image
import pillow_avif
from io import BytesIO
import os

app = Flask(__name__, static_folder='static')

@app.route('/<path:path>', methods=['GET', 'POST'])

#   格式参考B站，示例：
#   http://127.0.0.1:10000/example.ico@.webp
#   http://127.0.0.1:10000/example.gif@128w.avif
#   http://127.0.0.1:10000/example.png@256h.jpg
#   http://127.0.0.1:10000/example.jpg@512w.png
#   http://127.0.0.1:10000/example.avif@.gif
#   http://127.0.0.1:10000/example.webp@64w.ico

def resizer(path):

    out_path = path.replace('/', '_')

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

    if os.path.isfile(f'./static/{out_path}'):
        os.utime(f'./static/{out_path}', None)
        return send_from_directory(app.static_folder, out_path, mimetype=io_mimetype)

    else:
        image = f'./{path.split("@")[0]}'
        parameter = path.split('@')[1].split('.')[0]
        fileEx = path.split('@')[1].split('.')[1]

        img = Image.open(image)
        if 'w' in parameter:
            out_w = int(parameter.replace('w', ''))
            if out_w < img.width:
                out_h = round(out_w*img.height/img.width)
                img = img.resize((out_w, out_h), Image.BILINEAR)
                img.save(f'./static/{out_path}')
        elif 'h' in parameter:
            out_h = int(parameter.replace('w', ''))
            if out_h < img.height:
                out_w = round(out_h*img.width/img.height)
                img = img.resize((out_w, out_h), Image.BILINEAR)
                img.save(f'./static/{out_path}')

        img.save(f'./static/{out_path}')
        image_io = BytesIO()
        img.save(image_io, io_type)
        image_io.seek(0)
        return send_file(image_io, mimetype=io_mimetype)

if __name__ == '__main__':
    app.run(port=10000)
