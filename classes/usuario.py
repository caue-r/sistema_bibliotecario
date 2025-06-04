from banco.BancoMySql import BancoMysql

class Usuario:
    def __init__(self, nome: str, cpf: str, email: str, id: int = None):
        self.__id = id
        self.__nome = nome
        self.__cpf = cpf
        self.__email = email

    def __str__(self):
        return f"ID: {self.__id}, Nome: {self.__nome}, CPF: {self.__cpf}, Email: {self.__email}"

    # Getters
    def get_id(self): return self.__id
    def get_nome(self): return self.__nome
    def get_cpf(self): return self.__cpf
    def get_email(self): return self.__email

    # Métodos de banco
    def salvar_no_banco(self, banco: BancoMysql):
        if banco.conectar():
            query = """
                INSERT INTO usuarios (nome, cpf, email)
                VALUES (%s, %s, %s)
            """
            banco.executar_query(2, query, (self.__nome, self.__cpf, self.__email))
            banco.fechar_conexao()

    @staticmethod
    def listar_todos(banco: BancoMysql):
        if banco.conectar():
            query = "SELECT * FROM usuarios"
            resultado = banco.executar_query(1, query)
            banco.fechar_conexao()
            return resultado

    @staticmethod
    def listar_que_fizeram_emprestimos(banco: BancoMysql):
        if banco.conectar():
            query = """
                SELECT DISTINCT u.nome
                FROM usuarios u
                JOIN emprestimos e ON u.id = e.usuario_id
            """
            resultado = banco.executar_query(1, query)
            banco.fechar_conexao()
            return resultado
