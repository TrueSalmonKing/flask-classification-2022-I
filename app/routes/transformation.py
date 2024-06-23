import redis
from flask import render_template
from rq import Connection, Queue
from rq.job import Job

from app import app
from app.forms.transformation_form import TransformationForm
from ml.classification_utils import fetch_image
from config import Configuration

from PIL import ImageEnhance
from base64 import b64encode
import io

config = Configuration()


@app.route('/transformation', methods=['GET', 'POST'])
def transformation():
    """API for selecting an image and applying transformations
    using the provided values for the four defined transformations: 
    color, brightness, contrast and sharpness.
    Returns both the original image and the transformed image."""
    form = TransformationForm()
    if form.validate_on_submit():  # POST
        image_id = form.image.data
        color = form.color.data
        brightness = form.brightness.data
        contrast = form.contrast.data
        sharpness = form.sharpness.data

        # Apply the image transformations and returning a base64 
        # image data string to be displayed
        transformed_img = transform(image_id, color, brightness, contrast, sharpness)
        img = io.BytesIO()
        transformed_img.save(img, format='JPEG')
        transformed_img = b64encode(img.getvalue()).decode()

        # Render the template with the image transformation
        return render_template('transformation_output.html', 
            image_id=image_id,
            color=color,
            brightness=brightness,
            contrast=contrast,
            sharpness=sharpness,
            transformed_img=transformed_img)

    # otherwise, it is a get request and should return the
    # image and the transformation values selection
    return render_template('transformation_select.html', form=form)


def transform(image_id, color, brightness, contrast, sharpness):
    # Fetch the image to compute the transformations
    image = fetch_image(image_id)

    # Apply color transformation
    enhancer = ImageEnhance.Color(image)
    transformed_img = enhancer.enhance(color)

    # Apply brightness transformation
    enhancer = ImageEnhance.Brightness(transformed_img)
    transformed_img = enhancer.enhance(brightness)

    # Apply contrast transformation
    enhancer = ImageEnhance.Contrast(transformed_img)
    transformed_img = enhancer.enhance(contrast)

    # Apply sharpness transformation
    enhancer = ImageEnhance.Sharpness(transformed_img)
    transformed_img = enhancer.enhance(sharpness)

    return transformed_img
