# Controle de Implementação do Banco de Dados

## Tabelas Principais

| Tabela                        | Status    | Responsável | Observações                     |
|-------------------------------|-----------|-------------|---------------------------------|
| `users`                       |     🟡    |   CAMELO    | Depende de `countries`          |
| `mangas`                      |     🟡    |   CAMELO    | Depende de `countries`          |
| `chapters`                    |     🟡    |   CAMELO    | Depende de `countires`          |
| `pages`                       |     🟢    |   CAMELO    |                                 |
| `tags`                        |     🟢    |   LEME      |                                 |
| `countries`                   |     ⚪    |             |                                 |

## Tabelas de Relacionamento

| Tabela                        | Status    | Responsável | Observações                     |
|-------------------------------|-----------|-------------|---------------------------------|
| `read (users_mangas)`         |     ⚪    |             |                                 |
| `reviews`                     |     ⚪    |             |                                 |
| `users_reviews`               |     ⚪    |             |                                 |
| `chapters_reviews`            |     ⚪    |             |                                 |
| `mangas_reviews`              |     ⚪    |             |                                 |
| `pages_reviews`               |     ⚪    |             |                                 |
| `related (mangas_mangas)`     |     ⚪    |             |                                 |
| `genre (mangas_tags)`         |     ⚪    |             |                                 |
| `localized (mangas_countries)`|     ⚪    |             |                                 |

## Legenda de Status

- 🟢 Concluído
- 🟡 Em andamento
- 🔴 Não iniciado
- ⚪ Não atribuído

## Checklist de Implementação

Para cada tabela, seguir instruções em [Próximos Passos](./NEXTSTEPS.md)
