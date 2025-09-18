from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            return render_template('register.html', error='Email already registered')
        
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            response = redirect(url_for('main.index'))
            response.set_cookie('access_token', access_token)
            return response
        
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    response = redirect(url_for('main.index'))
    response.set_cookie('access_token', '', expires=0)
    return response