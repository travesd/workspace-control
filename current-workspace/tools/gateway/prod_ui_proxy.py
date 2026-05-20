#!/usr/bin/env python3
"""Local UI router with Cloudflare Access-backed prod dashboard API proxying."""

from __future__ import annotations

import http.server
import json
import os
import subprocess
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass


HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
}

SAFE_PROD_METHODS = {"GET", "HEAD", "OPTIONS"}


def env_bool(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def parse_prefixes(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def normalize_base_url(value: str) -> str:
    return value.rstrip("/")


def build_target_url(base_url: str, raw_path: str) -> str:
    parsed = urllib.parse.urlsplit(raw_path)
    if parsed.scheme and parsed.netloc:
        raw_path = urllib.parse.urlunsplit(("", "", parsed.path, parsed.query, ""))
    if not raw_path.startswith("/"):
        raw_path = f"/{raw_path}"
    return f"{base_url}{raw_path}"


def prefix_matches(path: str, prefix: str) -> bool:
    clean = prefix.rstrip("/")
    if not clean:
        return False
    return path == clean or path.startswith(f"{clean}/")


def strip_cf_access_cookie(cookie_header: str) -> str:
    parts = []
    for part in cookie_header.split(";"):
        stripped = part.strip()
        if not stripped:
            continue
        if stripped.startswith("CF_Authorization="):
            continue
        parts.append(stripped)
    return "; ".join(parts)


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D401
        return None


OPENER = urllib.request.build_opener(NoRedirectHandler)


@dataclass(frozen=True)
class ProxyConfig:
    local_frontend_url: str
    local_api_url: str
    prod_dashboard_url: str
    local_api_prefixes: list[str]
    allow_mutating_prod: bool
    cloudflared_bin: str
    access_token_url: str
    access_login_command: str
    token_refresh_seconds: int
    request_timeout_seconds: int


class AccessTokenProvider:
    def __init__(self, config: ProxyConfig) -> None:
        self.config = config
        self._lock = threading.Lock()
        self._token: str | None = None
        self._refresh_after = 0.0

    def token(self, force_refresh: bool = False) -> str:
        with self._lock:
            now = time.time()
            if not force_refresh and self._token and now < self._refresh_after:
                return self._token

            env = os.environ.copy()
            env.setdefault("HOME", "/home/nonroot")
            result = subprocess.run(
                [
                    self.config.cloudflared_bin,
                    "access",
                    "token",
                    self.config.access_token_url,
                ],
                capture_output=True,
                env=env,
                text=True,
                timeout=45,
                check=False,
            )
            token = result.stdout.strip()
            if result.returncode != 0 or not token or "\n" in token:
                raise RuntimeError(
                    "Cloudflare Access token unavailable; run "
                    f"{self.config.access_login_command}"
                )
            self._token = token
            self._refresh_after = now + self.config.token_refresh_seconds
            return token


class ProxyHandler(http.server.BaseHTTPRequestHandler):
    server_version = "AgentGatewayProdUIProxy/1.0"

    def do_GET(self) -> None:
        self.handle_proxy()

    def do_HEAD(self) -> None:
        self.handle_proxy()

    def do_POST(self) -> None:
        self.handle_proxy()

    def do_PUT(self) -> None:
        self.handle_proxy()

    def do_PATCH(self) -> None:
        self.handle_proxy()

    def do_DELETE(self) -> None:
        self.handle_proxy()

    def do_OPTIONS(self) -> None:
        self.handle_proxy()

    def log_message(self, fmt: str, *args) -> None:  # noqa: D401
        print(
            "%s - - [%s] %s"
            % (self.client_address[0], self.log_date_time_string(), fmt % args),
            flush=True,
        )

    @property
    def config(self) -> ProxyConfig:
        return self.server.config  # type: ignore[attr-defined]

    @property
    def token_provider(self) -> AccessTokenProvider:
        return self.server.token_provider  # type: ignore[attr-defined]

    def handle_proxy(self) -> None:
        parsed = urllib.parse.urlsplit(self.path)
        path = parsed.path or "/"
        if path == "/__gateway_proxy/health":
            self.write_health()
            return

        upstream_kind, upstream_base = self.route(path)
        if upstream_kind == "prod-dashboard" and not self.config.allow_mutating_prod:
            if self.command.upper() not in SAFE_PROD_METHODS:
                self.send_error(403, "prod proxy is read-only by default")
                return

        content_length = int(self.headers.get("Content-Length") or "0")
        body = self.rfile.read(content_length) if content_length else None
        target_url = build_target_url(upstream_base, self.path)

        try:
            status, headers, response_body = self.forward(
                upstream_kind,
                upstream_base,
                target_url,
                body,
                force_token_refresh=False,
            )
            if upstream_kind == "prod-dashboard" and status in {301, 302, 303, 307, 308, 401, 403}:
                status, headers, response_body = self.forward(
                    upstream_kind,
                    upstream_base,
                    target_url,
                    body,
                    force_token_refresh=True,
                )
        except Exception as exc:  # noqa: BLE001
            self.send_error(502, str(exc))
            return

        self.send_response(status)
        for key, value in headers.items():
            lower = key.lower()
            if lower in HOP_BY_HOP_HEADERS:
                continue
            self.send_header(key, value)
        self.send_header("X-Agent-Gateway-Upstream", upstream_kind)
        self.end_headers()
        if self.command.upper() != "HEAD" and response_body:
            self.wfile.write(response_body)

    def route(self, path: str) -> tuple[str, str]:
        if any(prefix_matches(path, prefix) for prefix in self.config.local_api_prefixes):
            return "local-api", self.config.local_api_url
        if path == "/api" or path.startswith("/api/"):
            return "prod-dashboard", self.config.prod_dashboard_url
        return "local-frontend", self.config.local_frontend_url

    def forward(
        self,
        upstream_kind: str,
        upstream_base: str,
        target_url: str,
        body: bytes | None,
        force_token_refresh: bool,
    ) -> tuple[int, dict[str, str], bytes]:
        headers: dict[str, str] = {}
        for key, value in self.headers.items():
            lower = key.lower()
            if lower in HOP_BY_HOP_HEADERS or lower in {"host", "content-length", "accept-encoding"}:
                continue
            if upstream_kind == "prod-dashboard" and lower == "cookie":
                value = strip_cf_access_cookie(value)
                if not value:
                    continue
            headers[key] = value

        parsed_base = urllib.parse.urlsplit(upstream_base)
        headers["Host"] = parsed_base.netloc
        headers["X-Forwarded-Host"] = self.headers.get("Host", "")
        headers["X-Forwarded-Proto"] = "http"

        if upstream_kind == "prod-dashboard":
            token = self.token_provider.token(force_refresh=force_token_refresh)
            existing_cookie = headers.get("Cookie", "")
            cf_cookie = f"CF_Authorization={token}"
            headers["Cookie"] = f"{existing_cookie}; {cf_cookie}" if existing_cookie else cf_cookie

        request = urllib.request.Request(
            target_url,
            data=body,
            headers=headers,
            method=self.command.upper(),
        )

        try:
            with OPENER.open(request, timeout=self.config.request_timeout_seconds) as response:
                return response.status, dict(response.headers.items()), response.read()
        except urllib.error.HTTPError as response:
            return response.code, dict(response.headers.items()), response.read()

    def write_health(self) -> None:
        payload = {
            "ok": True,
            "local_frontend_url": self.config.local_frontend_url,
            "local_api_url": self.config.local_api_url,
            "prod_dashboard_url": self.config.prod_dashboard_url,
            "local_api_prefixes": self.config.local_api_prefixes,
            "allow_mutating_prod": self.config.allow_mutating_prod,
        }
        body = json.dumps(payload, sort_keys=True).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command.upper() != "HEAD":
            self.wfile.write(body)


class ThreadingHTTPServer(http.server.ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def main() -> None:
    listen_host = os.environ.get("PROXY_LISTEN_HOST", "127.0.0.1")
    listen_port = int(os.environ.get("PROXY_LISTEN_PORT", "19080"))
    config = ProxyConfig(
        local_frontend_url=normalize_base_url(os.environ["LOCAL_FRONTEND_URL"]),
        local_api_url=normalize_base_url(os.environ["LOCAL_API_URL"]),
        prod_dashboard_url=normalize_base_url(
            os.environ.get("PROD_DASHBOARD_URL", "https://dashboard-prod.phishsonar.com")
        ),
        local_api_prefixes=parse_prefixes(os.environ.get("LOCAL_API_PREFIXES", "")),
        allow_mutating_prod=env_bool("ALLOW_MUTATING_PROD", False),
        cloudflared_bin=os.environ.get("CLOUDFLARED_BIN", "/usr/local/bin/cloudflared"),
        access_token_url=os.environ.get("ACCESS_TOKEN_URL", "https://dashboard-prod.phishsonar.com"),
        access_login_command=os.environ.get(
            "ACCESS_LOGIN_COMMAND",
            "/workspace/tools/access/accessctl login prod dashboard",
        ),
        token_refresh_seconds=int(os.environ.get("TOKEN_REFRESH_SECONDS", "3000")),
        request_timeout_seconds=int(os.environ.get("REQUEST_TIMEOUT_SECONDS", "60")),
    )

    server = ThreadingHTTPServer((listen_host, listen_port), ProxyHandler)
    server.config = config  # type: ignore[attr-defined]
    server.token_provider = AccessTokenProvider(config)  # type: ignore[attr-defined]
    print(
        "gateway prod-ui proxy listening on "
        f"{listen_host}:{listen_port}; local_api_prefixes={config.local_api_prefixes}",
        flush=True,
    )
    server.serve_forever()


if __name__ == "__main__":
    main()
