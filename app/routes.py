from app            import app
from datetime       import date
from typing         import Final

from flask import (
    render_template,
    redirect,
    url_for,
    request,
    flash
)

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
PAGE_BOOK_ADMIN_LIST:    Final[str] = "bookAdminList.html"
PAGE_LOAN_REGISTER:      Final[str] = "loanRegister.html"
PAGE_BOOK_REGISTER:      Final[str] = "bookRegister.html"
PAGE_BOOK_LIST:          Final[str] = "bookList.html"
PAGE_BOOK_DETAILS:       Final[str] = "bookDetails.html"

PAGE_USER_LIST:          Final[str] = "userList.html"
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

    busca = request.args.get('busca', '')

    if busca:
        livros = Livro.query.filter(
            (Livro.titulo.ilike(f'%{busca}%')) |
            (Livro.autor.ilike(f'%{busca}%')) |
            (Livro.isbn.ilike(f'%{busca}%'))
        ).order_by(
            Livro.titulo
        ).all()

    else:
        livros = Livro.query.order_by(
            Livro.titulo
        ).limit(8).all()

    return render_template(
        HOME_PAGE,
        livros=livros
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

# ----- Livros (Administrador) -----
@app.route('/admin/livros')
@login_required
def listarLivrosAdmin():

    if ControllerUser.checkAdminPermission():

        livros = Livro.query.order_by(
            Livro.titulo.asc()
        ).all()

        return render_template(
            PAGE_BOOK_ADMIN_LIST,
            livros=livros
        )

    flash(
        'Acesso negado.',
        'danger'
    )

    return redirect(
        url_for('index')
    )


# ----- Editar Livro -----
@app.route('/livro/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editarLivro(id):

    if ControllerUser.checkAdminPermission():

        livro = Livro.query.get_or_404(id)

        form = LivroForm(obj=livro)

        if request.method == 'GET':
            form.categoria.data = livro.categoria_id

        checkForm(form)

        if form.validate_on_submit():

            livro.isbn = form.isbn.data
            livro.titulo = form.titulo.data
            livro.autor = form.autor.data
            livro.categoria_id = form.categoria.data
            livro.editora = form.editora.data
            livro.ano = form.ano.data
            livro.quantidade_total = form.quantidade_total.data
            livro.quantidade_disponivel = form.quantidade_disponivel.data
            livro.resumo = form.resumo.data

            form.saveImageForBook(livro)

            db.session.commit()

            flash(
                'Livro atualizado com sucesso!',
                'success'
            )

            return redirect(
                url_for('listarLivrosAdmin')
            )

        return render_template(
            PAGE_BOOK_REGISTER,
            form=form,
            editando=True,
            livro=livro
        )

    flash(
        'Acesso negado.',
        'danger'
    )

    return redirect(
        url_for('index')
    )


# ----- Excluir Livro -----
@app.route('/livro/excluir/<int:id>', methods=['POST'])
@login_required
def excluirLivro(id):

    if ControllerUser.checkAdminPermission():

        livro = Livro.query.get_or_404(id)

        db.session.delete(livro)
        db.session.commit()

        flash(
            'Livro excluído com sucesso!',
            'success'
        )

        return redirect(
            url_for('listarLivrosAdmin')
        )

    flash(
        'Acesso negado.',
        'danger'
    )

    return redirect(
        url_for('index')
    )


# ----- Empréstimo -----
@app.route('/emprestimo/novo', methods=['GET', 'POST'])
@login_required
def realizar_emprestimo():

    if ControllerUser.checkAdminPermission():

        form = EmprestimoForm()

        form.usuario_id.choices = [
            (usuario.id, usuario.nome)
            for usuario in Usuario.query.order_by(Usuario.nome).all()
        ]

        form.livro_id.choices = [
            (livro.id, livro.titulo)
            for livro in Livro.query.filter(
                Livro.quantidade_disponivel > 0
            ).order_by(Livro.titulo).all()
        ]

        checkForm(form)

        if form.validate_on_submit():
            resultado = ControllerEmprestimo.realizarEmprestimo(form)
            if resultado:
                flash(
                    'Empréstimo realizado com sucesso!',
                    'success'
                )

                return redirect(
                    url_for('realizar_emprestimo')
                )

            flash(
                'Não foi possível realizar o empréstimo. Verifique limite do usuário ou disponibilidade do livro.',
                'danger'
            )

        emprestimos = Emprestimo.query.filter_by(
            status='ATIVO'
        ).order_by(
            Emprestimo.data_prevista.asc()
        ).all()

        return render_template(
            PAGE_LOAN_REGISTER,
            form=form,
            emprestimos=emprestimos
        )

    flash('Acesso negado.', 'danger')
    return redirect(url_for('index'))


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

# ----- Receber Livro -----
@app.route('/emprestimo/devolver/<int:id>', methods=['POST'])
@login_required
def devolverLivro(id):

    if ControllerUser.checkAdminPermission():

        emprestimo = Emprestimo.query.get_or_404(id)

        emprestimo.status = 'DEVOLVIDO'
        emprestimo.data_devolucao = date.today()
        emprestimo.livro.quantidade_disponivel += 1

        db.session.commit()

        flash(
            'Livro recebido com sucesso!',
            'success'
        )

        return redirect(
            url_for('realizar_emprestimo')
        )

    flash(
        'Acesso negado.',
        'danger'
    )

    return redirect(
        url_for('index')
    )
