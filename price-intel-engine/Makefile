.PHONY: install test run clean docker-build

install:
	pip install -r price-intel-engine/requirements.txt
	python3 price-intel-engine/scripts/setup_config.py

test:
	export PYTHONPATH=$PYTHONPATH:. && pytest price-intel-engine/tests

run:
	export PYTHONPATH=$PYTHONPATH:. && python3 price-intel-engine/src/main.py --term "Amul Butter" --dry-run

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-build:
	docker build -t price-intel -f price-intel-engine/Dockerfile price-intel-engine
