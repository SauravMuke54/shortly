# shortly

A simple URL shortener API built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.

Send a long URL, get back a short one. Visit the short one, get redirected to the original — with automatic expiry after 12 hours.

## Features

- 🔗 **Shorten URLs** via a simple REST endpoint
- ↪️ **Redirect** short codes to their original URL (HTTP 302)
- ⏳ **Auto-expiry** — links expire 12 hours after creation and return `410 Gone` once expired
- 🔢 **Base62 encoding** of database IDs for short, URL-safe codes
- 🩺 **Health check** endpoint for uptime monitoring
- 🧹 Linted and formatted with [Ruff](https://docs.astral.sh/ruff/), enforced in CI

## Tech Stack

| Layer          | Technology |
| -------------- | ---------- |
| API framework  | [FastAPI](https://fastapi.tiangolo.com/) |
| ORM            | [SQLAlchemy](https://www.sqlalchemy.org/) |
| Database       | PostgreSQL (via [psycopg](https://www.psycopg.org/)) |
| Migrations     | [Alembic](https://alembic.sqlalchemy.org/) |
| Server         | [Uvicorn](https://www.uvicorn.org/) |
| Package/build  | [uv](https://docs.astral.sh/uv/) |
| Linting        | [Ruff](https://docs.astral.sh/ruff/) |

## Project Structure

```
src/shortly/
├── main.py                  # FastAPI app entrypoint
├── api/
│   ├── router.py             # Combines all API routers
│   └── routes/
│       ├── short_url.py      # POST /api/shorten
│       └── redirect.py       # GET /{short_url}
├── core/
│   ├── config.py             # Environment/config loading
│   └── database.py           # SQLAlchemy engine & session
├── models/
│   ├── urls.py                # URL SQLAlchemy model
│   └── requests.py           # Pydantic request schemas
└── utils/
    └── base62.py              # Base62 encode/decode helpers
```

## Getting Started

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- A running PostgreSQL instance

### Installation

```bash
git clone https://github.com/SauravMuke54/shortly.git
cd shortly
uv sync
```

### Configuration

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://<user>:<password>@<host>:<port>/<database>
```

### Run the server

```bash
uv run uvicorn shortly.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, with interactive docs at `http://127.0.0.1:8000/docs`.

## API Reference

### Shorten a URL

```
POST /api/shorten
```

**Request body:**

```json
{
  "url": "https://example.com/some/very/long/path"
}
```

**Response — `201 Created`:**

```json
{
  "short_url": "http://127.0.0.1:8000/b1",
  "expires_at": "2026-08-20T21:00:00Z"
}
```

### Redirect to the original URL

```
GET /{short_url}
```

Redirects (`302`) to the original URL if it exists and hasn't expired.

| Status | Meaning |
| ------ | ------- |
| `302`  | Redirected to the original URL |
| `404`  | Short URL not found |
| `410`  | Short URL has expired |

### Health check

```
GET /health
```

```json
{ "status": "ok" }
```

## Development

Run lint checks:

```bash
uv run ruff check .
uv run ruff format --check .
```

CI (GitHub Actions) runs these same checks on every push and pull request to `main` and `develop`.

## License

No license specified yet — all rights reserved by the author unless stated otherwise.