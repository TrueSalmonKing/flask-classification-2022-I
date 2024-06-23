import redis
from flask import render_template, request, flash, redirect
from rq import Connection, Queue
from rq.job import Job
import os
import time
import threading

from app import app
from app.forms.classification_upload_form import ClassificationUploadForm
from ml.classification_utils import classify_image
from config import Configuration

config = Configuration()

@app.route('/classifications_upload', methods=['GET', 'POST'])
def classifications_upload():
    """API for selecting a model and allowing the user to 
    upload an image before running a classification job, with
    the image being temporarily saved on the server. 
    Security checks are done to ensure the file is a valid
    image file before proceeding with the classification job. 
    Returns the output scores from the model."""
    form = ClassificationUploadForm()
    if form.validate_on_submit():  # POST
        model_id = form.model.data

        # Initial checks on the success of the upload
        if 'image' not in request.files:
            flash('No selected file')
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # Security check on the image tyep through the extension
        if not allowed_file(file.filename):
            flash('Invalid file. Please upload an image file (png, jpg or jpeg file)')
            return redirect(request.url)


        # Save the image into the imagenet images folder temporarily
        filename = save_image_temp(file)
        # Scheduling a background job to delete the uploaded image file
        # after 10 seconds
        threading.Thread(target=delete_temp_image, args=(filename,)).start()

        redis_url = Configuration.REDIS_URL
        redis_conn = redis.from_url(redis_url)
        with Connection(redis_conn):
            q = Queue(name=Configuration.QUEUE)
            job = Job.create(classify_image, kwargs={
                "model_id": model_id,
                "img_id": filename
            })
            task = q.enqueue_job(job)

        return render_template("classification_output_queue.html", image_id=filename, jobID=task.get_id())

    return render_template('classification_select_upload.html', form=form)

def allowed_file(filename):
    """Function used to validate the filename of the uploaded file
    prior to classifying it, to ensure only images are uploaded"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image_temp(file):
    """Function used to save the image file into the static_img
    folder temporarily"""
    filename = 'temp_img_'+str(time.time())
    file.save(os.path.join(config.image_folder_path, filename))

    return filename

def delete_temp_image(filename):
    """Function used to delete the uploadd file after 
    the classification
    """
    time.sleep(10)
    try:
        os.remove(os.path.join(config.image_folder_path, filename))
    except Exception as e:
        error_message = f"Error deleting temporary image {filename}: {e}"
        with open('error_log.txt', 'a') as f:
            f.write(error_message + '\n')
