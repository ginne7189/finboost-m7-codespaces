FROM python:3.12-slim
WORKDIR /app
COPY app.py client.py worker.py ./
RUN useradd --create-home student && mkdir /app/data && chown student /app/data
USER student
EXPOSE 8000
CMD ["python", "app.py", "--host", "0.0.0.0"]
