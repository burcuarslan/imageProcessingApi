from io import BytesIO

import cv2
import numpy as np
from flask import Flask, request, jsonify, make_response
from PIL import Image

app = Flask(__name__)




@app.route('/process_image', methods=['POST'])
def process_image():
    # İstekten resmi al
    req_image = request.files['image']
    data = request.form
    w = int(data.get('w'))
    h = int(data.get('h'))
    img = cv2.imdecode(np.fromstring(request.files['image'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
    # Boyutlandırma
    resized_img = cv2.resize(img, (w, h))
    return buffer(resized_img)


@app.route('/cropped_image', methods=['POST'])
def cropped_image():
    data = request.form

    w = int(data.get('w'))
    h = int(data.get('h'))
    y = int(data.get('y'))
    x = int(data.get('x'))
    img = cv2.imdecode(np.fromstring(request.files['image'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
    # Boyutlandırma
    # resized_img = cv2.resize(img, (w,h))
    cropped_image = img[y:y + h, x:x + w]
    return buffer(cropped_image)


@app.route('/rotate_image', methods=['POST'])
def rotate_image():
    img = cv2.imdecode(np.fromstring(request.files['image'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
    # Boyutlandırma
    # resized_img = cv2.resize(img, (w,h))
    rotate_img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    return buffer(rotate_img)


def buffer(img):
    # PIL Image nesnesi oluşturma
    output_img = Image.fromarray(img)
    # JPEG formatına dönüştürme ve response nesnesi içinde kullanma
    output_buffer = BytesIO()
    output_img.save(output_buffer, format='JPEG')
    response = make_response(output_buffer.getvalue())
    response.headers['Content-Type'] = 'image/jpeg'

    return response
