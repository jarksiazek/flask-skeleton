PWD=$(shell pwd)
prereq:
	sudo apt-get install python3.10-venv
	python3 -m venv $(PWD)/venv
	source $(PWD)/venv/bin/activate
python-env:
	echo $(PWD)/venv

requirement:
	pip3 install -r requirements.txt


test-unit:
	pytest --cov src/code --cov-report xml --cov-report term src/tests

test-unit-dev:
	pytest --cov src/code --cov-report html --cov-report term src/tests

.PHONY: python-env

