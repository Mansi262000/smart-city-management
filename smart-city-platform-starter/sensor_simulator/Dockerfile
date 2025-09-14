FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY simulate.py /app/simulate.py
CMD ["python", "simulate.py"]
