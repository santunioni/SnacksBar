lint:
	@poetry run isort .
	@poetry run black .
	@poetry run pylint snacksbar
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
