from flask import Flask, request, abort, send_from_directory
import os
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello'

@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    imgStr = request.form['img']
    img = base64.b64decode(imgStr)
    fileName = request.form['fileName']
    filePath = os.path.join('imgs', fileName)
    with open(filePath, 'wb') as f:
        f.write(img)
    return "Success"

if __name__ == '__main__':
    app.run()
