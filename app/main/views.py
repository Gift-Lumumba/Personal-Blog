from flask import render_template
from . import main
from flask_login import login_required
# from .models import review
# from .forms import ReviewForm

# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Welcome to Personal Blog'
    return render_template('index.html',title = title)


@main.route('/blog/new/', methods = ['GET','POST'])
@login_required
def new_blog():

    form = BlogForm()
    if category is None:
        abort( 404 )

    if form.validate_on_submit():
        blog= form.content.data, form.category_id.data
        # category_id = form.category_id.data
        new_blog= Blog(blog = blog)
    

        new_pitch.save_pitch()
        return redirect(url_for('main.index'))

    return render_template('new_blog.html', new_blog_form= form, category= category)