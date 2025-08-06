# Nestspet - Diretrizes para Desenvolvimento de Banco de Dados

## Referência Principal

Sempre consulte o [Database Model](../docs/DATABASE_MODEL.md) como referência para a estrutura do banco de dados.

## Padrão de Implementação

### 1. Criação de Tabelas

Para cada nova tabela no banco de dados, seguir o fluxo:

1. **Model**:
   - Criar uma dataclass em `mugennocore/models/<nome_tabela>.py`
   - Usar `@dataclass(slots=True)` para otimização de memória
   - Exemplo:

     ```python
        from dataclasses import dataclass

        @dataclass(slots=True)
        class User:
            id: int
            name: str
            email: str
     ```

2. **Interface**:
   - Criar interface correspondente em `mugennocore/interfaces/<nome_tabela>.py`
   - Exemplo:

     ```python
        from typing import Protocol, runtime_checkable

        @runtime_checkable
        class IUser(Protocol):
            id: int
            user_name: str
            user_password: str
            user_role: str
            join_date: datetime
            email: str
            is_banned: bool
            nickname: str
            user_profile: UUID
            user_banner: UUID
            is_active: bool
            allow_nsfw: bool
            allow_dm: bool
            created_at: datetime
            updated_at: datetime

            def __str__(self) -> str: ...
            def __repr__(self) -> str: ...
     ```

### 2. Mapeamento Banco-Model

3. **Mapping**:
   - Criar função em `mugennodb/mapping/<nome_tabela>.py`
   - Converter `asyncpg.Record` para a dataclass do model
   - Exemplo:

     ```python
        from mugennocore.models.user import User
        from asyncpg import Record  # type: ignore

        def record_to_manga(record: Record) -> User:
            return User(
                id=record['id'],
                name=record['name'],
                email=record['email']
            )
     ```

### 3. Operações no Banco

4. **Database Interface**:
   - Implementar em `mugennodb/interfaces/<nome_tabela>.py`
   - Funções devem retornar objetos do mapping
   - Inserções devem receber interfaces do core
   - Exemplo:

     ```python
        from mugennocore.interfaces.user import IUser
        from mugennodb.database.mapping.user_map import record_to_manga
        from mugennodb.conection.database_protocol import DatabaseProtocol

        async def insert_user(db: DatabaseProtocol, user: IUser) -> User:
            record = await db.fetchrow(
                "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *",
                user.name, user.email
            )
            return record_to_manga(record)
     ```

### 4. Testes no REPL

5. **Endpoint para REPL**:
   - Criar em `app/endpoints/db_<nome>_endpoints.py`
   - Definir `COMMANDS` dict e função `handle_command`
   - Exemplo:

     ```python
        from mugennodb.interfaces.user import insert_user
        from mugennocore.interfaces.user import IUser

        COMMANDS = {
            "insert_user": {
                "description": "Create test user with default values",
                "args": ["--role:str?", "--username:str?"],
                "example": "insert_user --role=admin --username=test",
            },
        }

        async def handle_command(db, parts: list[str]) -> None:
            if parts[0] == 'insert_user' and len(parts) == 3:
                user = IUser.create(parts[1], parts[2])
                result = await insert_user(db, user)
                print(f"Usuário criado: {result}")

     ```

6. **Integração no Main**:
   - Adicionar em `app/main.py`:

     ```python
        await db_user_endpoints.handle_command(db, parts)
     ```

## Boas Práticas

- Sempre usar type hints
- Manter consistência entre nomes de tabelas, models e interfaces
- Documentar todas as funções com docstrings
- Implementar testes unitários para cada camada
- testar com o comando `mypy .` para buscar por erros de tipagem antes de fazer pull request.
