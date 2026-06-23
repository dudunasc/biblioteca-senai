from flask import render_template, request, redirect, url_for, flash
from app import app, db, bcrypt
from app.models import Usuario, Livro, Emprestimo, Solicitacao
from app.forms import LivroForm, EmpretimoForm, SolicitacaoForm, UsuarioForm
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
from sqlalchemy import func


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
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
            return redirect(url_for('dashboard'))
        flash('Credenciais inválidas.', 'danger')
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    flash('Você saiu.', 'info')
    return redirect(url_for('login'))


# ==================== DASHBOARD ====================
@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal após login"""
    total_livros = Livro.query.count()
    total_emprestimos = Emprestimo.query.filter_by(status='ATIVO').count()
    total_solicitacoes = Solicitacao.query.filter_by(status='PENDENTE').count()
    
    context = {
        'total_livros': total_livros,
        'total_emprestimos': total_emprestimos,
        'total_solicitacoes': total_solicitacoes,
        'usuario': current_user
    }
    
    return render_template('dashboard.html', **context)


# ==================== LIVROS ====================
@app.route('/livros')
@login_required
def listar_livros():
    """Lista todos os livros do acervo"""
    livros = Livro.query.all()
    return render_template('bookList.html', livros=livros)


@app.route('/livro/<int:id>')
@login_required
def visualizar_livro(id):
    """Visualiza detalhes de um livro específico"""
    livro = Livro.query.get_or_404(id)
    return render_template('bookDetails.html', livro=livro)


@app.route('/livro/cadastro', methods=['GET', 'POST'])
@login_required
def cadastro_livro():
    """Cadastra um novo livro (apenas para administradores)"""
    if current_user.perfil != 'Administrador':
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('dashboard'))
    
    form = LivroForm()
    if form.validate_on_submit():
        existing = Livro.query.filter_by(isbn=form.isbn.data).first()
        if existing:
            flash('Este ISBN já está registrado.', 'danger')
            return render_template('bookRegister.html', form=form)
        
        livro = Livro(
            isbn=form.isbn.data,
            titulo=form.titulo.data,
            autor=form.autor.data,
            categoria=form.categoria.data,
            editora=form.editora.data,
            ano=form.ano.data,
            quantidade_total=form.quantidade_total.data,
            quantidade_disponivel=form.quantidade_total.data
        )
        db.session.add(livro)
        db.session.commit()
        flash(f'Livro "{livro.titulo}" cadastrado com sucesso.', 'success')
        return redirect(url_for('listar_livros'))
    
    return render_template('bookRegister.html', form=form)


# ==================== EMPRÉSTIMOS ====================
@app.route('/emprestimos')
@login_required
def listar_emprestimos():
    """Lista os empréstimos do usuário ou todos (se admin)"""
    if current_user.perfil == 'Administrador':
        emprestimos = Emprestimo.query.all()
    else:
        emprestimos = Emprestimo.query.filter_by(usuario_id=current_user.id).all()
    
    return render_template('loanList.html', emprestimos=emprestimos)


@app.route('/emprestimo/novo', methods=['GET', 'POST'])
@login_required
def novo_emprestimo():
    """Registra um novo empréstimo (apenas para administradores)"""
    if current_user.perfil != 'Administrador':
        flash('Você não tem permissão para realizar esta ação.', 'danger')
        return redirect(url_for('dashboard'))
    
    form = EmpretimoForm()
    
    # Popula as escolhas de usuários e livros
    form.usuario_id.choices = [(u.id, u.nome) for u in Usuario.query.all()]
    form.livro_id.choices = [(l.id, l.titulo) for l in Livro.query.all()]
    
    if form.validate_on_submit():
        livro = Livro.query.get(form.livro_id.data)
        
        if livro.quantidade_disponivel <= 0:
            flash('Não há exemplares disponíveis deste livro.', 'danger')
            return render_template('loanRegister.html', form=form)
        
        data_emprestimo = datetime.now().date()
        data_prevista = data_emprestimo + timedelta(days=14)
        
        emprestimo = Emprestimo(
            data_emprestimo=data_emprestimo,
            data_prevista=data_prevista,
            usuario_id=form.usuario_id.data,
            livro_id=form.livro_id.data,
            status='ATIVO'
        )
        
        livro.quantidade_disponivel -= 1
        
        db.session.add(emprestimo)
        db.session.commit()
        
        flash(f'Empréstimo realizado com sucesso. Devolução prevista para {data_prevista.strftime("%d/%m/%Y")}.', 'success')
        return redirect(url_for('listar_emprestimos'))
    
    return render_template('loanRegister.html', form=form)


# ==================== SOLICITAÇÕES ====================
@app.route('/solicitacoes')
@login_required
def listar_solicitacoes():
    """Lista as solicitações (apenas para administradores)"""
    if current_user.perfil != 'Administrador':
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('dashboard'))
    
    solicitacoes = Solicitacao.query.all()
    return render_template('requestList.html', solicitacoes=solicitacoes)


@app.route('/solicitacao/nova', methods=['GET', 'POST'])
@login_required
def nova_solicitacao():
    """Solicita a aquisição de um novo livro"""
    form = SolicitacaoForm()
    
    if form.validate_on_submit():
        solicitacao = Solicitacao(
            titulo_livro=form.titulo_livro.data,
            autor=form.autor.data or '',
            observacao=form.observacao.data or '',
            professor_id=current_user.id,
            status='PENDENTE',
            data_solicitacao=datetime.utcnow()
        )
        db.session.add(solicitacao)
        db.session.commit()
        flash('Solicitação realizada com sucesso. Aguarde análise.', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('requestRegister.html', form=form)


# ==================== RELATÓRIOS ====================
@app.route('/relatorio')
@login_required
def relatorio():
    """Gera relatório de livros por categoria"""
    if current_user.perfil != 'Administrador':
        flash('Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('dashboard'))
    
    dados = db.session.query(
        Livro.categoria,
        func.count(Livro.id).label('total')
    ).group_by(Livro.categoria).all()
    
    return render_template('report.html', dados=dados)


# ==================== USUÁRIOS ====================
@app.route('/usuario/cadastro', methods=['GET', 'POST'])
@login_required
def cadastro_usuario():
    """Cadastra um novo usuário (apenas para administradores)"""
    if current_user.perfil != 'Administrador':
        flash('Você não tem permissão para realizar esta ação.', 'danger')
        return redirect(url_for('dashboard'))
    
    form = UsuarioForm()
    
    if form.validate_on_submit():
        existing = Usuario.query.filter_by(email=form.email.data).first()
        if existing:
            flash('Este email já está registrado.', 'danger')
            return render_template('userRegister.html', form=form)
        
        usuario = Usuario(
            nome=form.nome.data,
            email=form.email.data,
            senha=bcrypt.generate_password_hash(form.senha.data).decode('utf-8'),
            perfil=form.perfil.data
        )
        db.session.add(usuario)
        db.session.commit()
        flash(f'Usuário "{usuario.nome}" cadastrado com sucesso.', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('userRegister.html', form=form)

