from . import db
# from werkzeug.security import generate_password_hash,check_password_hash
# from flask_login import UserMixin
# from . import login_manager
# from datetime import datetime

# @login_manager.user_loader
# def load_user(user_id):
#   return User.query.get(int(user_id))


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))

    the_blog = db.relationship('Blog', backref='user', lazy='dynamic')
    the_comment = db.relationship('Comment', backref = 'user', lazy = 'dynamic')
    delete = db.relationship('Delete', backref = 'user', lazy = 'dynamic')
    update = db.relationship('Update', backref = 'user', lazy = 'dynamic')

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

    def __repr__(self):
        return f'User {self.name}'