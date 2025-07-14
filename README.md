# 🏁 Formula 1 Insights Dashboard

A full-stack web application that parses, stores, and visualizes Formula 1 timing and standings data. Built using:

## 📦 Tech Stack

| Layer      | Technology                                  |
|------------|---------------------------------------------|
| Frontend   | React + TypeScript (Vite)                   |
| Backend    | FastAPI (Python 3.11)                       |
| ORM        | SQLAlchemy                                  |
| Database   | PostgreSQL 15                               |
| Testing    | `pytest`, `httpx`, `pytest-asyncio`, `jest` |
| Containerization | Docker + Docker Compose                     |
| Schema     | Pydantic                                    |

---

## 🧠 How It Works (Technical Overview)

This project implements a full-stack pipeline that ingests Formula 1 data from static datasets, transforms and validates it, stores it in a relational PostgreSQL database using an Object-Relational Mapping (ORM), exposes this data via a modern REST API using FastAPI, and renders interactive dashboard using a TypeScript-powered React frontend.

### 1. 📁 Dataset Ingestion

Raw data is stored in the `./dataset` directory and includes structured `.csv` files representing various Formula 1 entities such as:

- Drivers
- Circuits
- Races
- Lap times
- Driver standings

These files follow a tabular schema and are ingested using pandas Python package.

---

### 2. ✅ Data Parsing & Validation

Each dataset is:

- Read into memory using `pandas.read_csv()` parsing tool with custom cleaning functions.
- Mapped to Python dataclasses or Pydantic models for schema enforcement.
- Validated against constraints such as nullable fields, data types, and foreign keys (e.g., driver IDs existing in multiple tables).

Optional and nullable fields (e.g., driver number or fastest lap time) are handled using `Optional[...]` in Pydantic.

```python
class DriverBase(BaseModel):
    driver_id: int
    number: Optional[int] = None
    code: Optional[str] = None
```

---

### 3. 🧱 ORM Models & Database Mapping
- Validated data is inserted into a PostgreSQL 15 database using SQLAlchemy ORM.
- Each dataset corresponds to a Python class (Base) with proper data types, constraints, and relationships.
- SQLAlchemy relationship() fields define connections such as:

```
-> One-to-many: Circuit → Races
-> Many-to-one: Race → Driver
-> Many-to-many: Drivers ↔ Results (via foreign keys)
```

Example ORM model:
```python
class Circuit(Base):
    __tablename__ = "circuits"
    circuit_id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)
    country = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    alt = Column(Integer, nullable=True)
```

#### Data insertion uses either:
- Direct session.bulk_save_objects([...])
- Asynchronous ORM (via AsyncSession) for scalable ingestion

---

### 4. 🌐 Backend API
- The backend is built with FastAPI, serving as a lightweight but powerful REST API layer.
- Endpoints are modularized under app/api/routes.py
- Each endpoint connects to the DB via dependency-injected session objects using Depends(get_db_session)
- Pydantic response models (schemas) return structured and validated JSON

Example route:
```python
@router.get("/drivers/summary", response_model=List[DriverSummary])
async def get_driver_summaries(db: AsyncSession = Depends(get_db_session)):
    return await crud.get_driver_summary(db)
```

### Data Flow

                      ┌────────────────────────────┐
                      │      Raw Dataset Files     │
                      │    (CSV in /dataset)       │
                      └─────────────┬──────────────┘
                                    │
                                    ▼
                        ┌─────────────────────────┐
                        │    Python Data Parser   │
                        │       (pandas)          │
                        └───────────┬─────────────┘
                                    │
                                    ▼
                     ┌───────────────────────────────┐
                     │   Pydantic Schema Validation  │
                     │  (Type-safe, structured data) │
                     └──────────────┬────────────────┘
                                    │
                                    ▼
                   ┌───────────────────────────────────┐
                   │ SQLAlchemy ORM (Async Relational) │
                   │ - Define Models                   │
                   │ - Map Relationships               │
                   └────────────────┬──────────────────┘
                                    │
                                    ▼
                      ┌────────────────────────┐
                      │ PostgreSQL Relational  │
                      │        Database        │
                      └─────────────┬──────────┘
                                    │
                          ┌─────────▼─────────┐
                          │ FastAPI Endpoints │
                          │                   │
                          └─────────┬─────────┘
                                    │
                          ┌─────────▼─────────┐
                          │ React + TypeScript│
                          │   Frontend (UI)   │
                          └───────────────────┘

---

### 5. 📊 Frontend Data Fetching & Visualization
- The frontend is built using Vite + React + TypeScript. It performs the following:
- Fetches preprocessed summaries from the backend API using fetch() or axios
- Displays interactive dashboards, such as Circuit and Driver summaries, enabling searching and sorting

---

### 6. 🐳 Dockerized Architecture
The full system is containerized using Docker Compose, orchestrating:
- db: PostgreSQL with healthcheck and persistent volumes
- backend: FastAPI service built from backend/Dockerfile
- frontend: Vite + React app from frontend/Dockerfile
- Each service runs independently and exposes its port:

---

Healthchecks ensure that the backend only starts when the DB is ready.

---

### ⚙️ Assumptions
#### The following assumptions were made in the design and development of this application. These clarify what has been intentionally excluded from the current scope to focus on core functionality and reduce complexity for prototyping or demonstration purposes.
#### 🖥️ Frontend
- The frontend is designed for development use only and is served via a local dev server (e.g., Vite).
- No production-grade frontend configuration (e.g., Nginx, CDN, HTTPS, asset minification, or caching strategy) is included.
- The UI is not optimized for production-level performance, accessibility, or SEO.
#### 🔐 Security & Authentication
- No authentication (e.g., OAuth, JWT, sessions) or authorization controls are implemented.
- The system does not enforce secure communication (e.g., HTTPS).
- Input/output sanitization, CSRF protection, and other security hardening techniques are not comprehensively applied.
#### 🐳 Deployment & Infrastructure
- The project is not production-deployment ready.
- No support is included for orchestration platforms (e.g., Kubernetes, Docker Swarm).
- No CI/CD pipelines or automated deployment infrastructure are configured.
- The application is designed to run in a local or single-instance environment only.
#### 📊 Observability & Operational Concerns
- Logging is minimal and not structured for centralized log aggregation or analysis.
- Monitoring (e.g., Prometheus, Grafana) and alerting systems are not configured.
- Rate limiting and throttling mechanisms are not applied on API endpoints.
- No auditing or request tracing is in place (e.g., for tracking sensitive operations or user activity).
- Error handling and reporting are minimal and not integrated with external systems (e.g., Sentry, ELK stack).
#### 🧪 Testing
- No end-to-end (E2E) or load testing frameworks are integrated.
- There is no automated test pipeline or test coverage reporting.
#### 🧾 Data & API
- Assumes a local PostgreSQL database using test/demo data.
- No persistent storage configuration (e.g., backups, replicas) is provided.
- No API versioning or documentation beyond in-code type definitions or OpenAPI stubs (if any).
- API security mechanisms such as API keys, tokens, or CORS whitelisting are not implemented.

---

## 🚀 Features

### 🧠 Backend API
- REST endpoints to retrieve:
  - **Driver summaries** (total races, podiums)
  - **Circuit summaries** (fastest lap, number of races)
- Asynchronous DB interaction using `SQLAlchemy Async ORM`
- Modular CRUD structure
- Schema validation with `Pydantic`
- Dependency injection with FastAPI's `Depends`

### 🎨 Frontend
- Built using Vite, TypeScript, and React

---

## 🗂️ Project Structure

```plaintext
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── config.py
│   │   ├── crud/
│   │   │   ├── __init__.py
│   │   │   └── crud.py
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── models.py
│   │   │   └── session.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── loader.py
│   │   │   └── schemas.py
│   │   ├── __init__.py
│   │   └── main.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_crud.py
│   │   ├── test_loader.py
│   │   ├── test_main.py
│   │   ├── test_models.py
│   │   ├── test_routes.py
│   │   ├── test_schemas.py
│   │   ├── test_session.py
│   │   └── test_table_creator.py
│   ├── __init__.txt
│   ├── Dockerfile
│   └── requirements.txt
├── dataset/
│   ├── circuits.csv
│   ├── driver_standings.csv
│   ├── drivers.csv
│   ├── lap_times.csv
│   └── races.csv 
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CircuitSummaryCard.test.tsx
│   │   │   ├── CircuitSummaryCard.tsx
│   │   │   ├── DriverSummaryCard.tsx
│   │   │   ├── DriverSummaryCard.test.tsx
│   │   │   └── SummaryCard.module.cvv
│   │   ├── pages/
│   │   │   ├── Dashboard.test.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Home.test.tsx
│   │   │   └── Home.tsx
│   │   ├── services/
│   │   │   └── api.test.ts
│   │   │   └── api.ts
│   │   ├── types/
│   │   │    └── index.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── Dockerfile
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│──.env
│──.gitignore
├── babel.config.js
├── docker-compose.yml
├── jest.config.js
├── jest-css-modules.mock.js
├── package.json
├── pytest.ini
└── README.md
```

---

### 🧱 Branching Strategy

- `main`: stable, review-ready code
- `dev`: in-progress integration branch
- `feature/*`: individual features
- `fix/*`: bug fixes or small corrections
- `docs/*`: documentation
- `test/*`: test

> Merges to `main` only happen when the app is stable and working end-to-end.

---

### 🧬 ORM Structure (SQLAlchemy)

Each table is defined using SQLAlchemy ORM with AsyncSession. Here's a sample of the Driver model:

```python
class Driver(Base):
    __tablename__ = "drivers"
    driver_id = Column(Integer, primary_key=True)
    driver_ref = Column(String)
    number = Column(Integer, nullable=True)
    code = Column(String, nullable=True)
    forename = Column(String)
    surname = Column(String)
    dob = Column(Date)
    nationality = Column(String)
    url = Column(String)
```
    
---

### ⚙️ API Endpoints

>  Method	Endpoint	Description
> - GET	/drivers/summary	Get podiums and race count per driver
> - GET	/circuits/summary	Get fastest lap and race count per circuit

- Response models are returned as Pydantic objects with fields like
```json
[
  {
    "driver_id": 1,
    "forename": "Lewis",
    "surname": "Hamilton",
    "nationality": "British",
    "total_races": 300,
    "podiums": 180
  }
]
```
---

## 🐳 Docker Setup

### 🧱 Backend Dockerfile

- Uses Python 3.11 slim base
- Installs system dependencies for PostgreSQL
- Copies source and .env files

### 🌐 Frontend Dockerfile

- Based on node:20-alpine
- Uses npm install + Vite dev server

---

### 📦 How to Build & Run

1. Clone the repository
```shell
$ git clone https://github.com/aykutgoren/f1-dashboard.git
```
```shell
$ cd formula1-dashboard
```

2. Start the services
```shell
$ docker compose up --build
```

### Access:
- Frontend: http://localhost:5173/dashboard
- Backend API: http://localhost:8000/docs
- DB: PostgreSQL on localhost:5432

---

### 🧪 Testing

#### Backend
- Unit tests for models and schemas
- Integration tests for API routes
- Functional end-to-end testing of key endpoints

#### Frontend
- React jest tests

### ✅ Running Tests
! Make sure all services are up and running before running tests

#### Backend Tests
```shell
$ pip install -r backend/requirements.txt
```
1-) Navigate to the root folder -> f1-dashboard
```shell
$ cd f1-dashboard
```
2-) Run tests using pytest

To run all the tests:
```shell
$ pytest backend/tests
```
To run only unit tests:
```shell
$ pytest -m unit backend/tests
```
To run only integration tests:
```shell
$ pytest -m integration backend/tests
```
For running only functional tests:
```shell
$ pytest -m functional backend/tests
```
#### Frontend Tests

```shell
$ npm install
```
```shell
$ npx jest
```