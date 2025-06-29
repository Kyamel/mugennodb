# Pull Request Guidelines

To maintain a clean, reviewable, and scalable development workflow, please follow the conventions outlined below.

---

## 📚 Index

- [✅ Commit Guidelines](#-commit-guidelines)
- [🔀 Branch Naming](#-branch-naming)
- [📤 Pull Requests](#-pull-requests)
- [🚫 Avoid](#-avoid)
- [✅ Pre-PR Checklist](#-pre-pr-checklist)

---

## ✅ Commit Guidelines

- Use clear, concise, and **imperative** messages.
- Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

  ```
  <type>(optional scope): <short summary>
  ```

  **Common types**:
  - `feat`: A new feature
  - `fix`: A bug fix
  - `docs`: Documentation only changes
  - `refactor`: Code change that neither fixes a bug nor adds a feature
  - `test`: Adding missing tests or correcting existing tests
  - `chore`: Other changes that don't modify src or test files

### ✅ Examples

```
feat: add support for asyncpg in manga repository
fix(user-api): fix race condition in login endpoint
docs: add pull request guidelines
```

❌ Avoid generic messages like `update`, `fix bug`, or `temp`.

---

## 🔀 Branch Naming

- Branch names should be short and descriptive.
- Use kebab-case and prefix with the purpose:

Examples:
```
feat/add-chapter-model
fix/login-session-bug
refactor/repository-structure
```

---

## 📤 Pull Requests

- Open a PR once your feature or fix is ready or nearly complete.
- Use a **descriptive title** and explain:
  - What the change is
  - Why the change was made
  - How to test or verify it
- Link related issues: `Closes #42`
- Avoid mixing unrelated changes in the same PR.
- Prefer two small PRs over one large one.
- Run all tests and linters before submitting.

---

## 🚫 Avoid

- Massive commits that bundle unrelated changes.
- Branch names like `update`, `feature`, `test`, or `final-version`.
- Opening PRs with no description.
- Ignoring code review comments.

---

## ✅ Pre-PR Checklist

- [ ] Code passes all tests locally?
- [ ] Static typing is valid? (`mypy`)
- [ ] Feature is tested (manual or automated)?
- [ ] Branch is rebased with `main`?
- [ ] PR description explains _why_, not just _what_?
- [ ] Commits follow conventional commit format?

---

Following these guidelines makes reviewing faster, onboarding smoother, and development much more productive for everyone. 🚀