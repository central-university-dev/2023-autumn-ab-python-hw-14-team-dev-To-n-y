CODE_FOLDERS := app
TEST_FOLDERS := tests

.PHONY: run migration db_upgrade test lint format


format:
	poetry run isort $(CODE_FOLDERS) $(TEST_FOLDERS)
	poetry run black --line-length 79 --skip-string-normalization --extend-exclude="protos" $(CODE_FOLDERS) $(TEST_FOLDERS)


migration:
	poetry run alembic revision --autogenerate -m"$(name)"

db_upgrade:
	poetry run alembic upgrade head
