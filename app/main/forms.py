from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Required

class BlogForm(FlaskForm):
    title = StringField('Blog Title', validators = [Required()])
    post = TextAreaField('Blog Content', validators = None)
    submit = SubmitField('Submit')

class SubscriptionForm(FlaskForm):
    email = StringField('Email', validators = [Required()])
    submit = SubmitField('Subscribe')