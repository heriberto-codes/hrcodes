# Repository Navigation Map

## Top-Level

- `manage.py`: Django CLI entry point.
- `requirements.txt`: pinned Python dependencies.
- `README.md`: project overview and contributor entry point.
- `Dockerfile`: production container build and Gunicorn command.
- `fly.toml`: Fly.io application, release migration, runtime, and static configuration.
- `runtime.txt`: legacy Python runtime declaration.
- `agents.md`: repository rules and Turtle AI constraints.
- `architecture.md`: current system blueprint.
- `repo_map.md`: this navigation map.

## Client

- `templates/base.html`: primary site layout.
- `templates/home.html`: homepage section composition.
- `templates/includes/`: navigation, hero, about, experience, tools, work, blog preview, contact, and footer fragments.
- `templates/blog/`: blog index, category, detail, and blog-specific base.
- `templates/archive/`: archive page and archive-specific base.
- `static/style.css`: global design tokens and main site styling.
- `static/blog/blog.css`: blog-specific styling.
- `static/archive/archive.css`: archive-specific styling.
- `static/pages/`, `static/images/`, and `static/favicon.ico`: authored visual assets.

## Server

- `hrcodes/settings.py`: installed apps, middleware, templates, databases, static/media files, Sentry, and security configuration.
- `hrcodes/urls.py`: root URL composition, admin, archive, blog, and Sentry debug route.
- `hrcodes/wsgi.py`: production WSGI entry point.
- `hrcodes/asgi.py`: ASGI entry point.
- `hrcodes/views.py`: custom error views.
- `apps/pages/views.py`: homepage view and recent-post context.
- `apps/pages/urls.py`: homepage URL.
- `apps/blog/views.py`: blog listing, category, detail, and like behavior.
- `apps/blog/urls.py`: blog routes.
- `apps/blog/forms.py`: blog comment form definition.
- `apps/archive/views.py`: archive template view.
- `apps/archive/urls.py`: archive route.

## Data

- `apps/blog/models.py`: `Category`, `Post`, and `Like` models.
- `apps/blog/migrations/`: blog schema history.
- `apps/pages/migrations/` and `apps/archive/migrations/`: app migration packages.
- `db.sqlite3`: ignored local development database.

## Build Output and Deployment

- `staticfiles/`: generated `collectstatic` output; do not edit.
- `.github/workflows/fly-deploy.yml`: deployment workflow for pushes to `main`.
- `Dockerfile`: dependency installation, static collection, and runtime image.
- `fly.toml`: Fly.io service and release settings.

## Documentation and Turtle AI

- `.agents/skills/turtle-*/SKILL.md`: repository-scoped Turtle AI commands.
- `docs/system/workflow.md`: full workflow stages and command order.
- `docs/system/rules.md`: global gating and state-transition rules.
- `docs/system/state.md`: plan-file state model.
- `docs/backlog.md`: feature backlog when created by `turtle-backlog`.
- `docs/plans/`: per-feature implementation plans when created by `turtle-plan`.
- `docs/features/`: completed feature records when created by `turtle-document`.
- `docs/analysis/repo_analysis.md`: optional deeper repository analysis.

## Protected Paths

- `.env`: secrets and local environment configuration.
- `db.sqlite3`: local database contents.
- `venv/`, `bin/`, `lib/`, `pyvenv.cfg`: local virtual environment.
- `staticfiles/`: generated build output.
- `apps/*/migrations/`: migration history; change only for an explicit schema task.
- `.git/`: repository metadata.
- `fly.toml`, `Dockerfile`, `.github/workflows/`, and `hrcodes/settings.py`: high-impact deployment and configuration paths.

## Notes

- The repository contains a virtual environment split across `venv/` and top-level environment paths; do not treat those files as application source.
- Source static assets live in `static/`; production output is collected into `staticfiles/`.
- Public URLs are HTML-first. There is no public API layer.
