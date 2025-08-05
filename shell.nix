{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python312       
    pkgs.poetry
  ];

  # Variáveis de ambiente para seu app
  DB_USER = "postgres";
  DB_PASSWORD = "postgres";
  DB_HOST = "127.0.0.1";
  DB_PORT = "5432";
  DB_NAME = "mugen";

  # Habilitar virtualenv no Poetry (opcional)
  POETRY_VIRTUALENVS_CREATE = "true";

  shellHook = ''
    export DB_USER="postgres"
    export DB_PASSWORD="postgres"
    export DB_HOST="localhost"
    export DB_PORT="5432"
    export DB_NAME="mugen"

    echo "Configure o PostgreSQL v17 com as mesmas variáveis de ambiente, ou altere as variáveis no arquivo .env."
    echo "Poetry e Python prontos."
    echo "Python instalado em: $(which python)"
    echo "Poetry instalado em: $(which poetry)"
  '';
}
