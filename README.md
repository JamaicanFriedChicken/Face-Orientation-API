# Face-Orientation-API

This Flask REST API accepts an input image of a face from the user disregarding the image's metadata. The model then classifies the image's position as either rotated to a certain degree such as 90, 180, 270 and 360. Once classified, the model begins to correct the image and returns it in an upright position i.e. 0 or 360 degrees. If the model finds nothing wrong with the image, it proceeds to output it back to the user.

The model was trained on images of faces scraped on Google Images. The quality of the dataset varied along the ways of from having close face up shot to a side angles. However the model was able to achieve an accuracy of 94% from testing. Model performs poorly on faces that are covered, wears accessories, poor lighting and varying slim faces. From working on this project _make_predict_function() from Keras was discovered to have improved the model and resolved some errors. However it is undocumented at the moment.

These 3 variables below should be leading to where you've saved the folder. E.g. 'path/to/the/file/myproj_model.h5' 'path/to/the/file/my_model_weightsl.h5' app.config['UPLOAD_FOLDER'] = 'path/to/the/file/static/tmp/'

NEURAL_NET_MODEL_PATH = 'path/to/the/file/myproj_model.h5'

model.load_weights('path/to/the/file/my_model_weights.h5')

app.config['UPLOAD_FOLDER'] ='path/to/the/file/static/tmp/'

To run this API, be sure to have installed the necessary dependencies required.

$ conda create --name yourenvname python=x.x

$ python app.py

In the web browser, type in 127.0.0.1/5000 or localhost:5000 to access the API.
