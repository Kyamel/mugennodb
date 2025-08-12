# Nestspet - Diretrizes para Desenvolvimento de Banco de Dados

## Referência Principal

Sempre consulte o [Database Model](./docs/DATABASE_MODEL.md) como referência para a estrutura do banco de dados.

## Padrão de Implementação

### 1. Criação de Tabelas em `mugennocore/`

Para cada nova tabela criada no banco de dados em `000_init.sql`, seguir o fluxo:

1. **Model**:  
   Criar uma dataclass em `mugennocore/models/<nome_tabela_singular>.py`.  
   Usar `@dataclass(slots=True)` para otimização de memória  
   Exemplo:  

     ```python
        from dataclasses import dataclass

        @dataclass(slots=True)
        class User:
            id: int
            name: str
            email: str
     ```

2. **Interface**:  
   Criar interface correspondente em `mugennocore/interfaces/i<nome_tabela_singular>.py`.  
   Exemplo:  

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

### 2. Mapeamento Banco-Model em `mugennodb/`

1. **Mapping**:  
   Criar função em `mugennodb/mapping/<nome_tabela_singular>_map.py`.  
   Converter `asyncpg.Record` para a dataclass do model.  
   Exemplo:  

     ```python
        from typing import Optional
        from asyncpg import Record  # type: ignore
        from mugennocore.model.user import User

        def record_to_manga(record: Record) -> Optional[User]:
            if row is None:
                return None
            return User(
                id=record['id'],
                name=record['name'],
                email=record['email']
            )
     ```

### 3. Operações no Banco em `mugennodb/`

1. **Database Interface**:  
   Implementar em `mugennodb/interfaces/<nome_tabela>.py`.  
   Funções devem retornar objetos do mapping.  
   Inserções devem receber interfaces do core.  
   Exemplo:  

     ```python
        from mugennocore.interfaces.user import IUser
        from mugennodb.database.mapping.user_map import record_to_manga
        from mugennodb.conection.database_protocol import DatabaseProtocol

        async def insert_user(db: DatabaseProtocol, user: IUser) -> int:
            record = await db.fetchrow(
                "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *",
                user.name, user.email
            )
            return record["id"] if record else -1
     ```

### 4. Testes no REPL em `app/`

1. **Endpoint para REPL**:  
    Criar em `app/endpoints/db_<nome_tabela_singular>_endpoints.py`.  
    Definir `COMMANDS` dict e função `handle_command`.  
    Exemplo:  

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

        def parse_args_key_value(parts: list[str]) -> dict[str, str]:
            """
            Converts parts ["user_id=101", "--role=admin"] in {"user_id": "101", "role": "admin"}
            """
            args = {}
            for part in parts:
                if "=" in part:
                    key, value = part.lstrip("-").split("=", 1)
                    args[key] = value
            return args

        async def handle_command(db, parts: list[str]) -> None:
            cmd = parts[0]
            if cmd not in COMMANDS:
                print(f"Unknown command: {cmd}")
                return

            args_def = COMMANDS[cmd]["args"]
            required_keys = [arg.split(":")[0] for arg in args_def if not arg.startswith("--")]
            args = parse_args_key_value(parts[1:])

            # Check required args
            for key in required_keys:
                if key not in args:
                    print(f"Missing required argument: {key}")
                    return

            if cmd == "insert_user":
                role = args.get("role", "admin")
                username = args.get("username", "admin")
                

                user = User(
                    id=0,
                    user_name=username,
                    user_password="password123",
                    user_role=role,
                    join_date=datetime.now(),
                    email=f"{username}@example.com",
                    is_banned=False,
                    nickname=username,
                    user_profile=uuid4(),
                    user_banner=uuid4(),
                    is_active=True,
                    allow_nsfw=True,
                    allow_dm=False,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )

                uid = await insert_user(db, user)
                print(f"User inserted with ID {uid}")
     ```

2. **Integração no Main**:  
   Adicionar em `app/main.py`:

     ```python
        # inside ofsetup_completer():
        **user_endpoints.COMMANDS,
        # inside of repl():
        await db_user_endpoints.handle_command(db, parts)
     ```

## Boas Práticas

- Sempre usar type hints.
- Manter consistência entre nomes de tabelas, models e interfaces.
- Documentar todas as funções com docstrings.
- Implementar testes unitários para cada camada.
- testar com o comando `poetry run mypy .` para buscar por erros de tipagem antes de fazer pull request.
