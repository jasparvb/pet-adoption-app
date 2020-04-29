from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Optional, URL, NumberRange

class AddPetForm(FlaskForm):
    """Form for adding pets."""

    name = StringField("Pet Name", validators=[InputRequired()])
    species = SelectField("Species", choices=[("cat","Cat"), ("dog","Dog"), ("porcupine","Porcupine")])
    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    age = IntegerField("Age", validators=[Optional(), NumberRange(min=0, max=30)])
    notes = TextAreaField("Notes")


class EditPetForm(FlaskForm):
    """Form for editing pets."""

    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    notes = TextAreaField("Notes")
    available = BooleanField("Available")
