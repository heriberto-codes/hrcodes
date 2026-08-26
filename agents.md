# Repository Guidelines

## Project Overview

Hroman Codes is a server-rendered Django portfolio and business website for Heriberto Roman and Hroman Codes, LLC. It presents services, experience, projects, blog posts, and contact paths. Preserve the existing brand system and favor small, reviewable changes.

## Project Structure and Module Organization

- `hrcodes/`: Django project configuration, root URLs, and WSGI/ASGI entry points.
- `apps/pages/`: homepage composition and homepage data loading.
- `apps/blog/`: blog models, views, forms, URLs, and admin integration.
- `apps/archive/`: project archive route and view.
- `templates/`: shared layouts, page templates, and reusable include sections.
- `static/`: authored CSS, JavaScript, images, and other source assets.
- `staticfiles/`: generated collection output; do not edit by hand.
- `.github/workflows/`: GitHub Actions deployment automation.
- `.agents/skills/`: Turtle AI workflow skills.
- `docs/system/`: Turtle AI workflow rules and state documentation.

## Build, Test, and Development Commands

- Install dependencies: `venv/bin/pip install -r requirements.txt`
- Validate Django configuration: `DEBUG=True venv/bin/python manage.py check`
- Run locally: `DEBUG=True venv/bin/python manage.py runserver 127.0.0.1:8000`
- Run tests: `DEBUG=True venv/bin/python manage.py test`
- Collect production static assets: `venv/bin/python manage.py collectstatic --noinput`

Do not run production-oriented commands locally without the required environment variables.

## Coding Style and Naming Conventions

- Follow PEP 8 and established Django conventions for Python.
- Use snake_case for new Python modules, Markdown artifacts, plans, and feature files.
- Keep Django apps focused on their existing responsibilities.
- Prefer reusable template includes for homepage sections.
- Reuse CSS variables from `static/style.css` before introducing new colors or typography.
- Preserve existing URL names and template context contracts unless a planned change requires them.
- Do not introduce a new framework or build tool without explicit approval.

## Testing Guidelines

- Put tests in the owning Django app, using `tests.py` or a `tests/` package with `test_*.py` files.
- Cover view status codes, template selection, model behavior, URL routing, and state-changing behavior relevant to the change.
- Run the smallest relevant test set first, then the full Django test suite.
- Treat `manage.py check` as validation, not a substitute for behavioral tests.

## Commit and Pull Request Guidelines

- Use concise, imperative commit subjects that describe one coherent change.
- Keep unrelated formatting, generated files, and feature work out of the same commit.
- Summarize user-visible changes and verification performed in pull requests.

## Configuration and Environment

- Keep secrets in environment variables or `.env`; never commit secret values.
- Production requires `DATABASE_URL`, `SECRET_KEY`, and `SENTRY_DSN`.
- Fly.io deployment also uses repository secrets configured in GitHub Actions.
- Keep `DEBUG=False` in production. Use `DEBUG=True` only for local development and tests.

## Security and Safety

- Preserve CSRF protection, secure-cookie settings, HTTPS redirects, and Django authentication boundaries.
- Validate and authorize state-changing requests.
- Do not expose API keys, credentials, environment files, session data, or database dumps.
- Do not edit generated `staticfiles/`, virtual environments, or migration history unless the task explicitly requires it.
- Do not deploy, migrate production data, or modify infrastructure secrets without explicit user authorization.

## Architecture Safety

- Keep public page rendering in the existing Django view/template boundary.
- Keep blog persistence inside `apps/blog` models and views.
- Treat `hrcodes/settings.py`, root URL routing, deployment files, and migrations as high-impact paths.
- If documentation conflicts with executable code, use the code as the source of truth and update documentation deliberately.

## Turtle AI Workflow

For planned feature implementation, follow the required loop documented in `docs/system/workflow.md` and `docs/system/rules.md`:

`EXECUTE -> VERIFY -> ENGINEER CHECKPOINT -> TEST -> DEBUG if needed -> PLAN STEP UPDATE`

The active step is the first unchecked item in `docs/plans/<feature_slug>_plan.md`. Only `turtle-plan-step-update` may mark a plan step complete.
