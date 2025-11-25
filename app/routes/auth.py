from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter((User.username == username) | (User.email == username)).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))
        else:
            flash('Credenciais inválidas. Verifique seu usuário e senha.', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type')
        phone = request.form.get('phone')
        
        if User.query.filter_by(username=username).first():
            flash('Nome de usuário já existe.', 'danger')
            return render_template('register.html')
            
        if User.query.filter_by(email=email).first():
            flash('E-mail já cadastrado.', 'danger')
            return render_template('register.html')
            
        user = User(username=username, email=email, user_type=user_type, phone=phone)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
