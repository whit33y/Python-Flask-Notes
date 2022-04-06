from flask import Blueprint,render_template, request, flash,redirect,url_for  #Umozliwia dodawanei sciezek i zachowania porzadku miedzy nimi 
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first() #szuaknie takiego uzytkownika w bazie
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorect password or email, try again', category='error')
        else:
            flash('Incorect email or password, try again', category='error')
    return render_template('login.html', user=current_user)   
    # return render_template('login.html', text='Testing jinja', boolean=True)
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup',methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password = request.form.get('password')
        passwordConfirm = request.form.get('passwordConfirm')
        user = User.query.filter_by(email=email).first() #szuaknie czy nie ma juz takiego uzytkownika
        if user:
            flash('Email already exist', category='error')
        #fails
        elif len(email)<4:
            flash('Email must be greater than 4 characters. ', category='error')
        elif len(first_name)<2:
            flash('First name must be greater than 1 characters. ', category = 'error')
        elif password != passwordConfirm:
            flash('Passwords don\'t match ', category = 'error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters ', category = 'error')
        #good
        else:
            #pass informations to db
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created succesfully!', category='success')
            return  redirect(url_for('views.home'))
    return render_template('signup.html',user=current_user)


