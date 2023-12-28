CODE_FOLDERS := app
TEST_FOLDERS := tests

.PHONY: run migration db_upgrade test lint format run

run:
	poetry run uvicorn app.main:app --reload

format:
	poetry run black --line-length 79 --skip-string-normalization $(CODE_FOLDERS) $(TEST_FOLDERS)
	poetry run isort --profile black $(CODE_FOLDERS) $(TEST_FOLDERS)

test:
	poetry run pytest $(TEST_FOLDERS)

lint:
	isort --profile black --check $(CODE_FOLDERS) $(TEST_FOLDERS)
	black --check --line-length 79 --skip-string-normalization $(CODE_FOLDERS) $(TEST_FOLDERS)
	flake8 $(CODE_FOLDERS) $(TEST_FOLDERS)
	pylint $(CODE_FOLDERS) $(TEST_FOLDERS)
	mypy --install-types --non-interactive
	mypy $(CODE_FOLDERS) $(TEST_FOLDERS)


migration:
	poetry run alembic revision --autogenerate -m"$(name)"

db_upgrade:
	poetry run alembic upgrade head
