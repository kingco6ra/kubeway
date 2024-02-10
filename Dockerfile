FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y curl apt-transport-https ca-certificates gpg && \
    rm -rf /var/lib/apt/lists/*

RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    chmod +x ./kubectl && \
    mv ./kubectl /usr/local/bin/kubectl

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY src/ /app
COPY poetry.lock /app
COPY pyproject.toml /app
COPY config.yaml /app

WORKDIR /app

RUN poetry install

CMD ["poetry", "run", "python3", "main.py"]
