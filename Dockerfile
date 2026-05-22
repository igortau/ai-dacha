# Placeholder Dockerfile for portfolio MVP.
# Replace this with the real FastAPI backend Dockerfile when source code is added.

FROM python:3.12-slim

WORKDIR /app

RUN pip install fastapi uvicorn

COPY README.md /app/README.md

CMD ["python", "-c", "print('AI Dacha API placeholder. Add backend source code before running this container.')"]
