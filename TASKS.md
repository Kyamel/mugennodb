# Controle de Implementação do Banco de Dados

## Tabelas Principais

| Tabela                        | Status    | Responsável | Observações                     |
|-------------------------------|-----------|-------------|---------------------------------|
| `users`                       |     🟡    |   CAMELO    | Depende de `countries`          |
| `mangas`                      |     🟡    |   CAMELO    | Depende de `countries`          |
| `chapters`                    |     🟡    |   CAMELO    | Depende de `countires`          |
| `pages`                       |     🟢    |   CAMELO    |                                 |
| `tags`                        |     🟢    |   LEME      |                                 |
| `countries`                   |     🟢    |   LEME      |                                 |

## Tabelas de Relacionamento

| Tabela                        | Status    | Responsável | Observações                     |
|-------------------------------|-----------|-------------|---------------------------------|
| `read (users_mangas)`         |     🟡    |    EMERSON  |                                 |
| `reviews`                     |     🟡    |    EMERSON  |                                 |
| `chapters_reviews`            |     ⚪    |             |                                 |
| `mangas_reviews`              |     🟡    |    PEDRO    |                                 |
| `pages_reviews`               |     🟡    |    PEDRO    |                                 |
| `related (mangas_mangas)`     |     🟡    |    LEME     |                                 |
| `genre (mangas_tags)`         |     🟡    |    LEME     |                                 |
| `localized (mangas_countries)`|     🟡    |    LEME     |                                 |

## Legenda de Status

- 🟢 Concluído
- 🟡 Em andamento
- 🔴 Não iniciado
- ⚪ Não atribuído

## Checklist de Implementação

Para cada tabela, seguir instruções em [Próximos Passos](./NEXTSTEPS.md)
