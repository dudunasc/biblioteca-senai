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
    Emprestimo,
    Solicitacao
)

from app.forms import (
    LoginForm,
    UsuarioForm,
    LivroForm,
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
                    url_for('index')
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


# ----- Escolha do Perfil ----- 
@app.route('/escolher-perfil')
def escolher_perfil():

    return render_template(
        'escolher_perfil.html'
    )


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