import mysql.connector
from mysql.connector import errorcode

class BancoMysql:
    def __init__(self, esquema: str):
        self.__esquema = esquema
        self.__conexao = None
        self.__cursor = None

    def conectar(self) -> bool:
        try:
            self.__conexao = mysql.connector.connect(
                host='localhost',
                user='root',
                passwd='root',
                database=self.__esquema
            )
            self.__cursor = self.__conexao.cursor(dictionary=True)
            return True
        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_BAD_DB_ERROR:
                print(f'O banco de dados {self.__esquema} não existe!')
            elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Usuário ou senha inválidos!')
            else:
                print(error)
            return False

    def executar_query(self, tipo: int, query: str, params: tuple = ()) -> list | None:
        try:
            if not self.__conexao:
                print('Conexão não estabelecida.')
                return None

            self.__cursor.execute(query, params)

            if tipo == 1:
                return self.__cursor.fetchall()
            else:
                self.__conexao.commit()
        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_DUP_ENTRY:
                print('Erro: chave primária duplicada!')
            else:
                print(f'Erro ao executar a query: {error}')
            return None

    def fechar_conexao(self):
        if self.__conexao and self.__conexao.is_connected():
            self.__cursor.close()
            self.__conexao.close()
            print('Conexão encerrada!')
