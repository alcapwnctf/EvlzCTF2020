FROM caddy:alpine AS caddy
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
ENV BIND 127.0.0.1:8000
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
COPY ./src /app
COPY ./scripts /opt/scripts/
COPY ./frontend /frontend
COPY ./prestart.sh /app
COPY Caddyfile /

EXPOSE 80

COPY --from=caddy /usr/bin/caddy /usr/bin/caddy
