FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV PORT=8000

RUN mkdir -p uploads processed variants

# Preload AI models during build
RUN python preload_models.py

EXPOSE 8000

CMD ["gunicorn", "--config", "gunicorn.conf.py", "api_server:app"]
