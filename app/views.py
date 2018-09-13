from flask import render_template
from app import app
# from .models import review
# from .forms import ReviewForm

# Views
@app.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Welcome to Personal Blog'
    return render_template('index.html',title = title)