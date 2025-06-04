from banco.BancoMySql import BancoMysql
from datetime import date

class Emprestimo:
    def __init__(self, livro_id: str, usuario_id: int, data_emprestimo: date = date.today(), data_devolucao: date = None, id: int = None):
        self.__id = id
        self.__livro_id = livro_id
        self.__usuario_id = usuario_id
        self.__data_emprestimo = data_emprestimo
        self.__data_devolucao = data_devolucao

    def __str__(self):
        return f"ID: {self.__id}, Livro: {self.__livro_id}, Usuário: {self.__usuario_id}, Empréstimo: {self.__data_emprestimo}, Devolução: {self.__data_devolucao}"

    def salvar_no_banco(self, banco: BancoMysql):
        if not banco.conectar():
            return

        # Verificar se livro existe e está disponível
        livro = banco.executar_query(1, "SELECT status FROM livros WHERE isbn = %s", (self.__livro_id,))
        if not livro:
            print("❌ Livro não encontrado.")
            banco.fechar_conexao()
            return
        if livro[0]["status"] != "disponivel":
            print("❌ Livro não está disponível.")
            banco.fechar_conexao()
            return

        # Verificar se usuário existe
        usuario = banco.executar_query(1, "SELECT id FROM usuarios WHERE id = %s", (self.__usuario_id,))
        if not usuario:
            print("❌ Usuário não encontrado.")
            banco.fechar_conexao()
            return

        # Inserir empréstimo
        banco.executar_query(2, """
            INSERT INTO emprestimos (livro_id, usuario_id, data_emprestimo)
            VALUES (%s, %s, %s)
        """, (self.__livro_id, self.__usuario_id, self.__data_emprestimo))

        # Atualizar status do livro para "emprestado"
        banco.executar_query(2, "UPDATE livros SET status = 'emprestado' WHERE isbn = %s", (self.__livro_id,))
        banco.fechar_conexao()
        print("✅ Empréstimo registrado com sucesso.")

    @staticmethod
    def registrar_devolucao(banco: BancoMysql, emprestimo_id: int, data_devolucao: date = date.today()):
        if banco.conectar():
            # Atualizar data de devolução
            banco.executar_query(2, """
                UPDATE emprestimos
                SET data_devolucao = %s
                WHERE id = %s
            """, (data_devolucao, emprestimo_id))

            # Buscar ID do livro relacionado
            livro_id = banco.executar_query(1, "SELECT livro_id FROM emprestimos WHERE id = %s", (emprestimo_id,))
            if livro_id:
                banco.executar_query(2, "UPDATE livros SET status = 'disponivel' WHERE isbn = %s", (livro_id[0]["livro_id"],))

            banco.fechar_conexao()
            print("📦 Devolução registrada.")
