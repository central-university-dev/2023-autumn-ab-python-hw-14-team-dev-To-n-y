CODE_FOLDERS := app
TEST_FOLDERS := tests

.PHONY: run migration db_upgrade test lint format


format:
	poetry run isort $(CODE_FOLDERS) $(TEST_FOLDERS)
	poetry run black $(CODE_FOLDERS) $(TEST_FOLDERS)


lint:
	isort --check $(CODE_FOLDERS) $(TEST_FOLDERS)
	black --check $(CODE_FOLDERS) $(TEST_FOLDERS)
	flake8 $(CODE_FOLDERS) $(TEST_FOLDERS)
	pylint $(CODE_FOLDERS) $(TEST_FOLDERS)
	mypy $(CODE_FOLDERS) $(TEST_FOLDERS)


migration:
	poetry run alembic revision --autogenerate -m"$(name)"

db_upgrade:
	poetry run alembic upgrade head
