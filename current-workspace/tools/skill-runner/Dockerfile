FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl gnupg gosu lsb-release netcat-openbsd \
    && curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc \
       | gpg --dearmor -o /usr/share/keyrings/pgdg.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/pgdg.gpg] https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" \
       > /etc/apt/sources.list.d/pgdg.list \
    && apt-get update && apt-get install -y --no-install-recommends \
        postgresql-client-16 \
    && curl -fsSL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 \
       -o /usr/local/bin/cloudflared \
    && chmod +x /usr/local/bin/cloudflared \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir requests

COPY entrypoint.sh /usr/local/bin/skill-entrypoint
RUN chmod +x /usr/local/bin/skill-entrypoint
RUN groupadd -g 65532 cloudflared && \
    useradd -r -u 65532 -g cloudflared -d /home/nonroot -s /usr/sbin/nologin cloudflared && \
    mkdir -p /home/nonroot/.cloudflared && \
    chown -R 65532:65532 /home/nonroot

ENV HOME=/root
WORKDIR /work

ENTRYPOINT ["/usr/local/bin/skill-entrypoint"]
CMD ["bash"]
