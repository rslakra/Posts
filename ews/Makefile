# Author: Rohtash Lakra
# Makefile of the 'ews' (External Web Service) of the Posts project. It is a Flask application (see wsgi.py).
# Makefile macros (or variables) are defined a little bit differently than traditional bash, keep in mind that in
# the Makefile there's top-level Makefile-only syntax, and everything else is bash script syntax.
#
# Usage:
#   make setup     # creates the virtual environment and installs the requirements
#   make run       # runs the app in the foreground (debug mode with auto-reload), stop it with Ctrl+C
#   make start     # starts the app in the background, waits until it is healthy
#   make status    # shows whether the app is running and healthy
#   make stop      # stops the app started by 'make start'
#   make test      # runs the unit tests
#   make clean     # stops the app and removes the venv, caches, pid and log files
#
# The host/port can be overridden, e.g. `make start PORT=8081` (the 'iws' container uses 8080 by default).

# --------------------------------------------------------------
# Variables
# --------------------------------------------------------------
# Python Settings
VENV:=venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
# App Settings (the app is mounted under '/posts', see webapp/__init__.py)
HOST?=127.0.0.1
PORT?=8080
APP_URL=http://$(HOST):$(PORT)/posts
HEALTH_URL=$(APP_URL)/health-check/
# The background app's process id and log
PID_FILE:=.ews.pid
LOG_FILE:=ews.log

# .PHONY defines parts of the makefile that are not dependant on any specific file
.PHONY: help setup install-packages run start stop status test clean

# Defines the default target that `make` will to try to make when we just type `make`
.DEFAULT_GOAL:=help

# Lists the targets that have a '## description' comment.
help: ## Shows this help
	@echo
	@echo 'The following commands can be used:'
	@echo
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z_-]+:.*## / {printf "  %-18s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo

#
# Setup Environment Commands
#

$(PYTHON):
	@echo "Creating Python virtual environment ..."
	@python3 -m venv $(VENV)
	@$(PYTHON) -m ensurepip --upgrade >/dev/null 2>&1 || true

install-packages: $(PYTHON) ## Upgrades pip and installs the requirements
	@echo "Installing project packages ..."
	@$(PYTHON) -m pip install --upgrade pip
	@$(PYTHON) -m pip install -r requirements.txt

setup: install-packages ## Creates the virtual environment and installs the requirements (alias of install-packages)

#
# Application Commands
#

run: $(PYTHON) ## Runs the Flask app in the foreground (debug mode with auto-reload), stop it with Ctrl+C
	@echo "Running Flask Application on $(APP_URL) ..."
	@$(PYTHON) -m flask --app wsgi run --host $(HOST) --port $(PORT) --debug

# The debug mode is NOT used here: its reloader starts a child process that would outlive the stopped parent.
start: $(PYTHON) ## Starts the Flask app in the background and waits until it is healthy
	@if [ -f $(PID_FILE) ] && kill -0 $$(cat $(PID_FILE)) 2>/dev/null; then \
		echo "Flask Application is already running (pid $$(cat $(PID_FILE))) on $(APP_URL)"; \
		exit 0; \
	fi; \
	rm -f $(PID_FILE); \
	echo "Starting Flask Application on $(APP_URL) ..."; \
	nohup $(PYTHON) -m flask --app wsgi run --host $(HOST) --port $(PORT) >$(LOG_FILE) 2>&1 & \
	echo $$! >$(PID_FILE); \
	for i in $$(seq 1 20); do \
		if ! kill -0 $$(cat $(PID_FILE)) 2>/dev/null; then \
			echo "Flask Application failed to start, see $(LOG_FILE):"; \
			tail -n 15 $(LOG_FILE); \
			rm -f $(PID_FILE); \
			exit 1; \
		fi; \
		if curl -fsS -m 2 $(HEALTH_URL) >/dev/null 2>&1; then \
			echo "Flask Application is running (pid $$(cat $(PID_FILE))) on $(APP_URL)"; \
			echo "Log: $(LOG_FILE), stop it with: make stop"; \
			exit 0; \
		fi; \
		sleep 0.5; \
	done; \
	echo "Flask Application did not become healthy in time, see $(LOG_FILE)"; \
	exit 1

# Only the process that was started by 'make start' (and is a flask process) is stopped, never the process that
# merely listens on the port.
stop: ## Stops the Flask app started by 'make start'
	@if [ -f $(PID_FILE) ]; then \
		PID=$$(cat $(PID_FILE)); \
		if kill -0 $$PID 2>/dev/null && ps -p $$PID -o command= | grep -q "flask --app wsgi"; then \
			echo "Stopping Flask Application (pid $$PID) ..."; \
			kill $$PID; \
			for i in $$(seq 1 20); do kill -0 $$PID 2>/dev/null || break; sleep 0.25; done; \
			echo "Stopped."; \
		else \
			echo "No running Flask Application found for pid $$PID."; \
		fi; \
		rm -f $(PID_FILE); \
	else \
		echo "No Flask Application started by 'make start' found."; \
	fi

status: ## Shows whether the Flask app (started by 'make start') is running and healthy
	@if [ -f $(PID_FILE) ] && kill -0 $$(cat $(PID_FILE)) 2>/dev/null; then \
		echo "Flask Application: running (pid $$(cat $(PID_FILE))) on $(APP_URL)"; \
		if curl -fsS -m 3 $(HEALTH_URL) >/dev/null 2>&1; then \
			echo "App health:        OK ($(HEALTH_URL))"; \
		else \
			echo "App health:        NOT RESPONDING ($(HEALTH_URL)), see $(LOG_FILE)"; \
		fi; \
	else \
		echo "Flask Application: not running (start it with: make start)"; \
	fi

#
# Test Commands
#

test: $(PYTHON) ## Runs the unit tests
	@echo "Testing Python Application ..."
	@$(PYTHON) -m unittest

#
# Clean Commands
#

clean: stop ## Stops the app and removes the virtual environment, caches, pid and log files
	@echo "Cleaning up ..."
	rm -rf $(VENV)
	rm -f $(PID_FILE) $(LOG_FILE)
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +
	find . -type f -name '*.py[co]' -delete
