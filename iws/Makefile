# Author: Rohtash Lakra
# Signifies our desired python version
# Makefile macros (or variables) are defined a little bit differently than traditional bash, keep in mind that in the Makefile there's top-level Makefile-only syntax, and everything else is bash script syntax.
# PYTHON = python3
# https://gist.github.com/MarkWarneke/2e26d7caef237042e9374ebf564517ad
#
# --------------------------------------------------------------
# Generic Variables
# --------------------------------------------------------------
ROOT_DIR:=${PWD}
# Python Settings
VENV:=venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
REMOVE_FILES:=__pycache__
# Date Settings
TIMESTAMP:=$(date +%s)
DATE_TIMESTAMP:=$(date '+%Y-%m-%d')
# --------------------------------------------------------------
# MODIFY FROM HERE
# --------------------------------------------------------------
# App Static Variables
PROJECT_OWNER=Rohtash
PROJECT_NAME=posts-iws
DOCKER_CONTAINER_NAME=posts-iws
DOCKER_REPOSITORY:=${PROJECT_OWNER}/${PROJECT__NAME}
# --------------------------------------------------------------
# MySQL Settings
# --------------------------------------------------------------
NETWORK_NAME=mysql-network
MYSQL_CONTAINER_NAME=mysql-docker
MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=posts
# --------------------------------------------------------------
# Database Settings
# --------------------------------------------------------------
DATABASE_USERNAME=root
DATABASE_PASSWORD=
DATABASE_NAME=posts

# App Dynamic Variables
ifndef APP_NAME
APP_NAME=posts-iws
endif

ifndef HOST_PORT
HOST_PORT=8080
endif

ifndef CONTAINER_PORT
CONTAINER_PORT=8080
endif

ifndef DOCKER_IMAGE_TAG
DOCKER_IMAGE_TAG=latest
#DOCKER_IMAGE_TAG=$(date +%Y%m%d%H%M%S)
endif

# Variables that depend on git
ifndef GIT_BRANCH
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
endif
#GIT_BRANCH_SLUG=$(subst /,-,$(GIT_BRANCH))

ifndef GIT_BUILD_NUMBER
GIT_BUILD_NUMBER=99999
endif

ifndef GIT_COMMIT
GIT_COMMIT=$(git rev-parse HEAD)
endif
GIT_SHORT_COMMIT=${GIT_COMMIT:0:8}
#
# Makefile configs
#
# .PHONY defines parts of the makefile that are not dependant on any specific file
# This is most often used to store functions
.PHONY: help
# .PHONY: help Makefile

# Defines the default target that `make` will to try to make, or in the case of a phony target, execute the specified
# commands. This target is executed whenever we just type `make`
.DEFAULT_GOAL: help

all: help
#all: setup clean test run doc

# The @ makes sure that the command itself isn't echoed in the terminal
# Put it first so that "make" without argument is like "make help".
# Catch-all target: route all unknown targets
define find.functions
	@# @fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
    @printf "%-25s %s\n" "Target" "Description"
    @printf "%-25s %s\n" "----------------" "----------------"
    @make -pqR : 2>/dev/null \
        | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' \
        | sort \
        | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' \
        | xargs -I _ sh -c 'printf "%-25s " _; make _ -nB | (grep -i "^# Help:" || echo "") | tail -1 | sed "s/^# Help: //g"'
endef

# A hidden target
.hidden:

help:
	@echo
	@echo 'The following commands can be used:'
	@echo
	$(call find.functions)
	@echo

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
#%: Makefile
#	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# This generates the desired project file structure
# A very important thing to note is that macros (or makefile variables) are referenced in the target's code with a single dollar sign ${}, but all script variables are referenced with two dollar signs $${}
# setup:
#     @echo "Checking if project files are generated..."
#     [ -d project_files.project ] || (echo "No directory found, generating..." && mkdir project_files.project)
#     for FILE in ${FILES}; do \
#         touch "project_files.project/$${FILE}.txt"; \
#     done

setup: ## Sets up environment and installs requirements
setup:
	@# Help: Sets up environment and installs requirements
	@echo "Setting up the Python environment ..."
	python3 -m pip install virtualenv
	python3 -m $(VENV) $(VENV)
	#source $(VENV)/bin/activate
	. $(VENV)/bin/activate
	@echo
	$(pwd)
	@echo
	#$(PIP) install --upgrade pip
	$(PIP) install --upgrade pip
	#$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

#
# Clean Commands
#

# In this context, the *.project pattern means "anything that has the .project extension"
clean: ## Remove build and cache files
clean:
	@# Help: Remove build and cache files
	@echo "Cleaning up ..."
	#$(VENV)/bin/deactivate
	#deactivate
	rm -rf $(VENV)
	rm -rf $(REMOVE_FILES) *.project
	find . -name '*.py[co]' -delete
	find . -type f -name '*.py[co]' -delete

#
# Virtual Env Commands
#

venv:
	@# Help: Sets up environment and installs requirements
	@echo "Activating Virtual Environment ..."
	source $(VENV)/bin/activate

#
# Run Commands
#

run: ## Runs the python application
run: venv
	@# Help: Runs the python application
	@echo "Running Python Application ..."
	@$(PYTHON) -m flask --app wsgi run --port 8080 --debug

#
# Test Commands
#

# The ${} notation is specific to the make syntax and is very similar to bash's $()
# This function uses pytest to test our source files
test: ## Tests the python application
test:
	@# Help: Tests the python application
	@echo "Testing Python Application ..."
	@$(PYTHON) -m unittest
	@$(PYTHON) -m pytest
	-#find coverage/ -mindepth 1 -delete
#	pytest $${TESTS}
#	@$(PYTHON) setup.py sdist

#
# Doc Commands
#

doc: ## Generates the documentation
doc:
	@# Help: Generates the documentation
	${PYTHON} setup.py build_sphinx
	@echo
	@echo Generated documentation: "file://"$$(readlink -f doc/build/html/index.html)
	@echo


#
# Distribute Commands
#

dist: ## Distributes the application
dist: test
	@# Help: Distributes the application
	python setup.py sdist

#
# Docker Commands
#

#Builds Docker Container Image
docker-build-container: ## Builds Docker Container Image
	@# Help: Builds the docker container image of an app
	@echo "Building Docker Container Image ..."
	#docker build --progress=plain -t ${DOCKER_REPOSITORY}:${DOCKER_IMAGE_TAG} --target ${PROJECT_NAME} .
	docker build -t ${DOCKER_CONTAINER_NAME}:${DOCKER_IMAGE_TAG} .

# Runs the Docker Container
docker-run-container: ## Runs Docker Container
	@# Help: Runs the docker container of an app as background service
	@echo "Running Docker Container ..."
	@#docker run --name ${DOCKER_CONTAINER_NAME} --rm -p ${HOST_PORT}:${CONTAINER_PORT} -d -e APP_NAME=${APP_NAME} ${DOCKER_IMAGE_TAG}
	docker run --name ${DOCKER_CONTAINER_NAME} --rm -p ${HOST_PORT}:${CONTAINER_PORT} -d ${PROJECT_NAME}:${DOCKER_IMAGE_TAG}
	@#docker container run --name ${DOCKER_CONTAINER_NAME} --rm -p ${HOST_PORT}:${CONTAINER_PORT} -d ${PROJECT_NAME}:${DOCKER_IMAGE_TAG}


# Builds Docker Image and Run it.
#docker-build-all: ## Builds Docker Image and Runs it
#	@# Help: Builds the docker image of an app and runs it
#	@echo "Building Docker Image and Running it ..."
#	docker-build-image
#	docker-run-container

# Shows Docker Container Logs
docker-log-container: ## Shows Docker Container Logs
	@# Help: Shows the docker container's log of an app
	@echo "Showing Docker Container Logs [${DOCKER_CONTAINER_NAME}] ..."
	docker logs -f ${DOCKER_CONTAINER_NAME}
	#docker container logs -f ${DOCKER_CONTAINER_NAME}

# Executes the bash shell in the specified container, giving you a basic shell prompt.
# To exit back out of the container, type exit then press ENTER:
docker-bash-container: ## Executes the 'bash' shell in the container
	@# Help: Executes the 'bash' shell in the container, giving you a basic shell prompt.
	@echo "Executing Docker Container [${DOCKER_CONTAINER_NAME}] ..."
	docker exec -it ${DOCKER_CONTAINER_NAME} bash

# Stops Docker Container
docker-stop-container: ## Stops Docker Container
	@# Help: Stops the docker container of an app
	@echo "Stopping Docker Container [${DOCKER_CONTAINER_NAME}] ..."
	docker stop ${DOCKER_CONTAINER_NAME}
	docker container rm ${DOCKER_CONTAINER_NAME}

#
# Lint Commands
#

lint: ## Runs the application, exit if critical rules are broken
lint:
	@# Help: Runs the application, exit if critical rules are broken
	# stop the build if there are Python syntax errors or undefined names
	flake8 src --count --select=E9,F63,F7,F82 --show-source --statistics
	# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	flake8 src --count --exit-zero --statistics

#
# MySQL Docker Commands
#
mysql-create-network: ## Creates MySQL Network
	@# Help: Creates MySQL Network
	@echo "Creating MySQL Network"
	docker network create $(NETWORK_NAME)

mysql-run-container: ## Pulls and Runs MySQL Docker Image
	@# Help: Pulls and Runs MySQL Docker Image
	@echo "Pulling and Running MySQL Docker Image"
	docker container run --network $(NETWORK_NAME) --name $(MYSQL_CONTAINER_NAME) -e MYSQL_ROOT_PASSWORD=$(MYSQL_ROOT_PASSWORD) -e MYSQL_DATABASE=$(MYSQL_DATABASE) -d mysql:latest

# Shows the MySQL Docker container logs
mysql-log-container: ## Shows the MySQL Docker container logs
	@# Help: Shows the MySQL Docker container logs
	@echo "Showing MySQL Docker Container Logs [${DOCKER_CONTAINER_NAME}] ..."
	docker logs -f ${MYSQL_CONTAINER_NAME}
	#docker container logs -f ${MYSQL_CONTAINER_NAME}

# Executes the bash shell in the specified container, giving you a basic shell prompt.
# To exit back out of the container, type exit then press ENTER:
mysql-bash-container: ## Executes the 'bash' shell in the MySQL container
	@# Help: Executes the 'bash' shell in the MySQL container, giving you a basic shell prompt.
	@echo "Executing 'bash' shell in MySQL Container [${MYSQL_CONTAINER_NAME}] ..."
	docker exec -it ${MYSQL_CONTAINER_NAME} bash
	#docker exec -it ${MYSQL_CONTAINER_NAME} mysql -uroot -proot
	#use EmployeeService;
	#show databases;
	#show tables;
	#exit;

# Connects the MySQL Container as 'bash' shell prompt.
mysql-connect-database: ## Connects the MySQL Container as 'bash' shell prompt.
	@# Help: Connects the MySQL Container as 'bash' shell prompt.
	@echo "Connecting MySQL [${MYSQL_CONTAINER_NAME}] container as 'bash' shell prompt ..."
	docker exec -it ${MYSQL_CONTAINER_NAME} mysql -uroot -proot
	use posts;
	#exit;

# Stops MySQL Docker Container
mysql-stop-container: ## Stops MySQL Docker Container
	@# Help: Stops the MySQL Docker Container
	@echo "Stopping MySQL Docker Container [${MYSQL_CONTAINER_NAME}] ..."
	docker stop ${MYSQL_CONTAINER_NAME}
	docker rm ${MYSQL_CONTAINER_NAME}

