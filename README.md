# AI Model Risk Assessment API

An internal REST API built with FastAPI to track AI model risk assessments across business units — recording risk levels, review statuses, and the models under evaluation.

Built as a consolidation project to deepen understanding of FastAPI architecture, router-level authentication, environment-based configuration, and production-grade error handling.

---

## Tech Stack

- **FastAPI** — async REST framework with automatic OpenAPI documentation
- **Pydantic v2** — data validation with field validators and enum constraints
- **pydantic-settings** — environment-based configuration via `.env`
- **Python 3.11+**

---

## Project Structure

```
risk-assessment-FastAPI/
├── routers/
│   └── assessments.py      # CRUD routes with router-level API key authentication
├── dependencies.py         # Settings loading and API key verification dependency
├── models.py               # Pydantic models: Assessment, AssessmentResponse, enums
├── main.py                 # App entry point, router registration, global exception handler
├── .env                    # Environment variables — not committed to version control
├── .gitignore
└── README.md
```

---

## Setup

**1. Clone the repository**
```bash
git clone https://github.com/mohamedashqarcodes/risk-assessment-FastAPI.git
cd risk-assessment-FastAPI
```

**2. Create a virtual environment and install dependencies**
```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn pydantic pydantic-settings python-dotenv
```

**3. Create a `.env` file at the project root**
```
API_KEY=your-secret-key-here
APP_NAME=risk-assessment-api
MAX_RISK=HIGH
```

The `.gitignore` excludes `.env` — never commit credentials.

**4. Run the development server**
```bash
fastapi dev main.py
```

Interactive docs available at `http://127.0.0.1:8000/docs`

---

## API Endpoints

All routes require an `api_key` query parameter matching the value in `.env`.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/assessments/` | Create a new risk assessment |
| `GET` | `/assessments/` | List all assessments |
| `GET` | `/assessments/{id}` | Retrieve a single assessment by ID |
| `PUT` | `/assessments/{id}` | Update an existing assessment |
| `DELETE` | `/assessments/{id}` | Delete an assessment |

---

## Data Model

```python
Assessment:
  model_name: str      # Minimum 3 characters — validated on input
  biz_unit: str        # Business unit responsible for the model
  risk: Risk           # Enum: HIGH | MEDIUM | LOW
  review: Review       # Enum: YES | NO (default: NO)
```

`AssessmentResponse` extends `Assessment` with a server-assigned `id: int`.

---

## Authentication

API key authentication is applied at the router level via a FastAPI dependency injected into every route in `routers/assessments.py`. The key is loaded from `.env` through `pydantic-settings` — no credentials are hardcoded anywhere in the codebase.

An invalid or missing key returns `401 Unauthorized`.

---

## Error Handling

A global exception handler in `main.py` catches all unhandled exceptions and returns a standardised `500` JSON response:

```json
{"message": "internal error logged"}
```

This prevents raw tracebacks from leaking to API consumers while logging the error server-side.

---

## Design Decisions

**Router-level authentication over route-level** — attaching the `verify_api_key` dependency to the router rather than each individual route ensures no endpoint is accidentally left unprotected. Adding a new route to the router inherits authentication by default.

**Environment-based configuration via pydantic-settings** — `Settings` reads from `.env` at startup and validates that required fields are present. A missing variable raises an explicit error at startup rather than failing silently at runtime when a route is first called.

**`field_validator` on `model_name`** — strips whitespace and enforces a minimum length of 3 characters at the Pydantic validation layer before any route logic executes, keeping validation concerns out of route handlers.

**In-memory storage** — assessments are stored in a Python list for simplicity. Production deployment would replace this with a persistent database (SQLite for single-instance, PostgreSQL for multi-instance).

---

## What Was Practiced

- FastAPI router architecture and dependency injection
- Environment-based secrets management with pydantic-settings
- Pydantic v2 field validators and enum constraints
- Router-level authentication as a security pattern
- Global exception handling for production-grade error responses
- Deliberate edge-case testing: invalid API keys, missing fields, malformed input

---

## Next Steps

- Persist assessments to a database (SQLAlchemy + SQLite or PostgreSQL)
- Add pagination to the list endpoint
- Implement role-based access — separate read and write permissions
- Add pytest unit tests for each route and the validation logic
- Containerise with Docker for consistent deployment
