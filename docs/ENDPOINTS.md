# Documentação da API RESTful - Rede Social de Mangás

## 📋 Visão Geral

API RESTful para uma rede social onde usuários gerenciam conteúdo de mangás e moderadores revisam através de sistema de reports.

**Base URL**: `/api/v1`

---

## 🔐 Autenticação

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| `POST` | `/auth/login` | Login de usuário | Pública |
| `POST` | `/auth/register` | Registro de novo usuário | Pública |
| `GET` | `/auth/me` | Obter perfil do usuário logado | Privada |
| `PUT` | `/auth/me` | Atualizar perfil do usuário logado | Privada |

---

## 👥 Usuários

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| `GET` | `/users` | Listar usuários (filtros e paginação) | Privada |
| `GET` | `/users/:id` | Obter perfil de um usuário | Pública |
| `GET` | `/users/:id/following` | Listar quem o usuário segue | Pública |
| `GET` | `/users/:id/followers` | Listar seguidores do usuário | Pública |
| `POST` | `/users/:id/follow` | Seguir um usuário | Privada |
| `DELETE` | `/users/:id/follow` | Deixar de seguir um usuário | Privada |
| `POST` | `/users/:id/block` | Bloquear um usuário | Privada |
| `GET` | `/users/:id/reviews` | Obter reviews de um usuário | Pública |

---

## 📚 Mangás

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| `GET` | `/mangas` | Listar mangás (filtros e paginação) | Pública |
| `POST` | `/mangas` | Adicionar novo mangá | Privada |
| `GET` | `/mangas/:id` | Obter detalhes de um mangá | Pública |
| `PUT` | `/mangas/:id` | Atualizar mangá | Privada (Criador/Mod) |
| `DELETE` | `/mangas/:id` | Excluir mangá | Privada (Criador/Mod) |
| `GET` | `/mangas/:id/staff` | Obter staff de um mangá | Pública |
| `POST` | `/mangas/:id/staff` | Adicionar staff ao mangá | Privada |
| `GET` | `/mangas/:id/chapters` | Listar capítulos de um mangá | Pública |
| `GET` | `/mangas/:id/discussions` | Listar discussões sobre o mangá | Pública |
| `GET` | `/mangas/:id/external-links` | Listar links externos do mangá | Pública |
| `POST` | `/mangas/:id/external-links` | Adicionar link externo ao mangá | Privada |
| `POST` | `/mangas/:id/tags` | Adicionar tag ao mangá | Privada |
| `DELETE` | `/mangas/:id/tags/:tagId` | Remover tag do mangá | Privada |

---

## 📖 Capítulos

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| `GET` | `/chapters` | Listar capítulos (filtros e paginação) | Pública |
| `POST` | `/mangas/:id/chapters` | Adicionar capítulo a um mangá | Privada |
| `GET` | `/chapters/:id` | Obter detalhes de um capítulo | Pública |
| `PUT` | `/chapters/:id` | Atualizar capítulo | Privada (Criador/Mod) |
| `DELETE` | `/chapters/:id` | Excluir capítulo | Privada (Criador/Mod) |
| `GET` | `/chapters/:id/discussions` | Listar discussões sobre o capítulo | Pública |
| `POST` | `/chapters/:id/tags` | Adicionar tag ao capítulo | Privada |
| `DELETE` | `/chapters/:id/tags/:tagId` | Remover tag do capítulo | Privada |

---

## 💬 Discussões

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| `GET` | `/discussions` | Listar discussões (filtros e paginação) | Pública |
| `POST` | `/discussions` | Criar nova discussão | Privada |
| `GET` | `/discussions/:id` | Obter discussão e seus comentários | Pública |
| `PUT` | `/discussions/:id` | Atualizar discussão | Privada (Criador/Mod) |
| `DELETE` | `/discussions/:id` | Excluir discussão | Privada (Criador/Mod) |
| `POST` | `/discussions/:id/vote` | Votar em uma discussão (+1/-1) | Privada |
| `DELETE` | `/discussions/:id/vote` | Remover voto de uma discussão | Privada |
| `POST` | `/discussions/:id/tags` | Adicionar tag à discussão | Privada |
| `DELETE` | `/discussions/:id/tags/:tagId` | Remover tag da discussão | Privada |
| `POST` | `/discussions/:id/read` | Marcar discussão como lida | Privada |

---

## 💭 Comentários

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| `GET` | `/discussions/:id/comments` | Listar comentários de uma discussão | Pública |
| `POST` | `/discussions/:id/comments` | Adicionar comentário a uma discussão | Privada |
| `GET` | `/comments/:id` | Obter comentário específico | Pública |
| `PUT` | `/comments/:id` | Atualizar comentário | Privada (Criador/Mod) |
| `DELETE` | `/comments/:id` | Excluir comentário | Privada (Criador/Mod) |
| `POST` | `/comments/:id/vote` | Votar em um comentário (+1/-1) | Privada |
| `DELETE` | `/comments/:id/vote` | Remover voto de um comentário | Privada |
| `POST` | `/comments/:id/reply` | Responder a um comentário | Privada |

---

## ⭐ Reviews/Listas de Leitura

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| `GET` | `/users/me/reviews` | Obter reviews do usuário logado | Privada |
| `POST` | `/users/me/reviews` | Adicionar/atualizar review de mangá | Privada |
| `DELETE` | `/users/me/reviews/:mangaId` | Remover review de mangá | Privada |
| `GET` | `/users/me/chapter-progress` | Obter progresso de capítulos | Privada |
| `POST` | `/users/me/chapter-progress` | Atualizar progresso de capítulo | Privada |

---

## 🏷️ Tags

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| `GET` | `/tags` | Listar todas as tags (com busca) | Pública |
| `POST` | `/tags` | Criar nova tag | Privada (Moderadores) |
| `GET` | `/tags/:id` | Obter detalhes de uma tag | Pública |
| `GET` | `/tags/:id/mangas` | Listar mangás com esta tag | Pública |
| `GET` | `/tags/:id/discussions` | Listar discussões com esta tag | Pública |

---

## 👥 Grupos

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| `GET` | `/groups` | Listar grupos (filtros e paginação) | Pública |
| `POST` | `/groups` | Criar grupo | Privada |
| `GET` | `/groups/:id` | Obter detalhes de um grupo | Pública |
| `PUT` | `/groups/:id` | Atualizar grupo | Privada (Dono/Mod) |
| `DELETE` | `/groups/:id` | Excluir grupo | Privada (Dono/Mod) |
| `GET` | `/groups/:id/members` | Listar membros do grupo | Pública |
| `POST` | `/groups/:id/join` | Entrar em um grupo | Privada |
| `DELETE` | `/groups/:id/leave` | Sair de um grupo | Privada |
| `POST` | `/groups/:id/promote` | Promover membro a moderador | Privada (Dono) |
| `POST` | `/groups/:id/demote` | Rebaixar moderador a membro | Privada (Dono) |
| `GET` | `/groups/:id/discussions` | Listar discussões do grupo | Pública |

---

## 🎬 Staff

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| `GET` | `/staff` | Listar perfis de staff | Pública |
| `POST` | `/staff` | Criar perfil de staff | Privada |
| `GET` | `/staff/:id` | Obter detalhes de staff | Pública |
| `PUT` | `/staff/:id` | Atualizar perfil de staff | Privada |
| `GET` | `/staff/:id/mangas` | Listar mangás do staff | Pública |

---

## ⚖️ Moderação/Reports

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| `GET` | `/moderation/reports` | Listar reports | Privada (Moderadores) |
| `POST` | `/moderation/reports` | Criar report | Privada |
| `GET` | `/moderation/reports/:id` | Obter detalhes de report | Privada (Moderadores) |
| `PUT` | `/moderation/reports/:id` | Atualizar status do report | Privada (Moderadores) |
| `GET` | `/moderation/stats` | Estatísticas de moderação | Privada (Moderadores) |

---

## 🔔 Notificações

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| `GET` | `/notifications` | Listar notificações do usuário logado | Privada |
| `PUT` | `/notifications/:id/read` | Marcar notificação como lida | Privada |
| `PUT` | `/notifications/read-all` | Marcar todas como lidas | Privada |

---

## 📝 Exemplos de Requisições

### Adicionar Mangá

```http
POST /api/v1/mangas
Authorization: Bearer <token>
Content-Type: application/json

{
  "title_english": "One Piece",
  "title_native": "ワンピース",
  "release_date": "1997-07-22",
  "comic_type": "manga",
  "cover_url": "https://example.com/cover.jpg"
}
```

### Criar Report

```http
POST /api/v1/moderation/reports
Authorization: Bearer <token>
Content-Type: application/json

{
  "target_type": "manga",
  "target_id": "uuid-do-manga",
  "reason": "Conteúdo duplicado"
}
```

---

## 🛡️ Códigos de Status

| Código | Descrição |
|--------|-----------|
| `200` | OK - Sucesso |
| `201` | Created - Recurso criado |
| `400` | Bad Request - Dados inválidos |
| `401` | Unauthorized - Não autenticado |
| `403` | Forbidden - Sem permissão |
| `404` | Not Found - Recurso não encontrado |
| `500` | Internal Server Error - Erro no servidor |

---

## 📦 Respostas Padronizadas

### Sucesso

```json
{
  "success": true,
  "data": {...},
  "pagination": {...}
}
```

### Erro

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Mensagem de erro descritiva"
  }
}
```

### Pagination

```json
{
  "pagination": {
    "current_page": 3,
    "total_items": 1530,
    "per_page": 20
  }
}

{
  "pagination": {
    "next_cursor": "abc123...",
    "has_more": true,
    "limit": 20
  }
}
```

---

Este documento fornece uma visão completa da API RESTful para sua rede social de mangás, seguindo as melhores práticas e patterns RESTful.
