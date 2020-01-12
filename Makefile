REQUIREMENTS_FILE=./requirements.txt

.PHONY: env

env:
	python3 -m venv env

install_reqs:
	@python3 -m pip install -r $(REQUIREMENTS_FILE)
