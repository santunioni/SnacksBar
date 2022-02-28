FROM python:3.7
RUN pip install --upgrade pip
RUN pip install poetry
WORKDIR /home/app
COPY pyproject.toml poetry.lock ./
RUN poetry export --without-hashes > requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000
COPY src ./
ENTRYPOINT ["uvicorn", "--host", "0.0.0.0"]
