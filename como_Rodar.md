# Como rodar o projeto

## 1º passo

É necessário ter instalado o postgresql, python (3.12+) e clonar o repositório:

```
git clone https://github.com/Kyamel/mugennodb
```

## 2º passo

Criar um arquivo `.env` na raiz do projeto, onede deve conter o nome do banco dados, senha, porta, etc. Um exempo esta abaixo:

```
DB_USER="postgres"
DB_PASSWORD="postgres"
DB_HOST="127.0.0.1"
DB_PORT="5432"
DB_NAME="ColoqueAquiONomeDoBanco"
```

## 3º abra o terminal na raiz do projeto (`MUGENNODB`) e execute os comandos abaixo:

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
<img width="882" height="137" alt="Captura de tela de 2025-08-20 22-40-37" src="https://github.com/user-attachments/assets/9259f2b6-7961-490d-9845-66b95c5d3ba7" />

Digite `help` para exibir os comandos.
