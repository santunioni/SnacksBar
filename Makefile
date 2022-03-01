black:
	@poetry run black .

autoflake:
	@poetry run autoflake src \
	--in-place \
	--recursive \
	--expand-star-imports \
	--remove-duplicate-keys \
	--remove-unused-variables \
	--remove-all-unused-imports \
	--ignore-init-module-imports

pylint:
	@poetry run pylint --rcfile pylint.cfg src tests

lint: black autoflake pylint

mypy:
	@poetry run mypy src tests

pre-commit:
	@pre-commit run --all-files --hook-stage merge-commit || true

test:
	@poetry run pytest tests

checks: lint mypy pre-commit test

push:
	@git push && git push --tags

run:
	@mkdir -p data/
	@docker-compose up --build -d
	@docker-compose logs -f

m=""
msg=""
message=""
migrations:
	@cd src || true && alembic revision --autogenerate -m "$(m)$(msg)$(message)"

migrate:
	@cd src || true && alembic upgrade head

dev: migrate
	@cd src && PYTHONPATH=. python snacksbar/dev_server.py
