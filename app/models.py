from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))


class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    email = db.Column(db.String(255),unique = True,index = True)
    admin = db.Column(db.Boolean,default = False)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))

    the_blog = db.relationship('Blog', backref='user', lazy='dynamic')
    the_comment = db.relationship('Comment', backref = 'user', lazy = 'dynamic')
    update = db.relationship('Update', backref = 'user', lazy = 'dynamic')
    delete = db.relationship('Delete', backref = 'user', lazy = 'dynamic')

    @property
    def password(self):
         raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def verify_password(self, password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f'{self.username}'

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    users = db.relationship('User',backref = 'role',lazy="dynamic")


class Blog(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer,primary_key = True)
    post = db.Column(db.String(), index = True)
    title = db.Column(db.String(255),index = True)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer,db.ForeignKey('categories.id'))
    comments = db.relationship('Comment', backref = 'blog', lazy = 'dynamic')
    update = db.relationship('Update', backref = 'blog', lazy = 'dynamic')
    delete = db.relationship('Delete', backref = 'blog', lazy = 'dynamic')

    def save_blog(self):
        '''
        Function that saves all blogs posted
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all_blogs(cls):
        '''
        Function that queries database and returns all posted blogs.
        '''
        return Blog.query.all()

    @classmethod
    def get_blogs_by_category(cls,category_id):
        '''
        Function that queries the database and returns all blogs per category passed.
        '''
        return Blog.query.filter_by(category_id = category_id)

    @classmethod
    def delete_blog(self, blog_id):
        comments = Comment.query.filter_by(blog_id = blog_id).delete()
        blog = Blog.query.filter_by(id = blog_id).delete()
        db.session.commit()


class Category(db.Model):
    '''
    Function that will define all the different categories of blogs.
    '''
    __tablename__ ='categories'


    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255))
    category_description = db.Column(db.String(255))

    @classmethod
    def get_categories(cls):
        '''
        Function that queries the database and returns all the categories from the database
        '''
        categories = Category.query.all()
        return categories


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(30),index = True)
    email = db.Column(db.String(30),index = True)
    blog_id = db.Column(db.Integer,db.ForeignKey('blogs.id'))
    comment=db.Column(db.String(255),index = True)
    posted = db.Column(db.DateTime,default=datetime.utcnow)

    
    def save_comment(self):
        '''
        Function that saves all comments made on a blog
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(blog_id=id).all()

    @classmethod
    def delete_comment(cls, id):
        comment = Comment.query.filter_by(id = comment_id).delete()
        db.session.commit()

        return comments

class Update(db.Model):
    __tablename__ = 'updates'

    id = db.Column(db.Integer,primary_key = True)
    blog_id = db.Column(db.Integer,db.ForeignKey('blogs.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    update = db.Column(db.Integer,default=1)

    def __repr__(self):
        return f'Update {self.update}'


class Delete(db.Model):
    __tablename__ = 'delete'

    id = db.Column(db.Integer,primary_key = True)
    blog_id = db.Column(db.Integer,db.ForeignKey('blogs.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    delete = db.Column(db.Integer,default=1)

    def __repr__(self):
        return f'Delete {self.delete}'