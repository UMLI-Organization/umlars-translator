setup:
	poetry lock
	poetry install

test:
	poetry run python -m pytest

tox-test:
	poetry run python -m tox

docs:
	poetry run mkdocs serve

docs-build:
	poetry run mkdocs build

clean:
	rm -rf .tox
	rm -rf site
	rm -rf dist
	rm -rf */.pytest_cache
	rm -rf */__pycache__
	rm -rf .pytest_cache
	rm -rf __pycache__

export:
	poetry lock
	poetry export --without-hashes --without dev -f requirements.txt -o requirements.txt

version-new-prerelease:
	poetry version prerelease

version-new-release:
	poetry version patch

publish-test:
	poetry publish --build -r test-pypi

publish:
	poetry publish --build

docker-setup:
	poetry install --no-interaction --no-ansi

server-start:
	poetry install
	poetry run python3 -m umlars_translator --run-server

server-start-dev:
	poetry install
	poetry run python3 -m umlars_translator --run-server

.PHONY: setup tests docs clean export version-new-release version-new-prerelease publish publish-test