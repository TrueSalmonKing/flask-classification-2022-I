from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, InputRequired

from app.utils.list_images import list_images
from config import Configuration

conf = Configuration()


class TransformationForm(FlaskForm):
    image = SelectField('image', choices=list_images(), validators=[DataRequired()])
    color = FloatField('color', default=1.0, validators=[InputRequired()])
    brightness = FloatField('brightness', default=1.0, validators=[InputRequired()])
    contrast = FloatField('contrast', default=1.0, validators=[InputRequired()])
    sharpness = FloatField('sharpness', default=1.0, validators=[InputRequired()])
    submit = SubmitField('Submit')
