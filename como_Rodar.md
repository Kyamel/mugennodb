# Como rodar o projeto

## 1º passo

É necessário ter instalado o postgresql e o python

## 2º passo

Criar um arquivo `.env` na raiz do projeto, onede deve conter o nome do banco dados, senha, porta, etc. Um exempo esta abaixo:

```
DB_USER="postgres"
DB_PASSWORD="postgres"
DB_HOST="127.0.0.1"
DB_PORT="5432"
DB_NAME="ColoqueAquiONomeDoBanco"
```

## 3º abra o terminal na raiz do projeto (`MUGENNODB`) e executo os comandos abaixo:

Instalar poetry

```
pip install poetry
```

Instalar dependências

```
poetry install
```

Rodar o projeto

```
poetry run python app/main.py
```

Após executar este comando o terminal aparecerá assim:
