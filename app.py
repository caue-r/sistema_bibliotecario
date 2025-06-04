from flask import Flask, render_template, request, redirect, url_for
from classes.livro import Livro
from classes.usuario import Usuario
from classes.emprestimo import Emprestimo
from banco.BancoMySql import BancoMysql

app = Flask(__name__)

# Página inicial
@app.route("/")
def index():
    return render_template("index.html")


# Cadastro de livros
@app.route("/livros/novo", methods=["GET", "POST"])
def cadastrar_livro():
    if request.method == "POST":
        isbn = request.form["isbn"]
        titulo = request.form["titulo"]
        autor = request.form["autor"]
        ano = int(request.form["ano"])

        livro = Livro(isbn, titulo, autor, ano)
        banco = BancoMysql("biblioteca")
        livro.salvar_no_banco(banco)

        return redirect(url_for("index"))

    return render_template("cadastrar_livro.html")


# Cadastro de usuários
@app.route("/usuarios/novo", methods=["GET", "POST"])
def cadastrar_usuario():
    if request.method == "POST":
        nome = request.form["nome"]
        cpf = request.form["cpf"]
        email = request.form["email"]

        usuario = Usuario(nome, cpf, email)
        banco = BancoMysql("biblioteca")
        usuario.salvar_no_banco(banco)

        return redirect(url_for("index"))

    return render_template("cadastrar_usuario.html")


# Realizar empréstimo
@app.route("/emprestimos/novo", methods=["GET", "POST"])
def realizar_emprestimo():
    banco = BancoMysql("biblioteca")

    if request.method == "POST":
        isbn = request.form["isbn"]
        usuario_id = int(request.form["usuario_id"])
        emprestimo = Emprestimo(livro_id=isbn, usuario_id=usuario_id)
        emprestimo.salvar_no_banco(banco)
        return redirect(url_for("index"))

    livros = Livro.listar_disponiveis(banco)
    usuarios = Usuario.listar_todos(banco)
    return render_template("realizar_emprestimo.html", livros=livros, usuarios=usuarios)


# Registrar devolução
@app.route("/emprestimos/devolver", methods=["GET", "POST"])
def registrar_devolucao():
    banco = BancoMysql("biblioteca")

    if request.method == "POST":
        emprestimo_id = int(request.form["emprestimo_id"])
        Emprestimo.registrar_devolucao(banco, emprestimo_id)
        return redirect(url_for("index"))

    if not banco.conectar():
        print("❌ Erro ao conectar com o banco!")
        return "Erro ao conectar com o banco."

    emprestimos_ativos = banco.executar_query(1, """
        SELECT e.id, l.titulo AS livro_titulo, u.nome AS usuario_nome
        FROM emprestimos e
        JOIN livros l ON e.livro_id = l.isbn
        JOIN usuarios u ON e.usuario_id = u.id
        WHERE e.data_devolucao IS NULL
    """) or []

    print("📋 Empréstimos ativos encontrados:", emprestimos_ativos)
    banco.fechar_conexao()

    return render_template("registrar_devolucao.html", emprestimos=emprestimos_ativos)


# Listagens
@app.route("/livros")
def listar_livros():
    banco = BancoMysql("biblioteca")
    livros = Livro.listar_disponiveis(banco)
    return render_template("listar_livros.html", livros=livros)


@app.route("/emprestimos")
def listar_emprestimos():
    banco = BancoMysql("biblioteca")
    emprestimos = Livro.listar_emprestados(banco)
    return render_template("listar_emprestimos.html", emprestimos=emprestimos)


@app.route("/usuarios")
def listar_usuarios():
    banco = BancoMysql("biblioteca")
    usuarios = Usuario.listar_todos(banco)
    return render_template("listar_usuarios.html", usuarios=usuarios)


if __name__ == "__main__":
    app.run(debug=True)
