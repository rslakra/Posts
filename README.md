# Posts

This repository contains the Posts project: a **Spring Boot backend** (be), an **external web service** (ews), and an **internal web service** (iws).

## Project structure

```
Posts/
├── be/                     # Spring Boot backend (Java 21)
├── ews/                    # External web service (Python/Flask)
├── iws/                    # Internal web service (Python)
├── version.sh              # Shared version for be build/run scripts
├── runEWSApp.sh            # Run EWS app
├── runIWSApp.sh            # Run IWS app
├── .gitignore
├── .pylintrc
├── Makefile
├── LICENSE
└── README.md
```

## Backend (be)

Spring Boot 3.5, Java 21. REST API for users, posts, comments, tags; auth (register/login); H2 or MySQL; Liquibase for schema.

- **Build & run:** From `be/`: `./buildMaven.sh`, `./runMaven.sh` (version from project root `version.sh`)
- **API base:** `http://localhost:8080/api/v1` (e.g. `/auth/register`, `/auth/login`, `/users`, `/posts`)
- **H2 console:** `http://localhost:8080/h2` (when using H2)

See [be/README.md](./be/README.md) for API details, database setup, and project layout.

## Local development (EWS & IWS – Python)

### Check Python settings

```shell
python3 --version
python3 -m pip --version
python3 -m ensurepip --default-pip
```

### Set up a virtual environment

```shell
python3 -m pip install virtualenv
python3 -m venv venv
source venv/bin/activate   # or: source venv/Scripts/activate on Windows
```

### Upgrade pip and install dependencies

```shell
pip install --upgrade pip
pip install -r ews/requirements.txt   # or iws as needed
```

### Configuration

Create or update a local `.env` (e.g. in ews/ or iws/):

```shell
HOST=127.0.0.1
PORT=8080
DEBUG=True
DEFAULT_POOL_SIZE=1
RDS_POOL_SIZE=1
```

By default, Flask runs on port 5000.

### EWS & IWS

- [EWS Application](./ews/README.md)
- [IWS Application](./iws/README.md)

### Build (Python)

```shell
python3 -m build
```

### Save requirements

```shell
pip freeze > requirements.txt
```

### Unit tests

```shell
python -m unittest discover -s ./tests -p "test_*.py"
```

## Enable sudo without password on macOS

**Option 1:** Create `~/password` with your password, then:

```shell
echo password | sudo -S cat /etc/sudoers
```

**Option 2:** Run `sudo visudo`, find the admin group line `%admin ALL = (ALL) ALL`, and change to:

```text
%admin  ALL = (ALL) NOPASSWD:ALL
```

Save and exit.

## Reference

- [Spring Boot](https://spring.io/projects/spring-boot)
- [be/README.md](./be/README.md) – backend API, database, structure
- [Gunicorn – WSGI server](https://docs.gunicorn.org/en/latest/index.html)
- [Python Packaging User Guide](https://packaging.python.org/en/latest/)

## Author

Rohtash Lakra
