from flask import Blueprint, render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
#import bb_api.py as bb

auth = Blueprint('auth', __name__)



@auth.route('/login')
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if (not user or not check_password_hash(user.password, password)):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    if(user and check_password_hash(user.password, password)):
        return redirect(url_for('main.profile'))

@auth.route('/apple')
def apple():
    return render_template('apple.html')

@auth.route('/sign')
def sign():
    return render_template('signup.html')

@auth.route('/signup', methods=["GET","POST"])
def signup():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
    
    if (user): # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
   
    return redirect(url_for('main.profile'))

 
@auth.route('/logout')
def logout():
    return 'Logout'