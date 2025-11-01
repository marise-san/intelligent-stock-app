# Sistema de Gestão de Estoque

## Como iniciar o projeto

1. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

2. **Execute o aplicativo:**

```bash
python run.py
```

## Deploy no PythonAnywhere

1.  **Crie uma nova Web App:**
    *   No seu dashboard do PythonAnywhere, vá para a aba **Web**.
    *   Clique em **Add a new web app**.
    *   Escolha a opção **Manual configuration** e a versão do Python que você está usando (ex: Python 3.9).

2.  **Configure o Ambiente Virtual (Virtualenv):**
    *   Na aba **Web**, você verá uma seção **Virtualenv**. Clique no link para criar um novo ambiente virtual.
    *   Abra um **Bash console** no seu dashboard.
    *   Ative o ambiente virtual com o comando:
        ```bash
        workon my-virtualenv  # Substitua "my-virtualenv" pelo nome do seu ambiente virtual
        ```
    *   Navegue até o diretório do seu projeto (onde você clonou o repositório).
    *   Instale as dependências:
        ```bash
        pip install -r requirements.txt
        ```

3.  **Configure o arquivo WSGI:**
    *   Na aba **Web**, vá para a seção **Code** e clique no link do **WSGI configuration file**.
    *   Substitua o conteúdo do arquivo pelo seguinte código, ajustando o `path` para o diretório do seu projeto:
        ```python
        import sys
        path = '/home/seu-usuario/seu-projeto'  # Substitua pelo caminho do seu projeto
        if path not in sys.path:
            sys.path.append(path)

        from app import app as application
        ```

4.  **Configure os Arquivos Estáticos:**
    *   Na aba **Web**, vá para a seção **Static files**.
    *   Adicione um novo mapeamento:
        *   **URL:** `/static`
        *   **Directory:** `/home/seu-usuario/seu-projeto/app/static` (substitua com o caminho do seu projeto)

5.  **Configure o Banco de Dados:**
    *   O caminho do arquivo do banco de dados será diferente no PythonAnywhere.
    *   No seu código, em `config.py`, altere a `SQLALCHEMY_DATABASE_URI` para usar um caminho absoluto no PythonAnywhere:
        ```python
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join('/home/seu-usuario/seu-projeto', 'app.db') # Substitua pelo caminho do seu projeto
        ```

6.  **Recarregue a Web App:**
    *   Volte para a aba **Web** e clique no botão verde **Reload**.
    *   Sua aplicação estará disponível no endereço `seu-usuario.pythonanywhere.com`.
