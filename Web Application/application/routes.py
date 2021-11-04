from application import app
from flask import Flask, request, redirect, url_for, render_template, session, send_from_directory, send_file
import requests
import base64
import cv2
import numpy as np
import math
import pyodbc
import io

app.config['UPLOAD_EXTENSIONS'] = ['.png', '.jpg', '.jpeg', '.JPG']
app.config['UPLOAD_FOLDER'] = 'static/uploadedImages'
app.secret_key = 'cool_project'

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
    #print(fileStream)
    #session variable to keep track of broken objects(s)
    session['broken_object'] = broken[0]

    return render_template("image_output.html", binary_image=fileStream, broken_object=broken)

@app.route("/download", methods=['GET'])
def download():
    #use session variable to query all stuff for broken object
    #print(session['broken_object'])
    server = 'srcp-database.database.windows.net'
    database = 'SRCP_Database'
    username = ''
    password = ''   
    driver= '{ODBC Driver 17 for SQL Server}'

    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()

    dbdata = cursor.execute("SELECT TOP 1 FileData,FileName FROM dbo.Files").fetchone()
    #print(dbdata[0]) #<--------- binary data
    buffer = io.BytesIO()
    buffer.write(dbdata[0])
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, attachment_filename='Output.png', mimetype='png')

@app.route("/about_us")
def about_us():
    return render_template("about_us.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")