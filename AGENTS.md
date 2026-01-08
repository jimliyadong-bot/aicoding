# Repository Guidelines

## Project Structure & Module Organization
This repo contains three apps and shared docs.

- `server/`: FastAPI backend (API routes in `server/app/api`, models in `server/app/models`, schemas in `server/app/schemas`, services in `server/app/services`).
- `admin-web/`: Vue 3 + Vite admin UI (`admin-web/src` for pages/components, `admin-web/src/api` for API clients).
- `miniprogram/`: WeChat miniprogram client (pages under `miniprogram/pages`, API helpers in `miniprogram/api`).
- `docs/` and `deploy/`: architecture/deployment notes and Docker/nginx config.

## Build, Test, and Development Commands
Backend (from `server/`):
- `python -m venv venv` and `pip install -r requirements.txt` to set up dependencies.
- `copy .env.example .env` then update DB/Redis settings.
- `alembic upgrade head` to apply migrations.
- `python -m app.main` or `uvicorn app.main:app --reload` to run the API.

Admin web (from `admin-web/`):
- `npm install` to install dependencies.
- `npm run dev` for local dev, `npm run build` for production build, `npm run preview` for a local preview.

Root helpers:
- `docker-compose up -d` to start MySQL/Redis/API containers.
- `start-all.ps1`, `stop-all.ps1`, `check-status.ps1` for Windows local orchestration.

## Coding Style & Naming Conventions
- Python: 4-space indentation, snake_case for modules and functions.
- Vue/JS: follow existing SFC style in `admin-web/src` (2-space indentation in templates/styles, ES modules in scripts).
- Keep domain code in `server/app/services` and wire endpoints via `server/app/api/v1`.

## Testing Guidelines
- No full automated test suite is present.
- Use `server/scripts/test_audit_and_security.sh` for audit/security checks (requires `ADMIN_USERNAME`, `ADMIN_PASSWORD`, `TEST_USER_PASSWORD`).
- If you add tests, place them under `server/tests` and use `test_*.py` naming.

## Commit & Pull Request Guidelines
- Commit messages use a short type prefix (example: `docs: update README`).
- PRs should include: a brief summary, linked issue (if any), testing steps run, and screenshots for UI changes.
- Call out schema, env, or migration changes explicitly.

## Security & Configuration Tips
- Never commit secrets. Use `server/.env.example` and `admin-web/.env.development` as templates.
- Set `VITE_API_BASE_URL` for the admin UI and `apiBaseUrl` in `miniprogram/app.js` for the mini program.

## Agent-Specific Instructions
If you are using automation, follow the workflow notes in `CodeX.md`.