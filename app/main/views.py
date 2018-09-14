from flask import render_template, request, redirect, url_for, abort, g
from . import main
from .. import db
from .models import User,Blog,Comment
from flask_login import login_required, current_user
from .forms import BlogForm
from ..email import mail_message
import markdown2

# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    blogs = Blog.get_all_blogs()

    title = 'Home - Welcome to Personal Blog'
    return render_template('index.html',title = title,blogs = blogs)

#Admin section
@main.route('/admin/homepage')
@login_required
def homepage():

    '''
    View homepage template for admin
    '''
    if not current_user.admin:
        abort(403)
        
    return render_template('homepage.html', title = "Homepage")
#End of admin section

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html",user = user)

#BLOG SECTION

@main.route('/blog/<int:id>', methods = ["GET", "POST"])
def blog(id):
    '''
    Views route that displays a specific blog
    '''
    # display blog
    blog = Blog.query.get(id)

    # updating posted blog
    if blog is None:
        abort(404)
    format_blog = markdown2.markdown(blog.post, extras = ["code-friendly", "fenced-code-blocks"])

    # information from CommentForm
    name = request.args.get('name')
    email = request.args.get('email')
    comment = request.args.get('comment')

    if comment:
        new_comment = Comment(blog_id = blog.id, name = name, email = email,comment = comment)

        # Saving one's comment
        new_comment.save_comment()
        return redirect(url_for('.blog', id = blog.id))

    # displaying users' comments
    comments = Comment.get_comments(blog.id)

    title = 'Enter your Blog'
    return render_template('blog.html', blog = blog, title = title, comments = comments, format_blog = format_blog)

#blog delete and comment section

@main.route('/delete/blog/<int:id>', methods = ["GET", "POST"])
def delete_blog(id):
    blog = Blog.delete_blog(id)

    return redirect(url_for('.index'))

@main.route('/delete/comment/<int:id>', methods = ["GET", "POST"])
def delete_comment(id):
    comment = Comment.delete_comment(id)

    return redirect(url_for('.index'))
#end of blog delete and comment section

#new blog section
@main.route('/blog/new/<int:id>', methods = ["GET", "POST"])
def new_blog(id):

    form = BlogForm()
    user = User.query.filter_by(id = id).first()
    if form.validate_on_submit():
        title = form.title.data
        posted = form.posted.data

        # creating a new blog
        new_blog = Blog(title = title, posted = posted, user = current_user)

        # saving a new blog
        new_blog.save_blog()

        mail_message('New Post', 'email/update', user.email, user = user)

        return redirect(url_for('.index'))

    title = 'Write a New Blog'
    return render_template('new_blog.html', title = title, blog_form = form)
#end of new blog section
#END OF BLOG SECTION



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