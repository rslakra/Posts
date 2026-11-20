# IWS (Internal Web Service)

---

The ```iws``` represents an internal web service for the posts project.

## Project Structure

Although this layout is pretty straightforward, it has several drawbacks that arise as the app complexity increases. 
For example, it will be hard for you to reuse the application logic in other projects because all the functionality is 
bundled in ```webapp/__init__.py```. If you split this functionality into modules instead, then you could reuse complete modules 
across different projects.

```
    /
    ├── ews                             # An external web-service
    ├── iws                             # An internal web-service
    │    ├── account                    # an account’s rest service.
    │    │    ├── v1                    # contains v1 routers/api resources.
    │    │    │    ├── routes           # contains the routes of api resource.
    │    │    ├── v2                    # contains v2 routers/api resources.
    │    │    │    ├── routes           # contains the routes of api resource.
    │    │    ├── __init__.py           # The package initializer
    │    │    ├── models.py             # The model objects
    │    │    ├── README.md             # Instructions and helpful links
    │    │    └── _routes.py            # The package initializer
    │    ├── admin                      # an admin’s rest service.
    │    ├── api                        # The API service
    │    ├── comment                    # The HTML views/pages of accounts
    │    ├── common                     # contains the definition of the common’s models.
    │    ├── framework                  # contains the definition of the framework’s models.
    │    ├── logger                     # The logger module
    │    ├── post                       # contains the definition of the post’s models.
    │    ├── resources                  # contains the definition of the resources’s models.
    │    ├── rest                       # contains the definition of the rest api module.
    │    ├── tests                      # The unit-tests module of an application
    │    ├── webapp                     # contains the definition of the webapp’s module.
    │    │    ├── account               # contains the account’s templates.
    │    │    │    ├── _navbar.html     # contains the reusable fragments of web views.
    │    │    ├── admin                 # contains the admin’s templates.
    │    │    │    ├── _navbar.html     # contains the reusable fragments of web views.
    │    │    ├── comment               # contains the comment’s templates.
    │    │    │    ├── _navbar.html     # contains the reusable fragments of web views.
    │    │    ├── post                  # contains the post’s templates.
    │    │    │    ├── _navbar.html     # contains the reusable fragments of web views.
    │    │    ├── static                # The static contents like css, js etc.
    │    │    │    ├── css              # contains css files
    │    │    │    ├── images           # contains image files
    │    │    │    ├── js               # contains JavaScript files
    │    │    ├── templates             # contains the application’s templates.
    │    │    │    ├── account          # contains the reusable fragments of web views.
    │    │    │    │    ├── _navbar.html    # contains the routes of api resource.
    │    │    │    ├── admin            # contains the reusable fragments of web views.
    │    │    │    │    ├── _navbar.html    # contains the routes of api resource.
    │    │    │    ├── comment          # contains the reusable fragments of web views.
    │    │    │    ├── fragments        # contains the reusable fragments of web views.
    │    │    │    │    ├── _base.html      # base/parent contents of html files
    │    │    │    │    ├── _footer.html    # footer's contents
    │    │    │    │    └── _navigation.py  # navigation menu links
    │    │    │    ├── post             # contains the reusable fragments of web views.
    │    │    │    └── __init__.py      # The package initializer
    │    │    ├── __init__.py           # The package initializer
    │    │    ├── routes.py             # contains the definition of the web’s routes.
    │    ├── __init__.py                # The package initializer
    │    ├── config.py                  # contains the application configuration parameters.
    │    └── README.md                  # The README file of ews module
    ├── README.md                       # Instructions and helpful links
    └── robots.txt                      # tells which URLs the search engine crawlers can access on your site
```

## Local Development

### Check python settings
```shell
python3 --version
python3 -m pip --version
python3 -m ensurepip --default-pip
```

### Setup a virtual environment

```
python3 -m pip install virtualenv
python3 -m venv venv
source deactivate
source venv/bin/activate
```

**Note: -**
```source``` is Linux/Mac-OS command and doesn't work in Windows.

- Windows
```shell
venv\Scripts\activate
```

**Note: -**
The parenthesized (venv) in front of the prompt indicates that you’ve successfully activated the virtual environment.


### Install Requirements (Dependencies)

```
pip install --upgrade pip
python3 -m pip install -r requirements.txt
```


### Configuration Setup

Create or update local .env configuration file.

```shell
cp .env.sample .env
OR
touch .env

#
# App Configs
#
ENV_TYPE = develop
DEBUG = False
HOST = 0.0.0.0
PORT = 8082
#
# Pool Configs
#
DEFAULT_POOL_SIZE = 1
RDS_POOL_SIZE = 1
#
# Logger Configs
#
LOG_FILE_NAME = 'iws.log'
#
# Database Configs
#
# DB_TYPE = SQLAlchemy (SQLite file database) OR MYSQL (see 'make db-up')
DB_TYPE = SQLAlchemy
DB_HOSTNAME = 0.0.0.0
DB_PORT =
DB_NAME = posts
DB_USERNAME = posts
DB_PASSWORD = Password
```

**Note**:- Real environment variables (e.g. `docker run -e DB_TYPE=MYSQL`) take precedence over the `.env` file.


### Run IWS FastAPI Application


```shell
# Command to run the application (reads the port from environment variables)
#CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8082} --workers 4"]

uvicorn main:app --host 0.0.0.0 --port ${PORT:-8082} --reload

OR

uvicorn main:app --reload
# http://0.0.0.0:8082/health-check

# Production Mode (multiple worker processes)
uvicorn main:app --host 0.0.0.0 --port 8080 --workers 2
```

**Note**:- You can stop the development server by pressing ```Ctrl+C``` in your terminal.

### Access FastAPI Application
- [IWS Health Check](http://127.0.0.1:8082/health-check)
- [IWS OpenAPI Docs](http://127.0.0.1:8082/docs)

### Build Project
```shell
python3 -m build
```


### Make Commands (container based)

```shell
make start              # builds the image and starts the FastAPI app container (SQLite, settings of '.env')
make start DB=mysql     # also starts the MySQL container (db-up) and runs the app against it
make stop               # stops and removes the FastAPI app container
make status             # shows the status (state, ports, health) of the DB and app containers

make db-up              # starts the MySQL container (waits until it accepts connections)
make db-down            # stops and removes the MySQL container (the data volume is kept)
```

- The app is available on http://localhost:8080 (docs: http://localhost:8080/docs). Override with `HOST_PORT=<port>`.
- The MySQL container is published on `localhost:3306` (override with `MYSQL_HOST_PORT=<port>`). To run the app locally
  against it, set `DB_TYPE = MYSQL`, `DB_HOSTNAME = 127.0.0.1`, `DB_PORT = 3306`, `DB_NAME = posts`,
  `DB_USERNAME = root` and `DB_PASSWORD = root` in `.env`.
- `make start-fastapi` / `make stop-fastapi` start/stop the app locally with uvicorn (port 8082).

### Database

The database is selected with `DB_TYPE` (`.env` or an environment variable, which takes precedence):
`SQLAlchemy` (SQLite file) or `MYSQL`.

| Run mode | Database | Where the data lives |
|---|---|---|
| Local (`make start-fastapi`, `uvicorn ...`) | SQLite (`DB_TYPE = SQLAlchemy`) | the file `DB_PATH`/`DB_NAME`.db of `.env`, e.g. `~/Downloads/Database/SQLite/Posts.db` |
| Container (`make start`) | SQLite inside the container | `/root/Downloads/Database/SQLite/Posts.db` **inside the container**, nothing is mounted, so the data is lost when the container is removed (`make stop`) |
| Container (`make start DB=mysql`) | MySQL container `mysql-docker` | Docker volume `mysql-docker-data`, mounted at `/var/lib/mysql` in the MySQL container |

**Notes**
- `make start` copies the project's `.env` into the image, so a plain `make start` uses the SQLite settings of `.env`.
  `make start DB=mysql` overrides them with `-e DB_TYPE=MYSQL -e DB_HOSTNAME=mysql-docker -e DB_PORT=3306 -e DB_NAME=posts
  -e DB_USERNAME=root -e DB_PASSWORD=root` (see the `MYSQL_*` variables of the `Makefile`).
- Use an **absolute** `DB_PATH` for SQLite. A relative path (e.g. `data/posts.db`) is currently resolved as `/data/posts.db`.
- The tests use a separate database (`testPosts.db`, from `.env.test`), see [Unit Tests](#unit-tests).

#### Run the app against MySQL

```shell
make start DB=mysql     # starts MySQL (if needed), builds the image and runs the app against MySQL
make status             # both containers should be 'running' and healthy
# after 'make stop', run 'make start DB=mysql' again, a plain 'make start' switches back to SQLite
```

On startup the application creates its tables in the `posts` database. To run the app **locally** against the MySQL
container, set the following in `.env`:

```shell
DB_TYPE = MYSQL
DB_HOSTNAME = 127.0.0.1
DB_PORT = 3306
DB_NAME = posts
DB_USERNAME = root
DB_PASSWORD = root
```

#### MySQL data volume

- The volume `mysql-docker-data` outlives the container: `make db-down` removes the container, but the data is kept and
  is available again after the next `make db-up`.
- On macOS/Windows the volume lives inside Docker Desktop's Linux VM
  (`/var/lib/docker/volumes/mysql-docker-data/_data`), not on the host file system.

```shell
# shows the volume's details (mount point, creation time)
docker volume inspect mysql-docker-data

# browse the files of the volume with a throw-away container
docker run --rm -v mysql-docker-data:/data alpine ls -la /data

# open a MySQL shell / list the tables of the 'posts' database
docker exec -it mysql-docker mysql -uroot -proot posts
docker exec mysql-docker mysql -uroot -proot -e "use posts; show tables;"

# wipe all MySQL data (the container must be removed first)
make db-down
docker volume rm mysql-docker-data
```

To keep the data in a regular folder of the host instead, replace the volume of the `db-up` target in the `Makefile`
with a bind mount, e.g. `-v $(PWD)/mysql-data:/var/lib/mysql`.

### Docker Commands

- Builds the docker container image
```shell
docker build -t posts-iws:latest -f Dockerfile .

OR

docker build -t posts-iws:latest .
```

- Runs the docker container as background service
```shell
docker run --name posts-iws -p 8080:8080 -d posts-iws:latest
OR
docker run --name posts-iws --rm -p 8080:8080 -d posts-iws:latest
```

- Shows the docker container's log
```shell
docker logs -f posts-iws
```

- Executes the 'bash' shell in the container
```shell
docker exec -it posts-iws bash
```

```shell
docker stop posts-iws && docker container rm posts-iws
```


### Save Requirements (Dependencies)
```shell
pip freeze > requirements.txt
```


## Testing


### Unit Tests

The tests must run with `ENV_TYPE=test`, which selects `.env.test` (the test database `testPosts.db`), so they never
touch the development database. Running them without it fails immediately on purpose.

```shell
make test
# OR
./runUnitTests.sh
# OR
ENV_TYPE=test python3 -m unittest
ENV_TYPE=test python -m unittest discover -s ./tests -p "test_*.py"
```

**Note**:- `make test` also runs `pytest` after `unittest`, which is not part of `requirements.txt`.

### Performance Testing
```shell
# Run this in a separate terminal
# so that the load generation continues and you can carry on with the rest of the steps
kubectl run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://php-apache; done"
```


# Reference

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Uvicorn - ASGI server](https://www.uvicorn.org/)
- [Python Packaging User Guide](https://packaging.python.org/en/latest/)
- [The Twelve Factors App](https://12factor.net/)

### Logger Guide
- [Logging HOWTO](https://docs.python.org/3/howto/logging.html)

### Documentation
- [Documentation generator and online help system](https://docs.python.org/3/library/pydoc.html)

### Load Balancing
- [Load Balancing: The Intuition Behind the Power of Two Random Choices](https://medium.com/the-intuition-project/load-balancing-the-intuition-behind-the-power-of-two-random-choices-6de2e139ac2f)
- [Load Balancing](https://go-zero.dev/en/docs/tutorials/service/governance/lb)

### Docker

- [Docker Awesome Compose](https://github.com/docker/awesome-compose)


# Author
- Rohtash Lakra
