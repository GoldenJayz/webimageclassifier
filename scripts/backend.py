"""
    ------------------------

    Author: Jaden D
    Date Created: 6/24/2021
    Last Modified: 6/25/2021

    ------------------------

    End Goal:
        1. Create a website that spits out the data from the image recognition ai
        2. Get the percentage/data put into a json file in order to read the data
        3. Make the program run fast

    ------------------------

    Plans:
        1. Create the web backend using basic flask knowledge
        2. Setup the directories correctly
        3. Get the data updated every couple seconds
        4. A certain event in the webpage will trigger the backend to save the image provided in the input box box
        5. Check the Operating System this is being hosted
        6. Both images will be downloaded into the correct directories and the python backend will run a .bat file or .sh file to run it
        7. This will trigger retrain.py to train the ai
        8. Once that process is done another .bat script will run label_image.py to give it a classification
        9. Once done the data will be written into a .json file and frontend JavaScript will be used to check the JSON file for the website

    ------------------------

    Next:
        1. Get a way to seperate 2 images into 2 different folders
    
"""

import os
from flask import Flask, redirect, url_for, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'C:\\Users\\jmdan\\WebsiteAiImageClassifier\\tf_files\\DataSet\\Person' 
# make config for these
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            os.system(r"C:\Users\jmdan\WebsiteAiImageClassifier")
            os.system("python -m scripts.retrain  --bottleneck_dir=tf_files/bottlenecks  --how_many_training_steps 500 --model_dir=tf_files/models/mobilenet_0.50_224  --architecture=mobilenet_0.50_224  --summaries_dir=tf_files/training_summaries/mobilenet_0.50_224   --output_graph=tf_files/retrained_graph.pb --output_labels=tf_files/retrained_labels.txt --image_dir=tf_files/DataSet/")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="192.168.1.24", port="4200")

