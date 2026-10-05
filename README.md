# NovaBite Multi-Agent Restaurant Assistant

NovaBite is a restaurant-focused multi-agent application built with FastAPI, PostgreSQL, MongoDB, and retrieval-augmented generation (RAG) components. It is designed to support restaurant operations such as bookings, user authentication, policy-aware conversations, and AI-powered assistance.

## Features

- FastAPI backend with modular route and service layers
- PostgreSQL for relational data storage
- MongoDB for conversational and document-oriented data
- Alembic-based database migrations
- JWT-based authentication and authorization
- RAG workflow for restaurant menu and policy knowledge
- Multi-agent orchestration for restaurant assistance
- Health and database testing setup

## Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- MongoDB
- LangChain / LangGraph
- FAISS
- Pydantic + Pydantic Settings
- Pytest

## Project Structure

```text
app/
  Agents/
  core/
  database/
  models/
  ORC/
  RAG/
  repositories/
  routes/
  services/
  main.py

test/
  test_database.py
  test_health.py
  test_mongo.py

alembic.ini
pyproject.toml
README.md
```

## Prerequisites

Before running the project, make sure you have:

- Python 3.12
- PostgreSQL installed and running
- MongoDB installed and running
- A valid Groq API key for AI-backed agents

## Local Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Yahya_resturant
```

### 2. Create and activate a virtual environment

With Python venv:

```bash
python -m venv .venv
source .venv/bin/activate
```

Or with Conda:

```bash
conda create -n novabite python=3.12
conda activate novabite
```

### 3. Install dependencies

```bash
pip install -e .
```

For development tools:

```bash
pip install -e ".[dev]"
```

### 4. Configure environment variables

Create a `.env` file in the project root with values like:

```env
APP_NAME=NovaBite
APP_ENV=development
DEBUG=true

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=novabite
POSTGRES_USER=novabite
POSTGRES_PASSWORD=change_me

MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=novabite

JWT_SECRET_KEY=your-super-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

GROQ_API_KEY=YOUR_API_KEY
```

The application reads these values through the settings module in `app/core/config.py`.

## Running the Application

Start the FastAPI server with:

```bash
uvicorn app.main:app --reload
```

The application will be available at:

- http://127.0.0.1:8000
- Health check: http://127.0.0.1:8000/health

## Database Setup

This project uses PostgreSQL and MongoDB. Make sure both services are running before starting the app.

### PostgreSQL

Create a database named `novabite` and ensure the configured user has access.

### MongoDB

The default connection string uses MongoDB at `mongodb://localhost:27017` with database `novabite`.

## Testing

Run the test suite with:

```bash
pytest
```

## Notes

- The RAG and agent files under `app/RAG` and `app/Agents` are part of the AI workflow for menu and policy retrieval.
- The project uses `alembic` for database migrations when needed.
- Production secrets and keys should never be committed to version control.

## License

This project is currently unlicensed unless your team adds a license file and policy.
