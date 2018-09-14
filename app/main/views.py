from flask import render_template, request, redirect, url_for, abort, g
from . import main
from .. import db
from .models import User,Blog,Comment
from flask_login import login_required, current_user
from .forms import BlogForm
from ..email import mail_message

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



@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html",user = user)

# @main.route('/user/<uname>/update',methods = ['GET','POST'])
# @login_required
# def update_profile(uname):
#     user = User.query.filter_by(username = uname).first()
#     if user is None:
#         abort(404)

#     form = UpdateProfile()

#     if form.validate_on_submit():
#         user.bio = form.bio.data

#         db.session.add(user)
#         db.session.commit()

#         return redirect(url_for('.profile',uname=user.username))

#     return render_template('profile/update.html',form =form)

# @main.route('/user/<uname>/update/pic',methods= ['POST'])
# @login_required
# def update_pic(uname):
#     user = User.query.filter_by(username = uname).first()
#     if 'photo' in request.files:
#         filename = photos.save(request.files['photo'])
#         path = f'photos/{filename}'
#         user.profile_pic_path = path
#         db.session.commit()
#     return redirect(url_for('main.profile',uname=uname))