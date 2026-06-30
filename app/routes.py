from app import app

from flask import (
    render_template,
    redirect,
    url_for,
    request,
    flash
)

from typing import Final

from app.models import (
    db,
    Usuario,
    Livro,
    Categoria,
    Emprestimo,
    Solicitacao
)

from app.forms import (
    LoginForm,
    UsuarioForm,
    LivroForm,
    CategoriaForm,
    EmprestimoForm,
    SolicitacaoForm
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from app.controllers.controllerUser import ControllerUser
from app.controllers.controllerLivro import ControllerLivro
from app.controllers.controllerEmprestimo import ControllerEmprestimo
from app.controllers.controllerSolicitacao import ControllerSolicitacao


HOME_PAGE:               Final[str] = "dashboard.html"
PAGE_LOGIN:              Final[str] = "login.html"
PAGE_ADMIN_PANEL:        Final[str] = "dashboardAdmin.html"
PAGE_CATEGORY_REGISTER:  Final[str] = "categoryRegister.html"
PAGE_CATEGORY_LIST:      Final[str] = "categoryList.html"


PAGE_USER_REGISTER:      Final[str] = "userRegister.html"
PAGE_USER_LIST:          Final[str] = "userList.html"

PAGE_BOOK_REGISTER:      Final[str] = "bookRegister.html"
PAGE_BOOK_LIST:          Final[str] = "bookList.html"
PAGE_BOOK_DETAILS:       Final[str] = "bookDetails.html"

PAGE_LOAN_REGISTER:      Final[str] = "loanRegister.html"

PAGE_STUDENT_PANEL:      Final[str] = "studentPanel.html"
PAGE_TEACHER_PANEL:      Final[str] = "teacherPanel.html"

PAGE_REQUEST_REGISTER:   Final[str] = "requestRegister.html"
PAGE_REQUEST_LIST:       Final[str] = "requestList.html"

PAGE_REPORT:             Final[str] = "report.html"


# ----- funcao auxiliar ----- 
def checkForm(form):
    if request.method == 'POST':
        form.validate()

        if form.errors:
            for msg in form.errors.values():
                flash(msg[0], 'danger')


# ----- Dashboard Público ----- 
@app.route('/')
def index():

    return render_template(
        HOME_PAGE
    )


# ----- Login ----- 
@app.route('/login', methods=['GET', 'POST'])
def login():

    if ControllerUser.isLoged():

        return redirect(
            url_for('index')
        )

    form = LoginForm()

    checkForm(form)

    if form.validate_on_submit():
        user = form.login()

        if user:
            login_user(user)

            flash(
                'Login realizado com sucesso!',
                'success'
            )

            if user.perfil == 'ADMIN':
                return redirect(
                    url_for('dashboardAdmin')
                )

            elif user.perfil == 'PROFESSOR':
                return redirect(
                    url_for('painel_professor')
                )

            elif user.perfil == 'ALUNO':
                return redirect(
                    url_for('painel_aluno')
                )

        flash(
            'Email ou senha inválidos.',
            'danger'
        )

    return render_template(
        PAGE_LOGIN,
        form=form
    )

# ----- Dashboard Admin ----- 
@app.route('/admin')
@login_required
def dashboardAdmin():

    if ControllerUser.checkAdminPermission():

        total_usuarios = Usuario.query.count()
        total_livros = Livro.query.count()
        total_emprestimos = Emprestimo.query.filter_by(status='ATIVO').count()
        total_solicitacoes = Solicitacao.query.count()

        ultimos_emprestimos = Emprestimo.query.filter_by(
            status='ATIVO'
        ).order_by(
            Emprestimo.data_emprestimo.desc()
        ).limit(5).all()

        proximas_devolucoes = Emprestimo.query.filter_by(
            status='ATIVO'
        ).order_by(
            Emprestimo.data_prevista.asc()
        ).limit(5).all()

        return render_template(
            PAGE_ADMIN_PANEL,
            total_usuarios=total_usuarios,
            total_livros=total_livros,
            total_emprestimos=total_emprestimos,
            total_solicitacoes=total_solicitacoes,
            ultimos_emprestimos=ultimos_emprestimos,
            proximas_devolucoes=proximas_devolucoes
        )

    flash('Acesso negado.', 'danger')
    return redirect(url_for('index'))

# ----- Dashboard Professor ----- 
@app.route('/professor')
@login_required
def painel_professor():

    return render_template(
        PAGE_TEACHER_PANEL
    )

# ----- Dashboard Aluno ----- 
@app.route('/aluno')
@login_required
def painel_aluno():

    return render_template(
        PAGE_STUDENT_PANEL
    )

# ----- Logout ----- 
@app.route('/usuario/sair')
@login_required
def logout():

    logout_user()

    flash(
        'Você saiu do sistema.',
        'success'
    )

    return redirect(
        url_for('index')
    )

# ----- Cadastro Usuário ----- 
@app.route('/usuario/cadastro', methods=['GET', 'POST'])
@login_required
def cadastrar_usuario():

    if ControllerUser.checkAdminPermission():

        form = UsuarioForm()

        checkForm(form)

        if form.validate_on_submit():

            form.saveUser()

            flash(
                'Usuário cadastrado com sucesso!',
                'success'
            )

            return redirect(
                url_for('index')
            )

        return render_template(
            PAGE_USER_REGISTER,
            form=form
        )

    flash(
        'Acesso negado.',
        'danger'
    )

    return redirect(
        url_for('index')
    )

# ----- Cadastro Livro ----- 
@app.route('/livro/novo', methods=['GET', 'POST'])
@login_required
def cadastrar_livro():

    if ControllerUser.checkAdminPermission():

        form = LivroForm()

        checkForm(form)

        if form.validate_on_submit():

            form.saveBook()

            flash(
                'Livro cadastrado com sucesso!',
                'success'
            )

            return redirect(
                url_for('listar_livros')
            )

        return render_template(
            PAGE_BOOK_REGISTER,
            form=form
        )

    flash(
        'Acesso negado.',
        'danger'
    )

    return redirect(
        url_for('index')
    )

# ----- Cadastro Categoria -----
@app.route('/categoria/cadastro', methods=['GET', 'POST'])
@login_required
def cadastrarCategoria():

    if ControllerUser.checkAdminPermission():

        form = CategoriaForm()

        checkForm(form)

        if form.validate_on_submit():

            categoria = Categoria(
                nome=form.nome.data,
                descricao=form.descricao.data
            )

            db.session.add(categoria)
            db.session.commit()

            flash(
                'Categoria cadastrada com sucesso!',
                'success'
            )

            return redirect(
                url_for('listarCategorias')
            )

        return render_template(
            PAGE_CATEGORY_REGISTER,
            form=form
        )

    flash('Acesso negado.', 'danger')

    return redirect(
        url_for('index')
    )


# ----- Listar Categorias -----
@app.route('/categorias')
@login_required
def listarCategorias():

    if ControllerUser.checkAdminPermission():

        categorias = Categoria.query.order_by(
            Categoria.nome
        ).all()

        return render_template(
            PAGE_CATEGORY_LIST,
            categorias=categorias
        )

    flash('Acesso negado.', 'danger')

    return redirect(
        url_for('index')
    )

# ----- Consulta ao acervo ----- 
@app.route('/livros')
def listar_livros():

    titulo = request.args.get(
        'titulo',
        ''
    )

    categoria = request.args.get(
        'categoria',
        ''
    )

    livros = ControllerLivro.filtrarLivros(
        titulo,
        categoria
    )

    return render_template(
        PAGE_BOOK_LIST,
        livros=livros
    )

# ----- Detalhes dos livros ----- 
@app.route('/livro/<int:id>')
def visualizar_livro(id):

    livro = ControllerLivro.getBookById(id)

    return render_template(
        PAGE_BOOK_DETAILS,
        livro=livro
    )

# ----- Empréstimo ----- 
@app.route('/emprestimo/novo', methods=['GET', 'POST'])
@login_required
def realizar_emprestimo():

    if ControllerUser.checkAdminPermission():

        form = EmprestimoForm()

        checkForm(form)

        if form.validate_on_submit():

            ControllerEmprestimo.realizarEmprestimo(form)

            flash(
                'Empréstimo realizado com sucesso!',
                'success'
            )

            return redirect(
                url_for('index')
            )

        return render_template(
            PAGE_LOAN_REGISTER,
            form=form
        )

    flash(
        'Acesso negado.',
        'danger'
    )

    return redirect(
        url_for('index')
    )

# ----- Solicitacao de aquisição ----- 
@app.route('/solicitacao/nova', methods=['GET', 'POST'])
@login_required
def solicitar_aquisicao():

    form = SolicitacaoForm()

    checkForm(form)

    if form.validate_on_submit():

        ControllerSolicitacao.salvarSolicitacao(
            form,
            current_user.id
        )

        flash(
            'Solicitação enviada com sucesso!',
            'success'
        )

        return redirect(
            url_for('painel_professor')
        )

    return render_template(
        PAGE_REQUEST_REGISTER,
        form=form
    )

# ----- Relatórios ----- 
@app.route('/relatorio')
@login_required
def relatorio():

    if ControllerUser.checkAdminPermission():

        dados = ControllerEmprestimo.gerarRelatorio()

        return render_template(
            PAGE_REPORT,
            dados=dados
        )

    flash(
        'Acesso negado.',
        'danger'
    )

    return redirect(
        url_for('index')
    )