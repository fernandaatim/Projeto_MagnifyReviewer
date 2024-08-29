from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class ContactUsForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message="Name is required")])
    site = StringField('Site', validators=[DataRequired(message="Site is required")])
    email = StringField('Email', validators=[DataRequired(message="Email is required")])
    message = TextAreaField('Message', validators=[DataRequired(message="Message is required")])
