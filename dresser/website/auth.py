from flask import Blueprint, render_template, request, redirect, flash, url_for
from .models import User, Cloth
from . import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import base64

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(name=name).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('Logged in successfully👍', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Password Incorrect☹', category='error')
                return redirect(url_for('auth.login'))
        else:
            flash('User does not exist', category='error')
            return redirect(url_for('auth.login'))



    return render_template('login.html', user=current_user)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('username').lower()
        password = request.form.get('password')
        password_confirm = request.form.get('password2')
        image = request.files['p-image'].read()
        encoded_image = base64.b64encode(image).decode('utf-8')
        gender = request.form.get('gender')

        user = User.query.filter_by(name=name).first()
        if user:
            flash('A user with this name already exists☹', category='error')
        else:
            if password != password_confirm:
                flash('Passwords do not match', category='error')
            elif len(name) < 3:
                flash('Name should be at least 3 characters', category='error')
            elif len(password) < 4:
                flash('Password should be at least 4 characters', category='error')
            elif gender == None:
                flash('Please select a gender', category='error')
            else:
                if len(encoded_image) < 1:
                    new_user = User(name=name, password=generate_password_hash(password, method='sha256'), gender=gender)
                else:
                    new_user = User(name=name, password=generate_password_hash(password, method='sha256'), profile_pic=encoded_image, gender=gender)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Account has been created successfully👍', category='success')
                return redirect(url_for('views.home'))


    return render_template('signup.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))