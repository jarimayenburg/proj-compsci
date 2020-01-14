REQUIREMENTS_FILE=./requirements.txt

env_active: env
ifndef VIRTUAL_ENV
	$(error Not in Python virtual environment, run env/bin/activate)
endif

env:
	python3 -m venv env

install_reqs: env_active
	@python3 -m pip install -r $(REQUIREMENTS_FILE)

run:
	@python3 wildfire_simulator
