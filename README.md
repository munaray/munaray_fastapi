# Munaray FastAPI Project Initialization Module

The `init_project.py` module is a command-line utility to quickly scaffold a new FastAPI project with Docker, Alembic for migrations, SQLAlchemy (asyncio), PostgreSQL, and dotenv for environment management.

## Features

This module will:

-   Create a project directory with organized folders for source code, virtual environment, and configuration files.
-   Set up Docker, Docker Compose, and PostgreSQL integration.
-   Install essential FastAPI dependencies, including `uvicorn`, `alembic`, `asyncpg`, and `python-dotenv`.
-   Generate configuration files such as `.env`, `requirements.txt`, and Docker configurations.
-   Provide an Alembic setup with instructions for initializing database migrations.

## Usage

### Prerequisites

-   Python 3.11
-   Docker
-   Git

### Installation

### 1. Clone the Repository

```bash
git clone https://github.com/munaray/munaray_fastapi.git
cd munaray_fastapi
python3.11 -m venv venv
source venv/bin/activate
```

### 1.1 Install the init_fastapi_project module

```bash
pip install -e .
```

### 1.2 Add this module to path to provide global access

```bash
# For macOS/Linux
export PATH="/path/to/your/python/environment/bin:$PATH"

# For Windows
setx PATH "%PATH%;C:\path\to\your\python\environment\Scripts"

```

### 1.3 Create a New FastAPI Project

```bash
cd /my/new/project/dir
init_fastapi_project

# You will be prompt to enter your project name

# Enter your project name: my-app
# Then wait till your project is created successfully
```

## Project Structure

The project is organized as follows:

```bash
my-app/
│
├── src/
│   ├── app.py
│   ├── db.py
│   ├── main.py
│   ├── settings.py
├── venv/
├── .env
├── .gitignore
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
└── README.md
```

**Note: Once your project is created, follow the generated README.md file in your new project for instructions on setting up Alembic and running the application.**

## Additional Resources

For more details on setting up a FastAPI project with asynchronous SQLAlchemy, Alembic, PostgreSQL, and Docker, refer to this comprehensive guide: [Setup FastAPI Project with Async SQLAlchemy, Alembic, and Docker.](https://berkkaraal.com/blog/2024/09/19/setup-fastapi-project-with-async-sqlalchemy-2-alembic-postgresql-and-docker/)

Enjoy using the Munaray FastAPI Project Template!
