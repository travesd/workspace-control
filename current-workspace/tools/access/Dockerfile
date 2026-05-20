ARG CLOUDFLARED_BASE_IMAGE=cloudflare/cloudflared:latest

FROM ${CLOUDFLARED_BASE_IMAGE} AS cloudflared

FROM alpine:3.20

RUN apk add --no-cache ca-certificates curl

COPY --from=cloudflared /usr/local/bin/cloudflared /usr/local/bin/cloudflared

RUN mkdir -p /home/nonroot/.cloudflared && \
    chown -R 65532:65532 /home/nonroot
USER 65532:65532

ENTRYPOINT ["cloudflared", "--no-autoupdate"]
CMD ["version"]
