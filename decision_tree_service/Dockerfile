FROM python:3.9-slim
WORKDIR /app
COPY . /app/
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5004
CMD ["gunicorn", "--bind", "0.0.0.0:5004", "app:app"]
