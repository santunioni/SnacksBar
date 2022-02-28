lint:
	@poetry run black .
	@poetry run pylint src
	@poetry run pylint tests

mypy:
	@poetry run mypy .

test:
	@poetry run pytest tests

pre-commit:
	@pre-commit run --all-files --hook-stage merge-commit

checks: lint mypy pre-commit test

push:
	@git push && git push --tags

run:
	@mkdir -p data/
	@docker-compose up --build -d
	@docker-compose logs -f
