setup:
	poetry lock
	poetry install

test:
	poetry run pytest

tox-test:
	poetry run tox

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
	poetry run uvicorn src.umlars_translator.app.main:app --reload --host="0.0.0.0" --port=8080

server-start-dev:
	poetry run uvicorn src.umlars_translator.app.main:app --reload --host="0.0.0.0" --port=8080

.PHONY: setup tests docs clean export version-new-release version-new-prerelease publish publish-test