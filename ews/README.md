# EWS (External Web Service)

---

The ```ews``` represents an external webapp service for the posts project.

## Project Structure
```
/
├── modules                     # The name of the module
├── ews                         # An external web-service
│    ├── api                    # The API of the client
│    │    ├── accounts          # accounts APIs
│    │    ├── comments          # comments APIs
│    │    ├── posts             # posts APIs
│    │    ├── v1                # v1 blueprints/endpoints
│    │    └── __init__.py       # The package initializer
│    ├── static                 # The static contents like css, js etc.
│    │    ├── css               # css files
│    │    ├── images            # image files
│    │    ├── js                # JavaScript files
│    │    └── __init__.py       # The package initializer
│    ├── templates              # The web templates like fragments, html pages etc.
│    │    ├── views             # The HTML views/pages
│    │    └── __init__.py       # The package initializer
│    ├── .env                   # The .env file
│    ├── __init__.py            # The package initializer
│    ├── default.env            # The default .env file
│    ├── README.md              # Instructions and helpful links
│    ├── requirements.txt       # The webapp's dependencies/packages
│    └── wsgi.py                # the WSGI app
├── iws                         # An internal web-service
├── README.md                   # Instructions and helpful links
└── robots.txt                  # tells which URLs the search engine crawlers can access on your site
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

- Install Flask

**Note**: - Only if you didn't install the 'requirements.txt' file.

```shell
python3 -m pip install Flask
```


### Configuration Setup

Create or update local .env configuration file.

```shell
cp ./ews/default.env .env
OR
touch .env

# Local Variables
HOST = 127.0.0.1
PORT = 8080
DEBUG = True
DEFAULT_POOL_SIZE = 1
RDS_POOL_SIZE = 1
```


### Run EWS Flask Application

**By default**, Flask runs the application on **port 5000**.


```shell
python wsgi.py

OR

python -m flask --app wsgi run --port 8080 --debug
# http://127.0.0.1:8080/posts

OR

flask --app wsgi run
python -m flask --app wsgi run
# http://127.0.0.1:5000/posts
```

**Note**:- You can stop the development server by pressing ```Ctrl+C``` in your terminal.

### Access Flask Application
- [EWS on port 8080](http://127.0.0.1:8080/posts)
- [EWS on port 5000](http://127.0.0.1:5000/posts)


### Build Project
```shell
python3 -m build
```

### Save Requirements (Dependencies)
```shell
pip freeze > requirements.txt
```


## Unit Tests
```shell
python3 -m unittest
python -m unittest discover -s ./tests -p "test_*.py"
```

# Reference

- [Gunicorn - WSGI server](https://docs.gunicorn.org/en/latest/index.html)
- [Python Packaging User Guide](https://packaging.python.org/en/latest/)

# Author
- Rohtash Lakra
