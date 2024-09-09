from flask import Flask, send_from_directory, send_file
from PIL import Image
from io import BytesIO
import os

app = Flask(__name__, static_folder='static')

@app.route('/<path:path>', methods=['GET', 'POST'])

#   格式，参考B站：
#   http://127.0.0.1:10000/example.png@256w_256h.webp
#   http://127.0.0.1:10000/example.png@256w.jpg
#   http://127.0.0.1:10000/example.png@256h.png
#   http://127.0.0.1:10000/example.png@.gif

def resizer(path):
    out_path = path.replace('/', '_')
    if os.path.isfile(f'./static/{out_path}'):
        os.utime(f'./static/{out_path}', None)
        return send_from_directory(app.static_folder, out_path)
    else:
        image = f'./{path.split("@")[0]}'
        parameter = path.split('@')[1]
        if 'w' in parameter and 'h' in parameter:
            out_w = int(parameter.split('_')[0].replace('w', ''))
            out_h = int(parameter.split('_')[1].split('.')[0].replace('h', ''))
            fileEx = parameter.split('.')[1]
            img = Image.open(image)
            resized = img.resize((out_w, out_h), Image.BILINEAR)
            resized.save(f'./static/{out_path}')
        elif 'w' in parameter:
            out_w = int(parameter.split('.')[0].replace('w', ''))
            fileEx = parameter.split('.')[1]
            img = Image.open(image)
            out_h = round(out_w*img.height/img.width)
            resized = img.resize((out_w, out_h), Image.BILINEAR)
            resized.save(f'./static/{out_path}')
        elif 'h' in parameter:
            out_h = int(parameter.split('.')[0].replace('h', ''))
            fileEx = parameter.split('.')[1]
            img = Image.open(image)
            out_w = round(out_h*img.width/img.height)
            resized = img.resize((out_w, out_h), Image.BILINEAR)
            resized.save(f'./static/{out_path}')
        else:
            img = Image.open(image)
            img.save(f'./static/{out_path}')

        if fileEx.lower() == 'webp':
            io_type = 'WebP'
            io_mimetype = 'image/webp'
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

        image_io = BytesIO()
        resized.save(image_io, io_type)
        image_io.seek(0)
        return send_file(image_io, mimetype=io_mimetype)

if __name__ == '__main__':
    app.run(port=10000)