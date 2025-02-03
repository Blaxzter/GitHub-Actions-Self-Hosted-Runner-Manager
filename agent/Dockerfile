FROM python:3.11-slim

WORKDIR /app
RUN pip install --user requests docker python-dotenv

WORKDIR /app
COPY agent.py .

CMD ["python", "agent.py"] 