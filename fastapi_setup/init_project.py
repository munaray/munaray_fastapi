import os
import subprocess
from pathlib import Path


def create_file(path, content=""):
    with open(path, "w") as file:
        file.write(content)

def create_fastapi_project():
    project_name = input("Enter the project name: ")
    project_root = Path(project_name)
    src_path = project_root / "src"
    os.makedirs(src_path, exist_ok=True)

    # Create the virtual environment setup commands
    subprocess.run(["python3.11", "-m", "venv", str(project_root / "venv")])

    # Requirements files
    requirements = """
fastapi[standard]
uvicorn
sqlalchemy[asyncio]
asyncpg
python-dotenv
alembic
"""
    create_file(project_root / "requirements.txt", requirements.strip())

    # .env file
    env_content = """
PG_HOST=localhost
PG_PORT=5432
PG_USER=postgres
PG_PASSWORD=postgres
PG_DB=db
SQLALCHEMY_ECHO=true
"""
    create_file(project_root / ".env", env_content.strip())

    # Docker Compose
    docker_compose = """
services:
  postgres:
    image: postgres:16-alpine
    volumes:
      - ./var/db:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=db
  backend:
    build: .
    restart: on-failure
    command: bash -c "alembic upgrade head && python3 -m src.main"
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    env_file: .env
    environment:
      - PG_HOST=postgres
"""
    create_file(project_root / "docker-compose.yaml", docker_compose.strip())

    # Dockerfile
    dockerfile_content = """
FROM python:3.11-bookworm

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

COPY . .
"""
    create_file(project_root / "Dockerfile", dockerfile_content.strip())

    # src/app.py
    app_py = """
from fastapi import APIRouter, FastAPI

app = FastAPI()

v1_router = APIRouter(prefix="/api/v1")

app.include_router(v1_router)
"""
    create_file(src_path / "app.py", app_py.strip())

    # src/main.py
    main_py = """
import uvicorn

if __name__ == "__main__":
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=True)
"""
    create_file(src_path / "main.py", main_py.strip())

    # src/db.py
    db_py = """
import datetime
from typing import AsyncGenerator

from sqlalchemy import DateTime
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

import src.settings as settings

class Base(AsyncAttrs, DeclarativeBase):

    type_annotation_map = {
        datetime.datetime: DateTime(timezone=True),
    }

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    echo=settings.SQLALCHEMY_ECHO,
)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
"""
    create_file(src_path / "db.py", db_py.strip())

    # src/settings.py
    settings_py = """
import os
from dotenv import load_dotenv

load_dotenv()

def get_env_var(key, default=None):
    try:
        return os.environ[key]
    except KeyError:
        if default is None:
            raise ValueError(f"Environment variable {key} is missing")
        return default

PG_HOST = get_env_var("PG_HOST")
PG_PORT = get_env_var("PG_PORT")
PG_USER = get_env_var("PG_USER")
PG_PASSWORD = get_env_var("PG_PASSWORD")
PG_DB = get_env_var("PG_DB")

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
)
SQLALCHEMY_ECHO = get_env_var("SQLALCHEMY_ECHO", "") == "true"
"""
    create_file(src_path / "settings.py", settings_py.strip())

    # README File
    readmefile_content = """
# This FastAPI Project Setup is Generated By munaray_fastapi

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Alembic for Database Migrations

```bash
alembic init -t async alembic
```

Update alembic/env.py for Database URL from Settings

```bash
# ...
from alembic import context
from src import settings

config.set_main_option("sqlalchemy.url", settings.SQLALCHEMY_DATABASE_URL)
# ...
```

Update src/db.py for Naming Conventions in Base Class

```bash
# ...
from sqlalchemy import MetaData

class Base(AsyncAttrs, DeclarativeBase):

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

    type_annotation_map = {
        datetime.datetime: DateTime(timezone=True),
    }
# ...
```

Configure Alembic Metadata and Import Models
In alembic/env.py, add the Base model’s metadata:

```bash
# ...
from src.db import Base

target_metadata = Base.metadata
# ...

```

Start the Database

```bash
docker compose up -d postgres
```

**Note**: If you have postgres locally install on your machine it will be running on port 5432, So it is either you change the port number in the `docker-compose.yml` file or run

```bash
sudo systemctl stop postgresql
```

then start the database with docker.

if you encounter a permission denied error with `var/db` folder run this command to fix it.

```bash
chmod -R 755 var/db
```

Generate the Initial Migration

```bash
docker compose run backend /bin/bash
# Then run this inside the container
alembic revision --autogenerate -m "Initial migration"
```

### 3. Run the Application with Docker Compose

Firstly stop the postgres service

```bash
docker compose down postgres
```

Then start and re-build server and database with Docker Compose

```bash
docker compose up --build -d
```

Watch the logs with

```bash
docker compose logs -f
```

Stop the containers with

```bash
docker compose down
```

Additional Resources
For more details on setting up a FastAPI project with asynchronous SQLAlchemy, Alembic, PostgreSQL, and Docker, refer to this comprehensive guide: [Setup FastAPI Project with Async SQLAlchemy, Alembic, and Docker.](https://berkkaraal.com/blog/2024/09/19/setup-fastapi-project-with-async-sqlalchemy-2-alembic-postgresql-and-docker/)
"""
    create_file(project_root / "README.md", readmefile_content.strip())

    # .gitignore
    gitignore_content = """
# Ignore virtual environment
venv/

# Ignore environment variables
.env
"""
    create_file(project_root / ".gitignore", gitignore_content.strip())

    # .dockerignore
    dockerignore_content = """
# Ignore virtual environment
venv/

# Ignore environment variables
.env
"""
    create_file(project_root / ".dockerignore", dockerignore_content.strip())

    print(f"Project '{project_name}' created successfully!")

# Example usage
if __name__ == "__main__":
    create_fastapi_project()
