from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_data = request.form.get('email')
        password_data = request.form.get('password')

        # check if user exist in DB and if passwords match
        user_exists = User.query.filter_by(email=email_data).first()
        if user_exists:
            if check_password_hash(user_exists.password, password_data):
                flash('You are logged in!', category='success')
                login_user(user_exists, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Your password is incorrect.', category='error')
        else:
            flash('Your email does not exist.', category='error')
    return render_template('login.html')


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email_data = request.form.get('email')
        username_data = request.form.get('username')
        password_1_data = request.form.get('password_1')
        password_2_data = request.form.get('password_2')

        # check if user already exists and if passwords are valid
        # todo verify email
        email_exists = User.query.filter_by(email=email_data).first()
        username_exist = User.query.filter_by(username=username_data).first()
        if email_exists:
            flash('This email is already in use.', category='error')
        elif username_exist:
            flash('This username is already in use.', category='error')
        elif password_1_data != password_2_data:
            flash('Passwords don\'t match!', category='error')
        elif len(username_data) < 4:
            flash('Username is too short', category='error')
        elif len(password_1_data) < 6:
            flash('Password is too short', category='error')
        else:
            new_user = User(email=email_data,
                            username=username_data, password=generate_password_hash(password_1_data, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created')
            return redirect(url_for('views.home'))

    return render_template('signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))
