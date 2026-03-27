# BESS-Controller
BESS Control Algorithms

Folder Structure


bess-optimization-system/
│
├── app/
│   ├── __init__.py              # FastAPI app setup, CORS, DB session dependency
│   ├── main.py                  # API routes, dependency injection, core endpoints
│   ├── models.py                # SQLAlchemy ORM models for all tables (sources, params, schedule, logs)
│   ├── service.py               # Business logic, loads all runtime parameters from DB, optimization engine
│   ├── database.py              # Database engine + sessionmaker initialization
│   ├── config.py                # Environment config (e.g., DB URL)
│   └── schemas.py               # Pydantic models for API request/response validation
│
├── alembic/                     # Alembic migration environment folder
│   ├── env.py                   # Alembic config with metadata target
│   ├── README                   # Alembic instructions
│   ├── script.py.mako
│   └── versions/                # Migration version scripts with create table & modify commands
│        └── <migration_files>.py
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py              # API endpoint tests
│   ├── test_service.py          # Unit tests for business logic using temporary DB
│   └── test_models.py           # Model integrity tests (optional)
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml            # GitHub Actions CI/CD pipeline definition
│
├── Dockerfile                   # Dockerfile for containerization of the API server
├── docker-compose.yml           # Optional multi-container orchestration (DB + app)
├── requirements.txt             # Python packages dependencies
├── alembic.ini                  # Alembic command line config file
├── README.md                    # Project overview and setup instructions
└── .env                        # Environment variables (not committed to Git)
