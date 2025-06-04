from banco.BancoMySql import BancoMysql

class Livro:
    def __init__(self, isbn: str, titulo: str, autor: str, ano: int, status: str = 'disponivel'):
        self.__isbn = isbn
        self.__titulo = titulo
        self.__autor = autor
        self.__ano = ano
        self.__status = status

    def __str__(self):
        return f"ISBN: {self.__isbn}, Título: {self.__titulo}, Autor: {self.__autor}, Ano: {self.__ano}, Status: {self.__status}"

    # Getters
    def get_isbn(self): return self.__isbn
    def get_titulo(self): return self.__titulo
    def get_autor(self): return self.__autor
    def get_ano(self): return self.__ano
    def get_status(self): return self.__status

    # Setters
    def set_status(self, status): self.__status = status

    # Salvar no banco
    def salvar_no_banco(self, banco: BancoMysql):
        if banco.conectar():
            query = """
                INSERT INTO livros (isbn, titulo, autor, ano, status)
                VALUES (%s, %s, %s, %s, %s)
            """
            banco.executar_query(2, query, (self.__isbn, self.__titulo, self.__autor, self.__ano, self.__status))
            banco.fechar_conexao()

    # Listar livros disponíveis
    @staticmethod
    def listar_disponiveis(banco: BancoMysql):
        if banco.conectar():
            query = "SELECT * FROM livros WHERE status = 'disponivel'"
            resultado = banco.executar_query(1, query)
            banco.fechar_conexao()
            return resultado

    # Listar livros emprestados com nome do usuário (via JOIN) – opcional
    @staticmethod
    def listar_emprestados(banco: BancoMysql):
        if banco.conectar():
            query = """
                SELECT l.titulo, u.nome
                FROM livros l
                JOIN emprestimos e ON l.isbn = e.livro_id
                JOIN usuarios u ON u.id = e.usuario_id
                WHERE l.status = 'emprestado'
            """
            resultado = banco.executar_query(1, query)
            banco.fechar_conexao()
            return resultado
