from application import app
from PIL import Image
from flask import Flask, request, redirect, url_for, render_template
import os
import io
import requests
import base64
import cv2
import numpy as np
import math

app.config['UPLOAD_EXTENSIONS'] = ['.png', '.jpg', '.jpeg', '.JPG']
app.config['UPLOAD_FOLDER'] = 'static/uploadedImages'

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/upload_images")
def upload_images():
    return render_template("upload_images.html")

@app.route("/uploader", methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    url = ''
    key = ''
    headers={'content-type':'application/octet-stream','Prediction-Key':key}
    
    #read file can only do this once
    read = uploaded_file.read()

    r = requests.post(url,data=read,headers=headers)
    
    #nparr = np.fromstring(fileStream, np.uint8)
    image = cv2.imdecode(np.frombuffer(read, np.uint8), -1)
    predictions = r.json()['predictions']

    imageWidth = image.shape[1]
    imageHeight = image.shape[0]
    items = []

    for prediction in predictions:
        if prediction['probability'] > .75:
            xCoord = prediction['boundingBox']['left'] * imageWidth
            yCoord = prediction['boundingBox']['top'] * imageHeight
            width = prediction['boundingBox']['width'] * imageWidth
            height = prediction['boundingBox']['height'] * imageHeight
            xPlus = xCoord + width
            yPlus = yCoord + height

            startpoint = (math.ceil(xCoord), math.ceil(yCoord))
            endpoint = (math.ceil(xPlus), math.ceil(yPlus))
            color = (255, 255, 255)
            thickness = 10

            image = cv2.rectangle(image, startpoint, endpoint, color, thickness)

            tagName = prediction['tagName']
            probability = math.floor(prediction['probability']*100)
            startpoint = (math.ceil(xCoord), math.ceil(yCoord) - 15)
            text = f'{tagName} {probability}%'

            cv2.putText(image, text, startpoint, cv2.FONT_HERSHEY_SIMPLEX, 2, color, thickness)
            items.append(prediction['tagName'])

    broken = []
    for object in items:
        if 'Head' in object and object.replace(' Head', '') not in broken:
            broken.append(object.replace(' Head', ''))
        if 'Tail' in object and object.replace(' Tail', '') not in broken:
            broken.append(object.replace(' Tail', ''))
        if 'Head' not in object and 'Tail' not in object:
            broken.append(object)

    #write file to binary then conver to image string to display
    img_str = cv2.imencode('.jpg', image)[1].tobytes()
    b64 = base64.b64encode(img_str)
    fileStream = b64.decode('utf-8')
    #print(type(img))
    #cv2.imwrite('static/uploadedImages/output.jpg', img_np)
    #b64 = uploaded_file.stream.read()
    #im = Image.open(base64.b64encode(uploaded_file.read()))
    #data = io.BytesIO()
    #im.save(data, "JPG")
    #encoded = base64.b64encode(data.getvalue())
    #encoded.decode('utf-8')
    #print(type(img_np))
    return render_template("image_output.html", binary_image=fileStream, broken_object=broken)

@app.route("/image_output")
def image_output():
    return render_template("image_output.html")

@app.route("/about_us")
def about_us():
    return render_template("about_us.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")