CODE_FOLDERS := apps service clients db
TEST_FOLDERS := tests

.PHONY: run migration db_upgrade test lint format


format:
	isort $(CODE_FOLDERS) $(TEST_FOLDERS)
	poetry run black --line-length 79 --skip-string-normalization --extend-exclude="protos" $(CODE_FOLDERS) $(TEST_FOLDERS)


migration:
	poetry run alembic revision --autogenerate -m"$(name)"

db_upgrade:
	poetry run alembic upgrade head
