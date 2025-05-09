VENV = venv
PYTHON = $(VENV)/bin/python

default: help

.PHONY: help 
help: ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.PHONY: test 
test: ## Run tests
	$(PYTHON) manage.py test

.PHONY: makemigrations 
makemigrations: ## Create new migration
	$(PYTHON) manage.py makemigrations

.PHONY: migrate 
migrate: ## Execute migrations
	$(PYTHON) manage.py migrate

.PHONY: run 
run: ## Deploy server
	$(PYTHON) manage.py runserver

.PHONY: djshell
djshell: ## Access django shell
	$(PYTHON) manage.py shell
