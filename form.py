from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.recaptcha import RecaptchaField

class ContactUsForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    site = StringField("Bosch's Site", validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    message = TextAreaField('About', validators=[DataRequired()])
    recaptcha = RecaptchaField()
