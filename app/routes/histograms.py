import redis
from flask import render_template
from rq import Connection, Queue
from rq.job import Job

from app import app
from app.forms.histogram_form import HistogramForm
from ml.classification_utils import classify_image
from config import Configuration

config = Configuration()

@app.route('/histograms', methods=['GET', 'POST'])
def histograms():
    """API for selecting an image and computing its 
    histogram. Returns an image of the histogram"""
    form = HistogramForm()
    if form.validate_on_submit():  # POST
        image_id = form.image.data
        return render_template("histogram_output.html", image_id=image_id)
    return render_template('histogram_select.html', form=form)
