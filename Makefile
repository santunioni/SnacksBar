lint:
	@poetry run isort .
	@poetry run black .
	@poetry run pylint snacksbar
	@poetry run pylint tests

mypy:
	@poetry run mypy .

test:
	@poetry run pytest tests

checks: lint mypy test

push:
	@git push && git push --tags
