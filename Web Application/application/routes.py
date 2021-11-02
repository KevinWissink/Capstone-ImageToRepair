from application import app
from flask import Flask, request, redirect, url_for, render_template
import os
import requests

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

    r = requests.post(url,data=uploaded_file.stream,headers=headers)
    return redirect(url_for('index'))

@app.route("/about_us")
def about_us():
    return render_template("about_us.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")