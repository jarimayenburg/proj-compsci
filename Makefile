REQUIREMENTS_FILE=./requirements.txt

build: env_active
	@python3 -m pip install -r $(REQUIREMENTS_FILE)

env_active: env
ifndef VIRTUAL_ENV
	$(error Not in Python virtual environment, run env/bin/activate)
endif

env:
	python3 -m venv env

clean:
	rm -rf env

run:
	@python3 wildfire_simulator
