FROM python:3.11.1

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /opt/app

# Install Poetry
RUN pip install poetry

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock app tests db ./

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install

CMD ["poetry", "run", "alembic", "upgrade", "head"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
