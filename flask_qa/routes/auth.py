from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

from flask_qa.extensions import db
from flask_qa.models import User
from flask_qa import variables

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, validators, PasswordField, ValidationError

auth = Blueprint('auth', __name__)

class RegisterUserForm(FlaskForm):
    username = StringField('Enter Your Username:', [validators.DataRequired(), validators.Length(max=255), validators.Length(min=5)])
    password = PasswordField('Enter Your Password:', [validators.DataRequired(), validators.Length(max=255), validators.Length(min=5),validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match'), validators.Regexp("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", message="Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character")])
    confirm = PasswordField('Repeat Password')
    recaptcha = RecaptchaField()
    submit = SubmitField(label=('Submit'))

    def validate_username(form, field):
        if User.query.filter_by(name=field.data).first():
         raise ValidationError('This username is already in use')

@auth.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterUserForm(request.form)
    if form.validate_on_submit():
        name = form.username.data
        unhashed_password = form.password.data

        user = User(
            name=name, 
            unhashed_password=unhashed_password,
            admin=False,  
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    context = {
        'form' : form
    }

    return render_template('registerValid.html', **context)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        user = User.query.filter_by(name=name).first()

        error_message = ''

        if not user or not check_password_hash(user.password, password):
            error_message = 'Could not login. Please check and try again.'

        if not error_message:
            login_user(user)
            return redirect(url_for('main.index'))

    return render_template('login.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))