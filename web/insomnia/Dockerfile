FROM caddy:alpine AS caddy
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
ENV BIND 127.0.0.1:8000
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
COPY ./app /app
COPY ./frontend /frontend
COPY ./memes /opt/memes
COPY ./font /opt/font
COPY ./prestart.sh /app
COPY Caddyfile /
COPY flag /
RUN chmod 444 /flag
RUN useradd -u 8877 appuser
USER appuser

EXPOSE 8888

COPY --from=caddy /usr/bin/caddy /usr/bin/caddy
