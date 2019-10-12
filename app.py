#This Flask REST API accepts a face image of any orientation then tries to predict
#what angle  the image is rotated at. 
#The port for this API is localhost:5000

#Import the required libraries
import os
import keras
import numpy as np
import numpy
from keras import backend, Sequential
from numpy import stack
from imageio import imread
from keras.models import load_model
from PIL import Image
from werkzeug.utils import secure_filename
from utils import (is_allowed_file, make_thumbnail)
from flask import (Flask, flash, render_template, redirect, request, session,
                   send_file, url_for)

#Declaring model as a global variable
global model

#Declaring the pre-trained Keras model's path directory and 
#loading the weights as well as the model into the API
NEURAL_NET_MODEL_PATH = 'D:/Python/Project/myproj_model.h5'
keras.backend.clear_session()
model = load_model(NEURAL_NET_MODEL_PATH)
model._make_predict_function()
model.load_weights('D:/Python/Project/my_model_weights.h5')

print('Model is loaded')

#Start of the Flask API
app = Flask(__name__)

#Declaring the root folder path 
app.config['SECRET_KEY'] = "S0merand0mk3y"
app.config['UPLOAD_FOLDER'] ='D:/Python/Project/static/tmp/'


#Homepage of the Flask API, checks whether user has interacted with the
#API; upload and submit their image to be classified as well as reporting if something was 
#done wrong.  
@app.route('/', methods=['GET', 'POST'])
def home():
	
    if request.method == 'GET':
        # show the upload form
        return render_template('home.html')
    
    if request.method == 'POST':
        # check if a file was passed into the POST request
        if 'image' not in request.files:
            flash('No file was uploaded.')
            return redirect(request.url)

        image_file = request.files['image']

        # if filename is empty, then assume no upload
        if image_file.filename == '':
            flash('No file was uploaded.')
            return redirect(request.url)

        # check to see if the file is "legit"
        if image_file and is_allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(filepath)

             #Once verified, image will be resized for Keras CNN model
            passed = make_thumbnail(filepath)
            if passed:
                return redirect(url_for('predict', filename=filename))
            else:
                return redirect(request.url)

#If an error occurs throughout the Flask App, used is linked to error page 
@app.errorhandler(500)
def server_error(error):
    """ Server error page handler """
    return render_template('error.html'), 500


#Checks if the user uploads a correct format of an image (jpeg,png etc.)
@app.route('/images/<filename>')
def images(filename):
    """ Route for serving uploaded images """
    images_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(images_path)

#Main core of the API, preprocesses image, performs prediction on model and input image
@app.route('/predict/<filename>')
def predict(filename):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img = Image.open(image_path)
    image_url = url_for('images', filename=filename)
            
    #reads and normalises the image for model to make predictions on image
    image_mtx = imread(image_path)
    image_mtx = image_mtx / 255.
    image_mtx = image_mtx.reshape(-1, 64, 64, 3)
    predictions = model.predict(image_mtx)
    
    #classification of the image's orientation
    angles = ['0', '180', '270', '90']
    angle = [0, 90, 180, 270]
    
    #Obtaining the confidence (accuracy) of model and predictions of image orientation
    confidence = str(round(max(predictions[0]), 4))
    predictions = angles[np.argmax(predictions)]
    print(predictions)
    
    #Compares the accuracy and predictions where if true angle is assigned a value.
    if confidence >= '0.8':
        if predictions == '270': angle = 270.0 
        elif predictions == '180': angle = 180.0
        elif predictions == '90': angle = 90.0
        elif predictions == '0' : angle = 0.0

    #rotates the image with the assigned angle then saves the image 
    z = img.rotate(angle)
    fixed_img = z
    fixed_img.save(os.path.join(app.config['UPLOAD_FOLDER'], 'fixed_' + filename))
    fixed_image_url = url_for('images', filename='fixed_' + filename)
    
    #Outputs the image's orientation, classification 
    #and the accuracy of the model to the website
    return render_template(
        'predict.html',
        image_url=image_url,
        img=fixed_image_url,
        predictions=predictions,
        confidence=confidence
    )


if __name__ == '__main__':
    app.run()
    app.config(debug=True) 
