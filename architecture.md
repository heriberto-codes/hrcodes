# System Architecture

## Overview

Hroman Codes is a public portfolio, services, and content website for Heriberto Roman and Hroman Codes, LLC. Visitors can review services, experience, projects, and blog content, then contact the business through external links. Django administrators manage blog data.

## Project Structure

- `manage.py`: Django command entry point.
- `hrcodes/settings.py`: environment, applications, middleware, database, static files, and security settings.
- `hrcodes/urls.py`: root route composition and admin route.
- `apps/pages/`: homepage view and URL.
- `apps/blog/`: blog persistence and public blog behavior.
- `apps/archive/`: standalone project archive page.
- `templates/`: Django layouts and page fragments.
- `static/`: authored frontend assets.
- `Dockerfile`, `fly.toml`, `.github/workflows/fly-deploy.yml`: production build and deployment path.

## System Boundaries

Inside the repository:

- Django request routing and server-rendered HTML.
- Blog categories, posts, and like counts.
- Site templates, styling, images, and frontend behavior.
- Container and Fly.io deployment configuration.

Outside the repository:

- PostgreSQL in production.
- Fly.io application hosting.
- GitHub Actions continuous deployment.
- Sentry error monitoring.
- External S3-hosted documents linked by the UI.
- Calendly, YouTube, GitHub, LinkedIn, Figma, and other outbound destinations.

## High-Level System Diagram

```text
Browser
  -> Fly.io / Gunicorn
    -> Django URL router
      -> pages, blog, or archive view
        -> Django templates + static assets
        -> ORM -> SQLite (local) / PostgreSQL (production)

GitHub main branch
  -> GitHub Actions
    -> flyctl deploy
      -> Docker image -> Fly.io

Django runtime -> Sentry
```

## Architectural Principles

- Prefer server-rendered Django pages and existing template includes.
- Keep app responsibilities separated by `pages`, `blog`, and `archive`.
- Reuse the established CSS tokens and Bootstrap-based responsive structure.
- Keep changes small, observable, and reversible.
- Preserve environment-driven production configuration.

## Constraints and Non-Goals

- This is not a single-page application and has no public JSON API.
- There is no background-task system, service layer, or separate frontend build pipeline.
- Do not introduce those patterns without a demonstrated requirement and explicit approval.
- Generated `staticfiles/` output is not an authored source boundary.

## Runtime Components

- Django 5.1.2 application.
- Gunicorn WSGI server in production.
- WhiteNoise for static-file delivery.
- Django ORM with SQLite locally and environment-configured PostgreSQL in production.
- CKEditor 4 integration for rich blog content.
- Sentry SDK for runtime error reporting.

## Request Flow

1. A browser request reaches Fly.io and Gunicorn in production, or Django's development server locally.
2. `hrcodes/urls.py` routes the request to `pages`, `blog`, `archive`, or Django admin.
3. The selected view reads ORM data when needed and builds template context.
4. Django renders a template from `templates/`.
5. CSS, JavaScript, and image requests are served from the static path.

## Data Flow

- The homepage reads the two newest `Post` records.
- Blog index and category pages query ordered `Post` collections.
- Blog detail reads a `Post` and its associated `Like` record.
- A session stores which posts a visitor has liked; the aggregate count persists in the database.

## Data Layer

- Local development: SQLite database at `db.sqlite3`.
- Production: database URL supplied through `DATABASE_URL`, normally PostgreSQL.
- Schema changes are owned by Django migrations inside each app.

## Database Schema (High Level)

- `Category`: name and slug; many-to-many relationship with posts.
- `Post`: title, slug, optional image, rich body, snippet, timestamps, categories, and publication status.
- `Like`: foreign key to a post and an aggregate positive count.

## Client Architecture

- Django templates compose the HTML response.
- `templates/base.html` provides the main layout.
- `templates/home.html` composes reusable sections from `templates/includes/`.
- Bootstrap, custom CSS, icon libraries, and lightweight JavaScript provide responsive presentation and interaction.
- Desktop and mobile variants exist for some content-heavy sections.

## Server Architecture

- `HomePageView` is a class-based template view that adds recent posts.
- Blog behavior uses function-based views and Django ORM queries.
- The archive is a class-based template view.
- Django admin is the content-management surface.

## API Structure

No public JSON API is currently implemented. Public behavior is HTML route based.

## Authentication

Django's built-in authentication supports the admin route. Public pages do not require authentication.

## Authorization

Admin access relies on Django's staff and permission model. Public content and like behavior are available without a user account.

## Security Model

- Secrets and database configuration come from environment variables.
- Production redirects HTTP to HTTPS and enables secure session and CSRF cookies.
- Django CSRF and clickjacking middleware remain enabled.
- The Fly.io proxy header is trusted for HTTPS detection.
- State-changing endpoints must use appropriate HTTP methods, CSRF protection, validation, and abuse controls.

## Background Tasks

No background worker or task queue exists.

## Performance Considerations

- Keep ORM queries bounded and avoid per-item query loops.
- Preserve static compression and hashed manifests in production.
- Optimize large images and animations before adding them to public pages.
- Treat embedded third-party media as a potential page-weight and privacy cost.

## Observability and Operations

- Sentry receives application errors through `SENTRY_DSN`.
- Fly.io provides application runtime and deployment logs.
- GitHub Actions reports deployment pipeline status.

## Build and Run

- Install: `venv/bin/pip install -r requirements.txt`
- Validate: `DEBUG=True venv/bin/python manage.py check`
- Test: `DEBUG=True venv/bin/python manage.py test`
- Develop: `DEBUG=True venv/bin/python manage.py runserver 127.0.0.1:8000`
- Production: Gunicorn starts `hrcodes.wsgi` on port 8000.

## Environment Configuration

- Required production variables: `DATABASE_URL`, `SECRET_KEY`, and `SENTRY_DSN`.
- Deployment automation also references AWS credential variables and `FLY_API_TOKEN`.
- Local `DEBUG=True` switches the database to SQLite and disables production HTTPS enforcement.

## Deployment

Pushes to `main` trigger `.github/workflows/fly-deploy.yml`. The workflow installs dependencies, collects static assets, and runs `flyctl deploy --remote-only`. Fly.io builds the Docker image and runs database migrations as its release command.

## Key Dependencies

- Django, Gunicorn, WhiteNoise, psycopg/psycopg2, django-environ, dj-database-url.
- django-ckeditor for rich blog content.
- sentry-sdk for monitoring.
- django-storages and boto3 are installed for storage integration, although current static-file delivery uses WhiteNoise.

## Known Risks

- CKEditor 4 is unsupported upstream and emits a Django security warning.
- The like action currently changes state through a GET route.
- The public `sentry-debug/` route intentionally raises an exception.
- Static and media URL patterns are repeated across URL modules.
- `runtime.txt` targets Python 3.10.5 while the Dockerfile defaults to Python 3.13.
- The Dockerfile contains duplicate operating-system package installation steps.

## Extension Points

- New public sections belong in `templates/includes/` and the homepage composition.
- New content domains should be isolated in their own Django app when they require models, routes, and administration.
- New integrations should remain environment-configured and wrapped at a clear boundary.

## Open Questions

- Whether blog publication status should filter public queries.
- Whether legacy Heroku and S3 configuration can be removed.
- Whether the experience and project content should become database-managed.
- Whether the like endpoint should be converted to POST with stronger abuse protection.

## Glossary / Acronyms

- ORM: Object-Relational Mapper.
- WSGI: Web Server Gateway Interface.
- CDN: Content Delivery Network.
