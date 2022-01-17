from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'POST':
    email = request.form.get('email')
    first_name = request.form.get('firstName')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    user = User.query.filter_by(email=email).first()
    if user:
      flash('Email already exists.', category='error')
    elif len(email) < 4:
      flash('Email must be greater than 3 characters.', category="error")
    elif len(first_name) < 2:
      flash('First name must be greater than 1 characters.', category="error")
    elif password1 != password2:
      flash('Passwords don\'t match.', category="error")
    elif len(password1) < 6:
      flash('Password must be at least 6 characters.', category="error")
    else:
      # add user to the database
      new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256')) # creating a new user entity
      db.session.add(new_user) # adding a user to db
      db.session.commit() # commit that change to database
      login_user(new_user, remember=True)
      # login_user(user, remember=True)
      flash('Account created!', category='success')
      return redirect(url_for('views.home'))
  
  return render_template("signup.html", user=current_user)
  

@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user:
      if check_password_hash(user.password, password):
        login_user(user, remember=True)
        flash('Logged in successfully.', category='success')
        return redirect(url_for('views.home'))
      else:
        flash('Incorrect password, try again.', category='error')
    else:
      flash('Email does not exist.', category='error')

  return render_template("login.html", user=current_user) # passing a variable 'user', to use it later in templates

@auth.route('/logout')
@login_required
def loguot():
  logout_user()
  return redirect(url_for('auth.login'))