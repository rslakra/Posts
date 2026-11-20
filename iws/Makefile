# Author: Rohtash Lakra
# Signifies our desired python version
# Makefile macros (or variables) are defined a little bit differently than traditional bash, keep in mind that in
# the Makefile there's top-level Makefile-only syntax, and everything else is bash script syntax.
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
ACTIVATE=$(VENV)/bin/activate
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
MYSQL_IMAGE=mysql:8.4
MYSQL_HOST_PORT=3306
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
.PHONY: help clean clean-images start stop status db-up db-down
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

#
# Clean Commands
#

# In this context, the *.project pattern means "anything that has the .project extension"
clean: ## Remove build and cache files and the docker images (created and stale) of this project
clean: clean-images
	@# Help: Remove build and cache files and the docker images (created and stale) of this project
	@echo "Cleaning up ..."
	#$(VENV)/bin/deactivate
	#deactivate
	rm -rf $(VENV)
	rm -rf $(REMOVE_FILES) *.project
	find . -name '*.py[co]' -delete
	find . -type f -name '*.py[co]' -delete

# Removes the docker images of this project:
# - the app container (it uses the image) and all the images of '$(DOCKER_CONTAINER_NAME)' (every tag), and
# - the stale (dangling, '<none>') images that were left over by rebuilding it. They are found via the 'project' label
#   of the Dockerfile, so the images of other projects are never touched.
# The MySQL container/volume (data) and the pulled 'mysql' image are NOT removed. Skipped when Docker isn't running.
clean-images: ## Remove the docker images (created and stale) of this project
	@# Help: Remove the docker images (created and stale) of this project
	@if ! docker info >/dev/null 2>&1; then \
		echo "Docker is not running, skipping the removal of the docker images."; \
		exit 0; \
	fi; \
	if docker container inspect $(DOCKER_CONTAINER_NAME) >/dev/null 2>&1; then \
		echo "Removing container [$(DOCKER_CONTAINER_NAME)] that uses the image ..."; \
		docker rm -f $(DOCKER_CONTAINER_NAME) >/dev/null; \
	fi; \
	IMAGES=$$(docker images -q $(DOCKER_CONTAINER_NAME) | sort -u); \
	if [ -n "$$IMAGES" ]; then \
		echo "Removing the images of [$(DOCKER_CONTAINER_NAME)] ..."; \
		docker image rm -f $$IMAGES; \
	else \
		echo "No images of [$(DOCKER_CONTAINER_NAME)] found."; \
	fi; \
	echo "Removing the stale (dangling) images of [$(PROJECT_NAME)] ..."; \
	docker image prune -f --filter "label=project=$(PROJECT_NAME)"


#
# Setup Environment Commands
#

venv: ## Creates virtual environment if missing
venv:
	@# Help: Creates virtual environment if missing
	@if [ ! -x "$(PYTHON)" ]; then \
		echo "Creating Python virtual environment ..."; \
		python3 -m venv $(VENV); \
	fi
	@$(PYTHON) -m ensurepip --upgrade >/dev/null 2>&1 || true

install-packages: ## Upgrades pip and installs requirements
install-packages: venv
	@# Help: Upgrades pip and installs requirements
	@echo "Installing project packages ..."
	@$(PYTHON) -m pip install --upgrade pip
	@$(PYTHON) -m pip install -r requirements.txt


setup: ## Alias of install-packages target
setup: install-packages
	@# Help: Alias of install-packages target


#
# Start Application Commands
#

start-fastapi: ## Runs FastAPI Application
start-fastapi: venv stop-fastapi
	@# Help: Runs FastAPI Application
	@echo "Running FastAPI Application ..."
	@$(PYTHON) -m uvicorn main:app --host 0.0.0.0 --port 8082 --reload

stop-fastapi: ## Stops processes listening on 8082
	@# Help: Stops stale FastAPI/uvicorn listeners
	@PIDS=$$(lsof -ti tcp:8082 2>/dev/null || true); \
	if [ -n "$$PIDS" ]; then \
		echo "Stopping existing process(es) on 8082: $$PIDS"; \
		kill $$PIDS; \
		sleep 1; \
	else \
		echo "No existing process found on 8082"; \
	fi

#
# Container Based Application Commands
#
# Usage:
#   make start             # builds the image and runs the app container (SQLite, the settings of '.env')
#   make start DB=mysql    # also starts the MySQL container ('db-up') and runs the app against it
#   make stop              # stops and removes the app container
#   make status            # shows the status of the DB and app containers
#   make db-up             # starts the MySQL container (waits until it accepts connections)
#   make db-down           # stops and removes the MySQL container (the data volume is kept)
#

# Database used by the app container: 'sqlite' (default, uses '.env') or 'mysql' (uses the MySQL container).
DB?=sqlite
START_DEPS:=
APP_DB_ARGS:=
ifeq ($(DB),mysql)
START_DEPS:=db-up
APP_DB_ARGS:=-e DB_TYPE=MYSQL -e DB_HOSTNAME=$(MYSQL_CONTAINER_NAME) -e DB_PORT=3306 -e DB_NAME=$(MYSQL_DATABASE) -e DB_USERNAME=root -e DB_PASSWORD=$(MYSQL_ROOT_PASSWORD)
endif

start: ## Builds and starts the FastAPI app as a docker container
start: $(START_DEPS) docker-build-container
	@# Help: Builds and starts the FastAPI app as a docker container (DB=mysql uses the MySQL container)
	@echo "Starting FastAPI container [$(DOCKER_CONTAINER_NAME)] with DB=$(DB) ..."
	@docker network inspect $(NETWORK_NAME) >/dev/null 2>&1 || docker network create $(NETWORK_NAME) >/dev/null
	@docker rm -f $(DOCKER_CONTAINER_NAME) >/dev/null 2>&1 || true
	docker run --name $(DOCKER_CONTAINER_NAME) --network $(NETWORK_NAME) -p $(HOST_PORT):$(CONTAINER_PORT) -d $(APP_DB_ARGS) $(DOCKER_CONTAINER_NAME):$(DOCKER_IMAGE_TAG)
	@echo "FastAPI is starting on http://localhost:$(HOST_PORT) (docs: http://localhost:$(HOST_PORT)/docs)"
	@echo "Logs: make docker-log-container"

stop: ## Stops the running FastAPI docker container
	@# Help: Stops and removes the running FastAPI docker container
	@if docker container inspect $(DOCKER_CONTAINER_NAME) >/dev/null 2>&1; then \
		echo "Stopping FastAPI container [$(DOCKER_CONTAINER_NAME)] ..."; \
		docker stop $(DOCKER_CONTAINER_NAME) >/dev/null; \
		docker rm -f $(DOCKER_CONTAINER_NAME) >/dev/null; \
		echo "Stopped."; \
	else \
		echo "No container named [$(DOCKER_CONTAINER_NAME)] found."; \
	fi

db-up: ## Starts the MySQL docker container
	@# Help: Starts the MySQL docker container and waits until it accepts connections
	@docker network inspect $(NETWORK_NAME) >/dev/null 2>&1 || docker network create $(NETWORK_NAME) >/dev/null
	@if docker container inspect $(MYSQL_CONTAINER_NAME) >/dev/null 2>&1; then \
		echo "Starting existing MySQL container [$(MYSQL_CONTAINER_NAME)] ..."; \
		docker start $(MYSQL_CONTAINER_NAME) >/dev/null; \
	else \
		echo "Creating MySQL container [$(MYSQL_CONTAINER_NAME)] ..."; \
		docker run --name $(MYSQL_CONTAINER_NAME) --network $(NETWORK_NAME) \
			-p $(MYSQL_HOST_PORT):3306 \
			-v $(MYSQL_CONTAINER_NAME)-data:/var/lib/mysql \
			-e MYSQL_ROOT_PASSWORD=$(MYSQL_ROOT_PASSWORD) -e MYSQL_DATABASE=$(MYSQL_DATABASE) \
			-d $(MYSQL_IMAGE) >/dev/null; \
	fi
	@echo "Waiting for MySQL to accept connections ..."
	@# '-h 127.0.0.1' forces TCP, so the temporary server of the image's initialization is not mistaken as ready.
	@for i in $$(seq 1 60); do \
		if docker exec $(MYSQL_CONTAINER_NAME) mysqladmin ping -h 127.0.0.1 -uroot -p$(MYSQL_ROOT_PASSWORD) --silent >/dev/null 2>&1; then \
			echo "MySQL is ready on localhost:$(MYSQL_HOST_PORT) (database: $(MYSQL_DATABASE))"; \
			exit 0; \
		fi; \
		sleep 2; \
	done; \
	echo "MySQL did not become ready in time. Check: docker logs $(MYSQL_CONTAINER_NAME)"; \
	exit 1

db-down: ## Stops the MySQL docker container
	@# Help: Stops and removes the MySQL docker container (the data volume is kept)
	@if docker container inspect $(MYSQL_CONTAINER_NAME) >/dev/null 2>&1; then \
		echo "Stopping MySQL container [$(MYSQL_CONTAINER_NAME)] ..."; \
		docker stop $(MYSQL_CONTAINER_NAME) >/dev/null; \
		docker rm -f $(MYSQL_CONTAINER_NAME) >/dev/null; \
		echo "Stopped. Data volume [$(MYSQL_CONTAINER_NAME)-data] is kept, remove it with: docker volume rm $(MYSQL_CONTAINER_NAME)-data"; \
	else \
		echo "No container named [$(MYSQL_CONTAINER_NAME)] found."; \
	fi

status: ## Shows the status of the DB and FastAPI app containers
	@# Help: Shows the status of the running DB and FastAPI app containers
	@if ! docker info >/dev/null 2>&1; then \
		echo "Docker is not running (or not reachable)."; \
		exit 1; \
	fi
	@printf "%-6s %-18s %-12s %s\n" "ROLE" "CONTAINER" "STATUS" "PORTS"
	@printf "%-6s %-18s %-12s %s\n" "----" "---------" "------" "-----"
	@for entry in "db:$(MYSQL_CONTAINER_NAME)" "app:$(DOCKER_CONTAINER_NAME)"; do \
		role=$${entry%%:*}; name=$${entry#*:}; \
		if docker container inspect $$name >/dev/null 2>&1; then \
			state=$$(docker inspect -f '{{.State.Status}}' $$name); \
			ports=$$(docker port $$name 2>/dev/null | tr '\n' ' '); \
			printf "%-6s %-18s %-12s %s\n" "$$role" "$$name" "$$state" "$${ports:--}"; \
		else \
			printf "%-6s %-18s %-12s %s\n" "$$role" "$$name" "not created" "-"; \
		fi; \
	done
	@if [ "$$(docker inspect -f '{{.State.Running}}' $(DOCKER_CONTAINER_NAME) 2>/dev/null)" = "true" ]; then \
		if curl -fsS -m 3 http://localhost:$(HOST_PORT)/health-check >/dev/null 2>&1; then \
			echo "App health: OK (http://localhost:$(HOST_PORT)/health-check)"; \
		else \
			echo "App health: NOT RESPONDING (http://localhost:$(HOST_PORT)/health-check), check: make docker-log-container"; \
		fi; \
	fi
	@if [ "$$(docker inspect -f '{{.State.Running}}' $(MYSQL_CONTAINER_NAME) 2>/dev/null)" = "true" ]; then \
		if docker exec $(MYSQL_CONTAINER_NAME) mysqladmin ping -h 127.0.0.1 -uroot -p$(MYSQL_ROOT_PASSWORD) --silent >/dev/null 2>&1; then \
			echo "DB health:  OK (MySQL accepts connections)"; \
		else \
			echo "DB health:  NOT READY, check: make mysql-log-container"; \
		fi; \
	fi

#
# Test Commands
#

# The ${} notation is specific to the make syntax and is very similar to bash's $()
# This function uses pytest to test our source files
test: ## Tests the python application
test:
	@# Help: Tests the python application
	@echo "Testing Python Application ..."
	@# ENV_TYPE=test selects '.env.test', so the tests never touch the development database.
	@ENV_TYPE=test $(PYTHON) -m unittest
	@# pytest is optional (not part of requirements.txt), the unittest run above already executes all the tests.
	@if $(PYTHON) -c "import pytest" >/dev/null 2>&1; then \
		ENV_TYPE=test $(PYTHON) -m pytest; \
	else \
		echo "pytest is not installed, skipping the pytest run."; \
	fi
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

