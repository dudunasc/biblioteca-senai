from flask import render_template, request, redirect, url_for, flash
from app import app, db, bcrypt
from app.models import Usuario
from flask_login import login_user, logout_user


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        perfil = request.form.get('perfil', 'Aluno')

        if not nome or not email or not senha:
            flash('Preencha todos os campos.', 'warning')
            return render_template('register.html')

        existing = Usuario.query.filter_by(email=email).first()
        if existing:
            flash('Este email já está registrado.', 'danger')
            return render_template('register.html')

        usuario = Usuario(
            nome=nome,
            email=email,
            senha=bcrypt.generate_password_hash(senha).decode('utf-8'),
            perfil=perfil
        )
        db.session.add(usuario)
        db.session.commit()
        flash('Conta criada com sucesso. Faça login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        user = Usuario.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.senha, senha):
            login_user(user)
            flash('Login realizado com sucesso.', 'success')
            return redirect(url_for('login'))
        flash('Credenciais inválidas.', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    flash('Você saiu.', 'info')
    return redirect(url_for('login'))

