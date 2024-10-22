from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import create_user, get_user_by_email
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = get_user_by_email(email)
        if user and check_password_hash(user[3], password):  
            session['user_id'] = user[0]  
            session['user_name'] = user[1]  
            return redirect(url_for('tasks.view_tasks'))
        else:
            flash('Invalid email or password')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        create_user(name, email, hashed_password)
        return redirect(url_for('auth.login'))
    return render_template('register.html')
