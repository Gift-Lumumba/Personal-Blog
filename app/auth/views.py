from flask import render_template,redirect,url_for
from ..models import User
from .forms import RegistrationForm
from .. import db
from . import auth

@auth.route('/login')
def login():
    return render_template('auth/login.html')

@auth.route('/register',methods = ["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()

        # mail_message("Welcome to pitch","email/welcome_user",user.email,user=user)
        # mail_message("Welcome to watchlist","email/welcome_user",user.email ,user=user)

        return redirect(url_for('auth.login'))
        title = "New Account"

    return render_template('auth/register.html',registration_form = form)
