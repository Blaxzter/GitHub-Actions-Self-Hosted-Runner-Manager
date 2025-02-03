FROM python:3.11-slim as builder

WORKDIR /app
RUN pip install --user requests docker python-dotenv

FROM python:3.11-slim as final
WORKDIR /app
COPY --from=builder /root/.local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY agent.py .

CMD ["python", "agent.py"] 