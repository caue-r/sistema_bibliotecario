# 📚 Sistema de Gerenciamento de Biblioteca

Projeto desenvolvido como atividade interdisciplinar das disciplinas de **Programação Orientada a Objetos (POO)** e **Banco de Dados (BD)**.

## 🧠 Objetivo

Criar um sistema simples de gerenciamento de biblioteca utilizando:
- Python + Flask
- MySQL
- Programação Orientada a Objetos
- Integração com banco de dados relacional

## 🛠️ Funcionalidades

- Cadastro de livros
- Cadastro de usuários
- Empréstimo de livros (com validações)
- Registro de devoluções
- Listagens de livros disponíveis, emprestados e usuários

## 🗂️ Estrutura do projeto

```
sistema_biblioteca/
├── app.py                      # Arquivo principal com rotas Flask
├── banco/
│   ├── BancoMySql.py           # Classe de conexão com MySQL
│   └── scriptdobancodedados.sql # Script SQL para criar as tabelas
├── classes/
│   ├── livro.py
│   ├── usuario.py
│   └── emprestimo.py
├── templates/                  # Páginas HTML (interface)
    ├── index.html
    ├── cadastrar_livro.html
    ├── cadastrar_usuario.html
    ├── realizar_emprestimo.html
    ├── registrar_devolucao.html
    └── listar_*.html
```

## 🚀 Como executar

1. **Instale as dependências:**
   ```bash
   pip install Flask mysql-connector-python
   ```

2. **Crie o banco de dados:**
   - Execute o script SQL `banco/scriptdobancodedados.sql` no seu MySQL local

3. **Configure o acesso ao banco:**
   - O acesso padrão está configurado como:
     - Host: `localhost`
     - User: `root`
     - Password: `root`
     - Banco: `biblioteca`

4. **Inicie a aplicação:**
   ```bash
   python app.py
   ```

5. **Acesse no navegador:**
   ```
   http://127.0.0.1:5000
   ```
